.. _how_xt_works:

=======================================
How XT Works
=======================================

Ensure we cover stages of submitting a run:

    - determining hyperparameter search style
    - capturing snapshot of code
    - building setup script
        - activate cmd, conda, python
        - data/model mount or download
        - run controller or user app
    - job submit:
        - create XT job and run(s)
        - upload code
        - user and XT environment variables
        - build service configuration params
        - backend submit
    - node execution:
        - service pre-processing
        - setup for XT controller or run (direct mode):
            - download code
            - unzip code
            - activate, conda, python
        - XT controller runs (and launches run)
            - opens MRC file
            - queues single or parent run
        - run(s) terminates
            - XT controller does run wrapup
        - XT controller exit
        - service post-processing


How XT operates:
    1. internally, XT maintains a set of default settings and credentials for all commands and services
    2. selected credentials and XT options to override defaults are specified in a local directory config file
    3. XT's command line options can override/supplement the config file settings

Basic XT configuration:
    1. [optional] Enter your Azure service credentials in the [xt-services] section of your config file
    2. [optional] Create entries in the [compute-targets] sections for the COMPUTE targets to use for running experiments
    3. [optional] Enter the computers that you have available to run with in the [boxes] section 

XT runs:
    1. normally, XT is run against a RUN SCRIPT (.bat or .sh) that you have written.  
       This RUN SCRIPT should:

            - perform any needed machine preparation, for example:
                - activate a conda virtual environment
                - downloads data for ML app
                - install ML app dependencies

            - run your ML app

            - do any optional post processing/analysis

    2. if you are creating child runs (thru the --repeat or --runs options), you may want 
       to specify a PARENT SCRIPT (using the --parent-script option) that will be run once
       on the target machine, before running the child runs.

    3. in some situations, you can XT directly against a python file.  For these cases, 
       XT will create a default RUN SCRIPT that includes a "activate conda xxx" command at the 
       beginning.  For your local machine, "xxx" will be the currently active conda environment.
       For running on Azure Batch or other boxes, "xxx" will be set to "py36".  For these situations,
       the target machine will be assumed to be ready to run your app.
    
How XT runs your program:

    1. user runs XT, with a command that targets a RUN script, an app, or a file

    2. XT does the following:
        - creates a new XT Job
        - creates an XT Run for each box to be used
        - a "created" event is logged for each Run
        - uploads the BEFORE files from your current directory to your Job's cloud storage
        - a "capture_before" event is logged for the Job
        - schedules the runs on their respective boxes 

    3. On each box, an instance of the XT controller app does the following:
        - receives incoming runs requests and inserts them into the box's run-queue
        - a "queued" event is logged for each of these runs
        - monitors the run-queue entries and each run's lifetime
        - starts runs from run-queue, to simultaneous maximum specified by the "max-runs" setting 
    
    4. When a run is started, the controller does the following:
        - a "started" event is logged for the Run
        - downloads the BEFORE files from the Job's cloud storage 
        - a "download_before" event is logged for the Run
        - if a RUN script was specified, $RUN_ARGS$ entry for this Run is updated
        - if no RUN script was found, one is created with default settings
        - the RUN script is executed (with Environment variables set for the Run)
        - as the Run process executes, STDOUT and STDERR output are monitored and redirected:
            - to a "output.txt" file in the current directory
            - to any "XT attach" listeners
        - the Run process does it's user-level logging:
            - hyperparameter settings
            - metric snapshots
        - when the Run process terminates:
            - an "ended" event is logged for the Run
            - the run's AFTER files are uploaded to Run's cloud storage
            - an "capture_after" event is logged for the Run

    5. Special handling for runs with "--repeat" specified:
        - these runs are called PARENT runs
        - when they are removed from the run-queue (and about to be run):
            - if a PARENT script was specified:
                - the PARENT script is run. 
                - after the PARENT script completes, the PARENT run is requeued
        - if there is no PARENT script, or it has already been run:
            - a CHILD run is created from the PARENT run 
            - the CHILD run is started (see # 4 above)
            - the --repeat count for the PARENT is decremented
            - if the --repeat count is non-zero, the PARENT run is requeued

For information about XT commands, run: xt help