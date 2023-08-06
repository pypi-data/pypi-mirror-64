#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# client.py - cmds related to talking with the XT controller on the compute node.

'''
NOTE: the code in this module is being refactored and moved into:
    - xt_client.py
    - attach.py
    - impl_compute.py
    - cmd_core.py
'''

import os
import sys
import json
import rpyc
import time
import uuid
import arrow
import socket 
import socket 
import signal   
import psutil    
import datetime
import numpy as np
import subprocess   
from time import sleep

from .helpers.bag import Bag
from .helpers.key_press_checker import KeyPressChecker
from .helpers.feedbackParts import feedback as fb

from xtlib import utils
from xtlib import errors
from xtlib import capture 
from xtlib import scriptor
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib import box_secrets
from xtlib import process_utils
from xtlib import box_information

from xtlib.store import Store
from xtlib.console import console
from xtlib.backends.backend_batch import AzureBatch
from xtlib.report_builder import ReportBuilder   

# constants
SH_NAME ="xtc_run.sh"

CONTROLLER_NAME_PATTERN = "xtlib.controller"
DETACHED_PROCESS = 0x00000008
CREATE_NO_WINDOW = 0x08000000

class Client():
    '''
    This class is responsible for talking to the XT controller (on local machine, VM's, or backend services)
    '''
    def __init__(self, config=None, store=None, core=None):
        self.config = config
        self.store = store
        self.blob_client = None     # will allocate on demand
        self.visible_for_debugging = False
        self.port = constants.CONTROLLER_PORT
        self.conn = None
        self.conn_box = None
        self.core = core
        self.token = None

    def ensure_token_is_set(self):
        #self.token = mongo.read_job_info("job_secret", jobNNN)
        #print("ensure_token_is_set: self.token=", self.token)
        assert self.token

    def create_new_client(self, config):
        return Client(config, self.store, self.core)

    def get_config(self):
        return self.config

    def cancel_runs(self, run_names):
        self.ensure_token_is_set()

        # send results as json text so that we are not tied to controller (which may be killed immediately after this call)
        results_json_text = self.conn.root.cancel_run(self.token, run_names)
        results = json.loads(results_json_text)
        return results

    def cancel_runs_by_property(self, prop_name, prop_value):
        self.ensure_token_is_set()
        # send results as json text so that we are not tied to controller (which may be killed immediately after this call)
        #                             cancel_runs_by_property
        results_json_text = self.conn.root.cancel_runs_by_property(self.token, prop_name, prop_value)
        results = json.loads(results_json_text)
        return results

    def connect(self, box_name, ip_addr, port):
        self.ensure_token_is_set()

        self.conn = None
        self.conn_box = None
        
        fn_server_public= os.path.expanduser(constants.FN_SERVER_CERT_PUBLIC)
        xt_server_cert = self.config.get_vault_key("xt_server_cert")

        use_public_half = False    # cannot get the public half approach to work

        try:
            # write CERT file JIT
            if use_public_half:
                _, public_half = xt_server_cert.split("END PRIVATE KEY-----\n")
                file_utils.write_text_file(fn_server_public, public_half)
            else:
                file_utils.write_text_file(fn_server_public, xt_server_cert)

            # # PHILLY experiment
            # ip_addr = "10.185.170.184"
            # ip_addr = 12815

            self.conn = rpyc.ssl_connect(ip_addr, port=ip_addr, keyfile=None, certfile=fn_server_public) 
            self.conn_box = box_name
        finally:
            # delete the CERT file
            #os.remove(fn_server_public)
            pass

    def is_controller_running(self, box_name, box_addr, port=constants.CONTROLLER_PORT):
        if not port:
            port = constants.CONTROLLER_PORT
            
        # KISS: just try to connect
        is_running = False

        try:
            ip_addr = self.core.get_ip_addr_from_box_addr(box_addr)
            console.diag("  trying to connect with: ip_addr={}, port={}".format(ip_addr, port))

            self.connect(box_name, ip_addr, port=port)
            is_running = True
        except BaseException as ex:
            console.diag("  received exception: " + str(ex))
            is_running = False
            #raise ex   # uncomment to see the stack trace

        console.diag("  is_controller_running: " + str(is_running))
        return is_running

    def cancel_controller(self, box_name, os_call_only=False):
        shutdown = False

        if not os_call_only:
            try:
                # first try to cancel it thru a SHUTDOWN REQUEST
                self.ensure_token_is_set()

                info = box_information.get_box_addr(self.config, box_name, self.store)
                box_addr = info["box_addr"]

                is_running = self.is_controller_running(box_name, box_addr)
                if is_running:
                    self.conn.root.shutdown(self.token)
                    shutdown = True
            except BaseException as ex:
                console.print("shutdown request result: ex={}".format(ex))
                raise ex    

        if not shutdown:
            # if above fails, kill the process if local or PEER
            self.cancel_thru_os(box_name)

    def cancel_thru_os(self, box_name, show_progress=True):
        progress = console.print if show_progress else console.diag

        progress("  checking running processes on: " + box_name)

        is_local = pc_utils.is_localhost(box_name)
        #console.print("box_name=", box_name, ", is_local=", is_local)

        ''' kill the controller process on the specified local/remote box'''
        if is_local:  # pc_utils.is_localhost(box_name, box_addr):
            result = self.cancel_local_controller(progress)
        else:
            result = self.cancel_remote_controller(box_name, progress)

        return result

    def cancel_local_controller(self, progress):
        # LOCALHOST: check if controller is running 
        python_name = "python"  # "python.exe" if pc_utils.is_windows() else "python"

        processes = psutil.process_iter()
        cancel_count = 0

        for p in processes:
            try:
                if p.name().lower().startswith("python"):
                    console.detail("process name: {}".format(p.name()))
                    cmd_line = " ".join(p.cmdline())

                    if CONTROLLER_NAME_PATTERN in cmd_line or constants.PY_RUN_CONTROLLER in cmd_line:
                        process = p
                        process.kill()
                        progress("  controller process={} killed".format(process.pid))
                        cancel_count += 1

            except BaseException as ex:
                pass
        
        result = cancel_count > 0
        if not result:
            progress("  local XT controller not running")

        return result

    def cancel_remote_controller(self, box_name, progress):
        # REMOTE BOX: check if controller is running 
        box_addr = self.config.get("boxes", box_name, dict_key="address")
        if not box_addr:
            errors.config_error("missing address property for box: {}".format(box_name))
    
        # run PS on box to determine if controller is running
        box_cmd = "ps aux | grep controller"
        exit_code, output = process_utils.sync_run_ssh(self, box_addr, box_cmd)
        
        #console.print("result=\n", output)
        targets = [text for text in output.split("\n") if "python" in text]
        #console.print("targets=", targets)

        cancel_count = 0

        if len(targets):
            for target in targets:
                parts = target.split(" ")

                # remove empty strings
                parts = list(filter(None, parts))

                #console.print("parts=", parts)
                if len(parts) > 1:
                    pid = parts[1].strip()

                    # send "cancel" command to remote linux box
                    box_cmd = 'kill -kill {}'.format(pid)
                    progress("  killing remote process: {}".format(pid))
                    process_utils.sync_run_ssh(self, box_addr, box_cmd, report_error=True)

                    cancel_count += 1

        result = cancel_count > 0
        if not result:
            progress("  remote XT controller not running")

        return result

    def connect_to_controller(self, box_name=None, ip_addr=None, port=None):
        '''
        establish communication with the XT controller process on the specified box.
        return True if connection established, False otherwise.
        '''
        connected = False
        console.diag("init_controler: box_name={}".format(box_name))

        if self.conn == box_name:
            connected = True
        else:
            if ip_addr:
                box_addr = ip_addr
            else:
                info = box_information.get_box_addr(self.config, box_name, self.store)
                box_addr = info["box_addr"]
                controller_port = info["controller_port"]
                self.token = info["box_secret"]   
                
                ip_addr = self.core.get_ip_addr_from_box_addr(box_addr)
                port = controller_port if controller_port else constants.CONTROLLER_PORT

            # the controller should now be running - try to connect
            try:
                console.diag("  connecting to controller")
                self.connect(box_name, ip_addr, port=port)
                console.diag("  connection successful!")

                # magic step: allows our callback to work correctly!
                # this must always be executed (even if self.conn is already true)
                bgsrv = rpyc.BgServingThread(self.conn)
                console.diag("  now running BgServingThread")
                connected = True
            except BaseException as ex:
                #self.report_controller_init_failure(box_name, box_addr, self.port, ex)
                # most common reasons for failure: not yet running (backend service) or finished running
                pass

        return connected 

    def close_controller(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.conn_box = None

        
    def cancel_controller_by_boxes(self, box_list):
        for box_name in box_list:
            # connect to specified box
            self.change_box(box_name)
            self.cancel_controller(box_name)
       

    def get_tensorboard_status(self, ws_name, run_name, box_name):
        if ws_name and run_name:
            self.connect_to_box_for_run(run_name)
        else:
            self.change_box(box_name)

        # get running status from controller
        status = self.conn.root.get_tensorboard_status(self.token)            

        # add other info to status
        if not box_name:
            box_name, job_id, node_index = self.get_run_info(ws_name, run_name)

        info = box_information.get_box_addr(self.config, box_name, self.store)
        tensorboard_port = info["tensorboard_port"]
        
        status["box_name"] = box_name
        status["ip_addr"] = ip_addr
        status["tensorboard_port"] = tensorboard_port if tensorboard_port else constants.TENSORBOARD_PORT

        return status


    def set_token_from_box_secret(self, box_name):
        self.token = box_secrets.get_secret(box_name)
        assert self.token

    def change_box(self, box_name, port=None): 
        self.set_token_from_box_secret(box_name)
        self.connect_to_controller(box_name, port=port)

    def get_connection_info(self, ws, run_name):
        '''
        - get IP_ADDR, PORT, and TASK_STATE from backend service for specified:
            - run
            - job_id, node_index

            1. look up service_id for job/node in job store
            2. ci = backend.get_connect_info(service_id)
            3. use ci["port"] and ci["ip_addr"] to connect in client
        '''
        pass

    def get_run_info(self, ws_name, run_name):
        # get job_id from first log record
        box_name = None
        job_id = None
        node_index = None

        records = self.store.get_run_log(ws_name, run_name)
        dd = records[0]["data"]
        box_name = dd["box_name"]

        if utils.is_azure_batch_box(dd["box_name"]):
            # get extra info for azure-batch nodes
            job_id = dd["job_id"]
            node_index = dd["node_index"]

        return box_name, job_id, node_index

    def connect_to_box_for_run(self, ws_name, run_name):
        state = None
        box_name, job_id, node_index = self.get_run_info(ws_name, run_name)
        info = box_information.get_box_addr(self.config, box_name, self.store)
        ip_addr = info["box_addr"]
        controller_port = info["controller_port"]

        if not controller_port:
            controller_port = self.port

        if state == "deallocated":
            connected = False
        elif controller_port:
            connected = self.connect_to_controller(ip_addr=ip_addr, port=controller_port)
        else:
            connected = self.connect_to_controller(box_name=box_name)

        if controller_port:
            box_name = ip_addr + ":" + str(controller_port)
            
        return state, connected, box_name, job_id


    # def pool_loop(self, boxes, func, init_controller=True):
    #     results = []

    #     for b, box_name in enumerate(boxes):
    #         #console.print("box_name=", box_name)

    #         # make everyone think box_name is our current controller 
    #         self.change_box(box_name)

    #         result = func(box_name, b)
    #         results.append(result)

    #     return results


    # def monitor_attach_run(self, ws, run_name, show_waiting_msg=True, escape=0):
    #     console.print("")    # separate the waiting loop output from previous output
    #     attach_attempts = 0

    #     def monitor_work():
    #         nonlocal attach_attempts
    #         azure_task_state, connected, box_name, job_id = self.connect_to_box_for_run(ws, run_name)
    #         attach_attempts += 1

    #         #if not connected:
    #         #    utils.user_exit("Unable to attach to run (state={})".format(state))
    #         if azure_task_state:
    #             #console.print("azure_task_state=", azure_task_state)
    #             # its an azure-batch controlled run
    #             if azure_task_state == "active":
    #                 text = "Waiting for run to start: {} ({} in azure-batch)".format(run_name.upper(), job_id)
    #             elif azure_task_state == "running" and not connected:
    #                 text = "Waiting for run to initialize: {} ({} in azure-batch)".format(run_name.upper(), job_id)
    #             else:
    #                 # exit monitor loop
    #                 return azure_task_state, connected, box_name, job_id, attach_attempts
    #         else:
    #             # its a normal box-controller run
    #             if not connected:
    #                 errors.env_error("could not connect to box: " + box_name)
    #             # we are connected, but has run started yet?
    #             status_dict = self.get_status_of_runs(ws, [run_name])
    #             # controller may not have heard of run yet (if we were fast)
    #             status = status_dict[run_name] if run_name in status_dict else "created"
    #             if status in ["created", "queued"]:
    #                 text = "Waiting for run to start: {} (queued to run on {})".format(run_name.upper(), box_name)
    #             else:
    #                 # status is one of running, killed, completed, spawning, ...
    #                 # exit monitor loop
    #                 return azure_task_state, connected, box_name, job_id, attach_attempts
    #         return text

    #     # wait for run to be attachable in a MONITOR LOOP
    #     result = self.monitor_loop(True, monitor_work, "[hit ESCAPE to detach] ", escape)
    #     #console.print("")    # separate the waiting loop output from subsequent output  

    #     if result:
    #         state, connected, box_name, job_id, attach_attempts = result
    #         #console.print("state=", state, ", connected=", connected, ", box_name=", box_name, ", job_id=", job_id)

    #         if not connected:
    #             if False:  #   attach_attempts == 1:
    #                 errors.user_exit("Unable to attach to run (state={})".format(state))
    #             else:
    #                 # not an error in this case
    #                 console.print("Unable to attach to run (state={})".format(state))
    #                 return
                    
    #         console.print("<attaching to: {}/{}>\n".format(ws, run_name))
    #         self.attach_task_to_console(ws, run_name, show_waiting_msg=show_waiting_msg, escape=escape)
    #     else:
    #         # None returned; user cancelled with ESCAPE, so no further action needed
    #         pass    

    # def monitor_loop(self, monitor, func, action_msg="monitoring ", escape_secs=0):
    #     '''
    #     set up a loop to continually call 'func' and display its output, until the ESCAPE key is pressed
    #     '''
    #     # handle the easy case first
    #     if not monitor:
    #         text = func()
    #         console.print(text, end="")
    #         return

    #     pc_utils.enable_ansi_escape_chars_on_windows_10()

    #     if monitor == True:
    #         monitor = 5     # default wait time
    #     else:
    #         monitor = int(monitor)
    #     started = datetime.datetime.now()

    #     started2 = time.time()
    #     timeout = escape_secs
    #     if timeout:
    #         timeout = float(timeout)

    #     last_result = None

    #     # MONITOR LOOP
    #     with KeyPressChecker() as checker:
    #         while True:
    #             result = func()
    #             if not isinstance(result, str):
    #                 # func has decided to stop the monitor loop itself
    #                 if last_result:
    #                     console.print("\n")
    #                 return result

    #             if last_result:
    #                 # erase last result on screen
    #                 console.print("\r", end="")
    #                 line_count = len(last_result.split("\n")) - 1 

    #                 # NOTE: on some systems, the number of lines needed to be erased seems to 
    #                 # vary by 1.  when it is too many, it destroys prevous output/commands.  until
    #                 # this is corrected, we pick the lower values that will cause some extra
    #                 # output on some systems.

    #                 #line_count += 1     # add 1 for the \n we will use to clearn the line
                    
    #                 pc_utils.move_cursor_up(line_count, True)

    #             elapsed = utils.elapsed_time(started)
    #             result += "\n" + action_msg + "(elapsed time: {})...".format(elapsed)

    #             console.print(result, end="")
    #             sys.stdout.flush()
                
    #             if timeout:
    #                 elapsed = time.time() - started2
    #                 if elapsed >= timeout:
    #                     console.print("\nmonitor timed out")
    #                     break

    #             # wait a few seconds during refresh
    #             if pc_utils.wait_for_escape(checker, monitor):
    #                 console.print("\nmonitor cancelled")
    #                 break

    #             last_result = result
    #     return None


    # def get_status_of_runs(self, ws, run_names):
    #     # use strings to communicate (faster than proxy objects)
    #     run_names_str = "^".join(run_names)
    #     #console.print("run_names_str=", run_names_str)
    #     self.ensure_token_is_set()
    #     json_status_dict = self.conn.root.get_status_of_runs(self.token, ws, run_names_str)
    #     #console.print("json_status_dict=", json_status_dict)

    #     box_status_dict = json.loads(json_status_dict)

    #     return box_status_dict

    # def get_status_of_workers(self, worker_name):
    #     # get status from controller
    #     self.ensure_token_is_set()
    #     status_text = self.conn.root.get_status_of_workers(self.token, worker_name)
    #     status_list = json.loads(status_text)
    #     return status_list

    # def filtered_out(self, status, active_only):
    #     if active_only and status not in ["created", "queued", "allocating", "spawning", "active", "running"]:
    #         return True

    #     return False

    # def jobs_report(self, ws=None, run_name=None, stage_flags=""):

    #     # create helper for filtering runs to show
    #     builder = ReportBuilder(self.config, self.store, self)
    #     status = ""
    #     #builder.init_filtering(status)
    #     #active_only = builder.filtering_active_only()

    #     # get runs from controller
    #     self.ensure_token_is_set()
    #     status_list = self.conn.root.get_runs(self.token, stage_flags, ws_name=ws, run_name=run_name).split("\n")[0:-1]

    #     if status_list:
    #         records = []
    #         for stats in status_list:
    #             ws, name, status, elapsed = stats.split("^")
    #             full_name = ws + "/" + name
    #             #console.print("full_name=", full_name)

    #             if not self.filtered_out(status, False):
    #                 elapsed = utils.format_elapsed_hms(elapsed)
    #                 record = {"name": full_name, "status": status, "elapsed": elapsed}
    #                 records.append(record)

    #         result, rows = builder.build_formatted_table(records, avail_cols=["name", "status", "elapsed"])
    #     else:
    #         result = "  <none>" + "\n"

    #     return result

    # def status_to_desc(self, run_name, status):
    #     if status == "queued":
    #         desc = "{} has been queued".format(run_name)
    #     elif status == "spawning":
    #         desc = "{} is spawning repeat runs".format(run_name)
    #     elif status == "running":
    #         desc = "{} has started running".format(run_name)
    #     elif status == "completed":
    #         desc = "{} has completed".format(run_name)
    #     elif status == "error":
    #         desc = "{} has terminated with an error".format(run_name)
    #     elif status == "cancelled":
    #         desc = "{} has been killed".format(run_name)
    #     elif status == "aborted":
    #         desc = "{} has been unexpectedly aborted".format(run_name)
    #     else:
    #         desc = "{} has unknown status={}".format(run_name, status)

    #     return "<" + desc + ">"

    # def attach_task_to_console(self, ws_name, run_name, show_waiting_msg=False, show_run_name=False, escape=0):
    #     full_run_name = ws_name + "/" + run_name

    #     # callback for each console msg from ATTACHED task
    #     def console_callback(run_name, msg):
    #         if msg.startswith(constants.APP_EXIT_MSG):
    #             #console.print(msg)
    #             status = msg.split(":")[1].strip()
    #             desc = self.status_to_desc(run_name, status)
    #             console.print(desc, flush=True)
    #             context.remote_app_is_running = False
    #         else:
    #             if show_run_name:
    #                 console.print(run_name + ": " + msg, end="", flush=True)
    #             else:   
    #                 console.print(msg, end="", flush=True)
    #         sys.stdout.flush()

    #     # RPYC bug workaround - callback cannot write to variable in its context
    #     # but it CAN write to an object's attribute
    #     context = Bag()
    #     context.remote_app_is_running = True

    #     show_detach_msg = False
    #     detach_requested = False

    #     self.ensure_token_is_set()
    #     attached, status = self.conn.root.attach(self.token, ws_name, run_name, console_callback)
    #     #console.print("attached=", attached, ", status=", status)

    #     if attached:
    #         #if show_waiting_msg:
    #         #    console.print("\n<attached: {}>\n".format(full_run_name))

    #         started = time.time()
    #         timeout = escape
    #         if timeout:
    #             timeout = float(timeout)
    
    #         try:
    #             with KeyPressChecker() as checker:
        
    #                 # ATTACH LOOP
    #                 #console.print("entering ATTACH WHILE LOOP...")
    #                 while context.remote_app_is_running:
    #                     #console.print(".", end="")
    #                     #sys.stdout.flush()

    #                     if checker.getch_nowait() == 27:
    #                         detach_requested = True
    #                         break

    #                     time.sleep(.1)

    #                     if timeout:
    #                         elapsed = time.time() - started
    #                         if elapsed >= timeout:
    #                             break


    #         except KeyboardInterrupt:
    #             detach_requested = True
    #         finally:
    #             self.ensure_token_is_set()
    #             self.conn.root.detach(self.token, ws_name, run_name, console_callback)

    #         if detach_requested or show_waiting_msg:
    #             console.print("\n<detached from run: {}>".format(full_run_name))
    #     else:
    #         desc = self.status_to_desc(run_name, status)
    #         console.print(desc)

    #     # while True:
    #     #     sleep(.1)     

    # def get_controller_elapsed(self):
    #     self.ensure_token_is_set()
    #     return self.conn.root.elapsed_time(self.token, )

    # def get_controller_xt_version(self):
    #     self.ensure_token_is_set()
    #     return self.conn.root.xt_version(self.token, )

    # def get_controller_log(self):
    #     self.ensure_token_is_set()
    #     return self.conn.root.controller_log(self.token, )

    # def get_controller_ip_addr(self):
    #     self.ensure_token_is_set()
    #     return self.conn.root.get_ip_addr(self.token, )

    # def get_controller_max_runs(self):
    #     self.ensure_token_is_set()
    #     return self.conn.root.get_max_runs(self.token, )

    # def set_controller_max_runs(self, value):
    #     #console.print("value=", value, ", type(value)=", type(value))
    #     self.ensure_token_is_set()
    #     self.conn.root.set_max_runs(self.token, value)

    # def start_console_app(self, cmd, working_dir, fn_stdout, fn_stderr, console_type):
    #     '''
    #     This is the one that works for all 3 console_type values!  
    #     Tested on windows, 4/15/2019, rfernand2, "agent1" home machine.
    #     '''
    #     if console_type == "integrated":
    #         hidden, detached = False, False
    #     elif console_type == "hidden":
    #         hidden, detached = True, False
    #     elif console_type == "visible":
    #         hidden, detached = True, True
    #     else:
    #         raise Exception("unsupported console_type: " + str(console_type))

    #     creationflags = DETACHED_PROCESS if detached else 0
    #     console.print("hidden=", hidden, ", detached=", detached)

    #     # apparently, we don't have to hold the file open - this is sufficient (cool!)
    #     if hidden:
    #         with open(fn_stdout, 'w') as output:
    #             #with open(fn_stderr, 'a') as error:
    #             subprocess.Popen(cmd, cwd=working_dir, creationflags=creationflags, \
    #                 stdout=output, stderr=subprocess.STDOUT)   # stderr=error) 
    #     else:
    #          subprocess.Popen(cmd, cwd=working_dir, creationflags=creationflags)

            
    # def report_controller_init_failure(self, box_name, box_addr, port, ex):
    #     batch_ext = ".bat" if pc_utils.is_windows() else ".sh"

    #     if pc_utils.is_localhost(box_name, box_addr):
    #         fn_script = file_utils.fix_slashes(constants.CONTROLLER_BATCH)
    #         #fn_log = file_utils.fix_slashes(constants.CONTROLLER_SCRIPT_LOG)
    #         fn_log = file_utils.fix_slashes(constants.CONTROLLER_INNER_LOG)

    #         console.print("Exception while trying to connect to LOCAL controller on port: " + str(port) + "; " + str(ex))
    #         console.print("\nSuggested steps to debug problem:")
    #         #console.print("  1. Ensure that port '{}' is open on {}".format(port, box_addr))
    #         console.print("  1. Ensure that the generated script looks correct: {}".format(fn_script))
    #         console.print("  2. Check the output of '{}' for errors".format(fn_log))
    #         console.print("  3. Try running the script yourself: {}\n".format(fn_script))
    #     else:
    #         fn_log = constants.CONTROLLER_INNER_LOG
    #         console.print("Exception while trying to connect to REMOTE controller on port: " + str(port) + "; " + str(ex))
    #         console.print("\nSuggested steps to debug problem:")
    #         console.print("  1. Ensure that port " + str(port) + " is open on " + box_addr)
    #         console.print("  2. Check the output of '{}' (on box) for errors\n".format(fn_log))
