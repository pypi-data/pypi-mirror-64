#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_pool.py: handles the platform submit/manage operations for service_types of pool and local
import os
import uuid
import shutil
from interface import implements

from xtlib import utils
from xtlib import errors
from xtlib import attach
from xtlib import pc_utils
from xtlib import scriptor
from xtlib import constants
from xtlib import file_utils
from xtlib import run_helper
from xtlib import process_utils
from xtlib import box_information
from xtlib.xt_client import XTClient

from xtlib.console import console
from xtlib.helpers.feedbackParts import feedback as fb

from .backend_interface import BackendInterface
from .backend_base import BackendBase

class PoolBackend(BackendBase):
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super(PoolBackend, self).__init__(compute, compute_def, core, config, username, arg_dict)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username
        self.env_vars = None
        self.client = self.core.client

    def adjust_run_commands(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, 
        args):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  This 
        base implementation does so by generating a new script file and adding it to the snapshot_dir.
        '''
        store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable,  \
            storage_name, storage_key = self.get_action_args(args)

        # local or POOL of vm's
        wrapped_parts = None     # we use same cmd on each box/job
        data_local = args["data_local"]

        for i, box_runs in enumerate(job_runs):
            # wrap the user commands in FIRST RUN of each box (apply data/model actions)
            br = box_runs[0]
            box_info = br["box_info"]
            box_name = box_info.box_name
            box_secret = br["box_secret"]
            actions = box_info.actions

            is_windows = box_info.box_os == "windows"

            run_specs = br["run_specs"]
            cmd_parts = run_specs["cmd_parts"]

            if not wrapped_parts:

                # we only do this once (for the first box/job)
                using_localhost =  pc_utils.is_localhost(box_name, box_info.address)

                # data_local overrides store_data_dir for LOCAL machine
                if using_localhost and data_local:
                    store_data_dir = os.path.expanduser(data_local)
                    data_action = "use_local"
                    if not "data" in actions:
                        actions.append("data")

                setup = self.config.get_setup_from_target_def(self.compute_def)

                env_vars = self.get_env_vars_for_box(box_name, box_info, i, box_secret)
                post_cmds = []

                # add env vars to script
                setter = "@set" if is_windows else "export"

                for name, value in env_vars.items():
                    cmd = "{} {}={}".format(setter, name, value)
                    post_cmds.append(cmd)

                #"xt download before/code --job={} --unzip "

                wrapped_parts = super().wrap_user_command(cmd_parts, snapshot_dir, store_data_dir, data_action, 
                    data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key, actions, 
                    is_windows=is_windows, pip_freeze=False, setup=setup, post_setup_cmds=post_cmds, args=args)

            # we update each box's command
            run_specs["cmd_parts"] = wrapped_parts

    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
           repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):

        fake_submit = args["fake_submit"]
        info_by_node = {}
        job_info = {"job": job_id}

        if not fake_submit:
            # first pass - ensure all boxes are NOT already running the controller
            for i, box_runs in enumerate(job_runs):
                box_info = box_runs[0]["box_info"]

                box_name = box_info.box_name
                box_addr = box_info.address
                port = constants.CONTROLLER_PORT

                if self.core.client.is_controller_running(box_name, box_addr, port):
                    errors.config_error("XT controller already running on box: " + box_name)

            # second pass - transfer the main script to each box and start it
            for i, box_runs in enumerate(job_runs):
                box_info = box_runs[0]["box_info"]

                # start run on specified box
                service_node_info = self.run_job_on_box(job_id, box_runs, box_index=i, box_info=box_info, app_info=None, 
                    pool_info=compute_def,  resume_name=resume_name, repeat=repeat_count, 
                    using_hp=using_hp, exper_name=experiment, snapshot_dir=snapshot_dir, args=args)

                node_id = "node" + str(i)
                info_by_node[node_id] = service_node_info

        return job_info, info_by_node

    def run_job_on_box(self, job_id, run_data_list, box_index, box_info, app_info, pool_info,  
            resume_name=None, repeat=None, using_hp=None, exper_name=None, snapshot_dir=None, args=None):
        '''
        copy the startup script to the specified box (using SCP) and run it (using SSH)
        '''
        box_name = box_info.box_name
        workspace = args["workspace"]
        #console.print("box_name=", box_name, ", box_index=", box_index)

        box_addr = box_info.address
        is_local = box_addr == "localhost"

        src_windows = pc_utils.is_windows()
        dst_windows = box_info.box_os == "windows"

        hold_open = args["hold"]
        run_data = run_data_list[0]
        run_name = run_data["run_name"]
        ws = args["workspace"]

        # kill any running instances of the controller on the box (those that didn't shut down cleanly)
        self.client.cancel_thru_os(box_name, False)

        # send over files to box
        dest_dir = utils.get_controller_cwd(dst_windows, is_local=False)
        fn_bootstrap = file_utils.path_join(dest_dir, os.path.basename(self.fn_wrapped))
        visible = args["show_controller"]

        if is_local:
            # LOCAL box
            # COPY the snapshot directory (localhost)
            file_utils.copy_tree(snapshot_dir, dest_dir, omit_dirs="__pycache__")
            fb.feedback("files copied to box")
            fb.feedback("{}/{}".format(ws, run_name))

            # start controller  (localhost)
            fn_log = os.path.expanduser("~/.xt/controller.log")
            process_utils.start_async_run_detached(fn_bootstrap, dest_dir, fn_log, visible=visible)

        else:
            # REMOTE box
            # copy the .zip file using scp
            src_dir = os.path.expanduser(constants.CWD_DIR) if src_windows else constants.CWD_DIR
            fn_src = file_utils.path_join(src_dir, constants.CODE_ZIP_FN)
            fn_dest = file_utils.path_join(dest_dir, constants.CODE_ZIP_FN)

            process_utils.scp_copy_file_to_box(self, box_addr, fn_src, fn_dest)

            # unzip the file
            # 1. we need the remote box expanded fn_dest
            err_code, output = process_utils.sync_run_ssh(self, box_addr, "ls " + fn_dest)
            full_fn_dest = output.strip()

            cmd = ''' python -c \\"import zipfile;  zip = zipfile.ZipFile('{}', 'r'); zip.extractall('{}')\\" '''.format(full_fn_dest, os.path.dirname(full_fn_dest))
            err_code2, output2 = process_utils.sync_run_ssh(self, box_addr, cmd)

            fb.feedback("files copied to box")
            fb.feedback("{}/{}".format(ws, run_name))

            # start the run
            run_in_cmd_window = visible

            if run_in_cmd_window:
                # for debugging, open a new cmd window and watch real-time output from remote box
                cmd = "bash --login " + fn_bootstrap
                ssh_cmd = process_utils.make_ssh_cmd(box_addr, cmd)

                local_cwd = utils.get_controller_cwd(True, is_local=True)
                fn_ssh = os.path.join(local_cwd, "run_ssh.bat")
                fn_log = os.path.join(local_cwd, "run_ssh.log")
                file_utils.write_text_file(fn_ssh, ssh_cmd)

                os.system("start cmd /K " + fn_ssh)

                #process_utils.start_async_run_detached(cmd, local_cwd, fn_log, visible=True)
            else:
                # normal run 
                #cmd = "bash --login " + fn_bootstrap
                cmd = ' "nohup bash --login {} </dev/null   > ~/.xt/controller.log 2>&1 &" '.format(fn_bootstrap) 

                process_utils.sync_run_ssh(self, box_addr, cmd)

        fb.feedback("submitted", is_final=True)  
        
        monitor_url = None

        service_node_info = {"job_id": job_id, "node_index": box_index, "box_name": box_name, "monitor_url": monitor_url}

        return service_node_info

    def get_env_vars_for_box(self, box_name, box_info, nodex_index, box_secret):
        #box_secrets.set_secret(box_name, box_secret)

        box_os = box_info.box_os
        max_runs = box_info.max_runs

        node_id = "node" + str(nodex_index)
        env_vars = {}
        scriptor.add_controller_env_vars(env_vars, self.config, box_secret, node_id)

        return env_vars

    def get_client_cs(self, service_node_info):
        '''
        Args:
            service_node_info: info that service maps to a compute node for a job
        Returns:
            {"ip": value, "port": value, "box_name": value}
        '''
        box_name = service_node_info["box_name"]
        controller_port = constants.CONTROLLER_PORT
        tensorboard_port = None
        ssh_port = 22

        if not box_name in self.config.get("boxes"):
            if pc_utils.is_localhost(box_name):
                box_name = "local"

        box_addr = self.config.get("boxes", box_name, dict_key="address", default_value=box_name, 
            prop_error="box not defined in config file: " + box_name)

        if "@" in box_addr:
            # strip off the username
            _, box_addr = box_addr.split("@", 1)
        #console.print("box_addr=", box_addr)

        if not "." in box_addr and box_addr != "localhost":
            raise Exception("box option must specify a machine by its IP address: " + str(box_addr))

        cs = {"ip": box_addr, "port": controller_port, "box_name": box_name}
        return cs
    
    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):

        boxes, pool_info, service_type = box_information.get_box_list(self.core, job_id=job, pool=self.compute)

        def monitor_work():
            # BOX LOOP
            text = ""
            for b, box_name in enumerate(boxes):
                # make everyone think box_name is our current controller 
                self.client.change_box(box_name)

                if run_name in ["tensorboard", "mirror"]:
                    text += self.get_box_process_status_inner(box_name, wworkspaces, run_name)
                else:
                    text += self.core.get_box_run_status_inner(box_name, workspace, run_name, stage_flags)

            return text

        # MONITOR-ENABLED COMMAND
        attach.monitor_loop(monitor, monitor_work, escape_secs=escape_secs)

    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results = None

        try:
            # connect to specified box
            first_run_name = run_names[0]

            cs, box_secret = run_helper.get_client_cs(self.core, workspace, first_run_name)
            if not cs:
                console.print("could not find client connection string for run: {}/{}".format(workspace, first_run_name))
            else:
                # add workspace to run_names
                run_names = [workspace + "/" + run_name for run_name in run_names]

                # send request to controller via the client service
                with XTClient(self.config, cs, box_secret) as xtc:
                    if xtc.connect():
                        cancel_results = xtc.cancel_runs(run_names)
                    else:
                        console.print("couldn't connect to controller for {}".format(box_name))
        except BaseException as ex:
            errors.report_exception(ex)
            pass

        return cancel_results

    def cancel_runs_by_property(self, prop_name, prop_value, box_name):
        cancel_results = None

        try:
            # connect to specified box
            if self.client.change_box(box_name):
                cancel_results = self.client.cancel_runs_by_property(prop_name, prop_value)
            else:
                console.print("couldn't connect to controller for {}".format(box_name))
        except BaseException as ex:
            errors.report_exception(ex)
            pass

        return cancel_results
        
    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results_by_box = {}

        for box_name, runs in runs_by_box.items():
            cancel_results = self.cancel_runs_by_property("job_id", job_id, box_name)
            cancel_results_by_box[box_name] = cancel_results

        return cancel_results_by_box

    def cancel_runs_by_user(self, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results =  self.cancel_runs_by_property("username", self.username, box_name)
        return cancel_results

    # def _launch_controller_localhost_windows(self, env_vars, box_info, python_script, controller_script, visible):
    #     fn_script_log = os.path.expanduser(constants.CONTROLLER_SCRIPT_LOG)

    #     # python_run_cmd = 'python -u -c "{}" > {}'.format(python_script, fn_controller_run_log)
    #     # utils.send_cmd_as_script_to_box(self, box_addr, python_run_cmd, fn_batch, prep_script, False)

    #     controller_script = scriptor.fixup_script(controller_script, for_windows=True, is_local=True)
    #     fn_batch = scriptor.write_controller_script_file(controller_script, is_windows=True)

    #     #console.print("fn_batch=", fn_batch)
    #     console.diag("  running batch file: " + fn_batch)

    #     parts = process_utils.make_launch_parts(box_info.shell_launch_prefix, [fn_batch])
    #     #console.print("parts=", parts)

    #     #console.print("just before subprocess.Popen, PYTHONPATH=", os.getenv("PYTHONPATH"), ", parts=", parts)

    #     if visible:
    #         fn_batch = file_utils.fix_slashes(fn_batch)
    #         console.diag("  running controller on LOCALHOST, Windows, fn_batch=" + str(fn_batch) + ", creationFlags=" + str(DETACHED_PROCESS))

    #         p = subprocess.Popen(parts, cwd=".", env=env_vars, creationflags=DETACHED_PROCESS) 
    #     else:
    #         with open(fn_script_log, 'w') as output:
    #            subprocess.Popen(parts, cwd=".",  env=env_vars, creationflags=CREATE_NO_WINDOW, stdout=output, stderr=subprocess.STDOUT) 

    # def _launch_controller_localhost_linux(self, env_vars, box_info, python_script, controller_script, visible):
    #     # # nohup is most reliable when used on python (vs. the shell script)
    #     # python_run_cmd = 'nohup python -u -c "{}" </dev/null > {} 2>&1 &'.format(python_script, fn_controller_run_log)
    #     # utils.send_cmd_as_script_to_box(self, box_addr, python_run_cmd, fn_script, prep_script, True)

    #     # specify "--login" so that script can access conda, etc.
    #     #run_cmd = ['/bin/sh', '--login', fn_script]

    #     controller_script = scriptor.fixup_script(controller_script, for_windows=False, is_local=True)
    #     fn_script = scriptor.write_controller_script_file(controller_script, is_windows=False)

    #     parts = process_utils.make_launch_parts(box_info.shell_launch_prefix, [fn_script])

    #     # TODO: capture output here?   
    #     # with open(fn_script_log, 'w') as output:
    #     console.diag("_launch_controller_localhost_linux: parts={}".format(parts))
    #     process = subprocess.Popen(parts, env=env_vars,)

    # def _launch_controller_remote_linux(self, env_vars, box_info, python_script, controller_script, visible):
    #     # fn_script = constants.CONTROLLER_SHELL
    #     # fn_controller_run_log = constants.CONTROLLER_RUN_LOG
    #     box_addr = box_info.address
        
    #     controller_script = scriptor.fixup_script(controller_script, for_windows=False, is_local=False)

    #     # since we cannot set the env_vars from this box, add env_vars just after first line in controller script
    #     for name, value in env_vars.items():
    #         cmd = "export {}={}".format(name, value)
    #         controller_script.insert(1, cmd)

    #     local_fn_script = scriptor.write_controller_script_file(controller_script, is_windows=False)
    #     remote_fn_script = constants.CONTROLLER_BATCH 

    #     # ensure REMOTE scripts dir exists
    #     box_cmd = "mkdir -p {}".format(os.path.dirname(remote_fn_script))
    #     process_utils.sync_run_ssh(self, box_addr, box_cmd)

    #     # for proper bg run, we need to redirect all 3: STDIN, STDOUT, and STDERR
    #     # nohup python -u -c "from xtlib import controller; controller.run(max_runs=1)" </dev/null   > ~/.xt/controller.log 2>&1  &
    #     # python_run_cmd = 'nohup python -u -c "{}" </dev/null  > {} 2>&1 &'.format(python_script, fn_controller_run_log)

    #     # copy the controller script file to the box         
    #     scriptor.send_script_to_remote_box(self, box_addr, fn_source=local_fn_script, fn_dest=remote_fn_script, linux_box=True)

    #     # the "nohup" command requires the shell
    #     # specify "--login" so that script can access conda, etc.
    #     run_cmd = process_utils.make_launch_cmd(box_info.shell_launch_prefix, remote_fn_script)

    #     process_utils.sync_run_ssh(self, box_addr, run_cmd)

    # def _launch_controller_common(self, box_name, box_addr, visible, demand_script=None):
    #     # for now, we will rely on:
    #     #   - the local/remote machine's active environment having xtlib installed (TODO: pip install xtlib, as needed)
    #     #   - remote box is running linux (TODO: support Windows-based remote boxes)

    #     # since we have to run multiple commands (conda and python), its much easier to develop/debug if we push
    #     # a shell script to the local/remote box and run that.

    #     # start controller on pool machine; generate a secret for subsequent communication 
    #     box_secret = str(uuid.uuid4()) 
    #     box_secrets.set_secret(box_name, box_secret)
    #     self.token = box_secret

    #     box_info = box_information.BoxInfo(self.config, box_name=box_name, store=self.store)
    #     #app_info = app_information.AppInfo(self.config, app_path="xtlib/controller.py", box_info=box_info)

    #     # app_info = self.core.get_app_info("xtlib/controller.py")
    #     # box_os = self.core.get_box_os(box_name)
    #     box_os = box_info.box_os

    #     # get prep script for XT controller
    #     #prep_script, shell_launch_prefix = self.core.get_prep_script(app_info, box_name, "combined")
    #     #prep_script = app_info.get_prep_script("combined")

    #     using_localhost =  pc_utils.is_localhost(box_name, box_addr)

    #     for_windows = using_localhost and pc_utils.is_windows()
    #     controller_script = scriptor.get_controller_script(box_name, box_info.box_class, for_windows, self.config)

    #     # this assumes we have all boxes we used defined, including "local"
    #     #box_info = self.core.get_box_info(box_name, {"max-runs": 1, "os": "linux"})
    #     max_runs = box_info.max_runs

    #     console.diag("launching controller on {} (addr={}, max-runs={}, box_os={}, controller_script={})".format(
    #         box_name.upper(), box_addr,  max_runs, box_os, controller_script))

    #     if using_localhost:
    #         env_vars = os.environ.copy()
    #     else:
    #         env_vars = {}

    #     # pool currently doesn't have access to job's env_vars
    #     #user_ev = args["env_var"]
    #     #env_vars.update(user_ev)        
    #     #env_vars["XT_NODE_ID"] = node_id

    #     node_id = "node0"
    #     scriptor.add_controller_env_vars(env_vars, self.config, box_secret, node_id)

    #     if demand_script:
    #         python_script = demand_script
    #     else:
    #         ip_only = self.core.get_ip_addr_from_box_addr(box_addr)
    #         python_script = None  # "from xtlib.controller import run as run; run(max_runs={}, my_ip_addr='{}')".format(max_runs, ip_only)

    #     if using_localhost:
    #         if pc_utils.is_windows():
    #             self._launch_controller_localhost_windows(env_vars, box_info, python_script, controller_script, visible)
    #         else:
    #             self._launch_controller_localhost_linux(env_vars, box_info, python_script, controller_script, visible)
    #     else:
    #         self._launch_controller_remote_linux(env_vars, box_info, python_script, controller_script, visible)
            
    # def run_local(self, run_specs, run_name, exper_name, app_info, job_id, box_name, resume_name, context, args):
    #     console.diag("run_local: start")
    #     wd = os.path.abspath(".")

    #     # better to send as JSON
    #     json_context = json.dumps(context.__dict__)

    #     # cannot pass None using rPYc?
    #     cmd_parts = run_specs["cmd_parts"]
    #     if cmd_parts is None:
    #         cmd_parts = ""

    #     fake_submit = args["fake_submit"]
    #     if not fake_submit:
    #         self.ensure_token_is_set()
    #         result, status = self.conn.root.queue_job(self.token, json_context, cmd_parts)
    #         console.diag("run_local: after queue_job")

    #     # copy to submit-logs
    #     dd = {"context": context.__dict__, "cmd_parts": cmd_parts}
    #     utils.copy_data_to_submit_logs(args, dd, "run_local.log")

    # def run_box(self, run_specs, run_name, exper_name, app_info, job_id, box_name, resume_name, context, args):

    #     # start the job
    #     console.diag("  sending controller request to run cmds on box: " + str(run_specs))

    #     # better to send as JSON
    #     json_context = json.dumps(context.__dict__)

    #     # cannot pass None using rPYc?
    #     cmd_parts = run_specs["cmd_parts"]
    #     if cmd_parts is None:
    #         cmd_parts = ""

    #     fake_submit = args["fake_submit"]
    #     if not fake_submit:
    #         self.ensure_token_is_set()
    #         self.conn.root.queue_job(self.token, json_context, cmd_parts)

    #     # copy to submit-logs
    #     dd = {"context": context.__dict__, "cmd_parts": cmd_parts}
    #     utils.copy_data_to_submit_logs(args, dd, "run_box.log")

