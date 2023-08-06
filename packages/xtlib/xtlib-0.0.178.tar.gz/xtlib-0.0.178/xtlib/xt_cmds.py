#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# xt_cmds.py: defines the XT commands, arguments, and options
'''
XT currently has about 60 commands and 90 arguments/options.  The goal
of this module is to remove all the explict parsing and usage of the 
config file, from the actual command definitions and entrypoints.
'''
import sys
import time
import logging
import importlib

from xtlib import qfe
from xtlib import utils
from .console import console
from xtlib import errors
from .helpers.feedbackParts import feedback
from .impl_shared import ImplShared

logger = logging.getLogger(__name__)

def main(cmd=None, new_start_time=None, capture_output=False):
    '''
    This is the XT app, used to manage and scale ML experiments, support various backends (Philly, Azure Batch, Azure ML).
    '''
    if new_start_time:
        global xt_start_time
        xt_start_time = new_start_time

    import numpy as np
    seed = 5
    if seed:
        np.random.seed(seed)
        np.random.RandomState(seed)

    if cmd:
        if cmd.startswith("xt "):
            cmd = cmd[3:]
        elif cmd == "xt":
            cmd = ""

        args = utils.cmd_split(cmd)

        # remove empty args
        args = [arg for arg in args if arg]
    else:
        # if caller did not supply cmd
        args = sys.argv[1:]
   
    # when executing multiple commands, reset the feedback for each command
    feedback.reset_feedback()

    #console.print("cmd=", cmd, ", args=", args)
    console.diag("in xt_cmds.main")

    #console.print("config=", config)

    impl_shared = ImplShared()
    config = impl_shared.init_config()
    store = impl_shared.store

    cmd_providers = config.get("providers", "command")
    impl_dict = {}

    for name, code_path in cmd_providers.items():
        package, class_name = code_path.rsplit(".", 1)
        module = importlib.import_module(package)
        impl_class = getattr(module, class_name)

        impl = impl_class(config, store)
        impl_dict[package] = impl


    # this enables QFE to match a function by its module name, to the class instance to process the command
    # impl_dict = {"xtlib.impl_utilities": utilities, "xtlib.impl_storage": storage, 
    #     "xtlib.impl_compute": compute, "xtlib.impl_help": help_impl}

    # this parses args and calls the correct command function with its args and options correctly set.
    # the config object supplies the default value for most options and flags.
    dispatcher = qfe.Dispatcher(impl_dict, config, preprocessor=impl_shared.pre_dispatch_processing)

    # hide under-development commands
    hide_commands  = ["collect_logs", "start_tensorboard", "stop_tensorboard"]

    # hide internal cmds (for xt development use only)
    hide_commands.append("generate_help")
    dispatcher.hide_commands(hide_commands)

    # expand symbols like $lastjob, $lastrun
    impl_shared.expand_xt_symbols(args)

    # this is the NORMAL outer exeception handling block, but
    # also see the client/server exception handling in xt_run.py
    try:
        text = dispatcher.dispatch(args, capture_output=capture_output)  
    except BaseException as ex:
        #console.print("in Exception Handler: utils.show_stack_trace=", utils.show_stack_trace)
        # does user want a stack-trace?
        logger.exception("Error during displatcher.dispatch, args={}".format(args))

        exc_type, exc_value, exc_traceback = sys.exc_info()
        errors.process_exception(exc_type, exc_value, exc_traceback)

    return text

if __name__ == "__main__":
    main()
