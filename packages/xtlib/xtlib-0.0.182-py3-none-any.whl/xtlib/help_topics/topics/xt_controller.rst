.. _xt_controller:

========================================
XT Controller
========================================

The XT controller app prodes several services to ML apps running under its control.  Users can elect
to bypass the XT controller and run directly under the control of the backend service by specifying
the --direct flag on the XT run command.

The XT controller currently provides the following services:

    scheduling:

        - scheduling runs on the node (up to --max-runs-per-box simultaneous runs)

        - creating child runs (for parent runs with the --repeat option)

        - running parent prep scripts before starting the child runs

    hyperparameter search:

        - generating new app config files for child runs, based on selected search algorithm

    run support:

        - downloading code files at start of runs

        - uploading after files at end of runs

        - logging of create, before, after run events

    XT client support:
        
        - attach/detach to console file

        - cancel runs, jobs

        - get status of node, jobs, and runs

    