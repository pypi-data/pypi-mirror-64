.. _graduating_sandbox:

========================================
Graduating from Sandbox Services
========================================

The XT Sandbox Services were designed to make it easy to try out and learn how 
to use XT.  When you are ready to do real work, you will want to create your own set of services.

A set of the basic XT services can be shared by 1 more XT users and is referred as an **XT Team**.

--------------------------
Adding a new XT Team
--------------------------

Adding a new team to XT involves creating serveral Azure services and then
adding them to your local XT config file.  This page provides a step-by-step 
guide for how to create the services and the config file changes needed.

There are several selections that need to be made for creating each service, but the process of
creating each service is very similiar across services.  By the time you create the 
final service, you will have become very familiar with the pattern.

Here is a summary of the overall steps needed to add a new team and the time needed for each:
    - create the 6 Azure services (15-30 mins)
    - add the service keys and XT certificate to the key value (15 mins)
    - edit the local XT config file (15 mins)

--------------------------
The Azure Services for XT
--------------------------

There are 6 services associated with an XT team:

    - Storage               (provides cloud storage for your experiments)
    - Mongo DB              (provides fast Database access to the stats and metrics of your experiments)
    - Key Vault             (provides secure storage of the credentials for your services)
    - Azure Batch           (a general compute service that offers on-demand Virtual Machines)
    - Azure ML              (a compute services designed for Machine Learning on VMs)
    - Container Registry    (provides storage for docker images)

The below steps show you how to create these services from the Azure Portal.  Mostly, we will
be relying on the default settings when creating these services, except as noted below. 

--------------------------
Automation of Steps
--------------------------

As an alternative to following Steps 5.4-5.9 below (which create the 6 services used by XT), you can use the new **xt create team** command to 
generate a single Azure template to create the services.  See the link at the botto of this page for more information on this approach.


--------------------------------------------
Creating the Storage Service
--------------------------------------------

1. Select a simple, short team name for your XT team, without any special punctuation.  For example, "phoenix".

2. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "Storage Account"
    - select the Microsoft "Storage account - blob, file, table, queue" item
    - click on "Create"

3. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you create a NEW group named the same as your XT team
    - for "Storage account name", we recommend your team name, followed by "storage" (e.g., phoenixstorage)
    - for "Location", choose a location that is close to your team's primary location.  you will use this same location for all of your XT services.
    - for "Account kind", choose "Storage (general purpose v1)" 
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Mongo DB Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "Cosmos"
    - select the Microsoft "Azure Cosmos DB" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Account name", we recommend your team name, followed by "mongodb" (e.g., phoenixmongodb)
    - for "API", choose "Azure Cosmos DB for MongoDB API"
    - for "Location", choose the same location used for your Storage service
    - for "Version", select "3.2"
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.


--------------------------------------------
Creating the Key Vault Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "key vault"
    - select the Microsoft "Key Vault" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Key vault name", we recommend your team name, followed by "keyvault" (e.g., phoenixkeyvault)
    - for "Region", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.


--------------------------------------------
Creating the Azure Batch Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "batch service"
    - select the Microsoft "Batch Service" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Account name", we recommend your team name, followed by "batch" (e.g., phoenixbatch)
    - for "Location", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Azure ML Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "machine learning"
    - select the Microsoft "Machine Learning" item
    - click on "Create"

2. For the Create dialog::

    - for "Workspace name", we recommend your team name, followed by "aml" (e.g., phoenixaml)
    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Location", choose the same location used for your Storage service
    - for "Workspace edition", choose "Enterprise"
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Container Registry Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "registry"
    - select the Microsoft "Container Registry" item
    - click on "Create"

2. For the Create dialog::

    - for "Registry name", we recommend your team name, followed by "registry" (e.g., phoenixregistry)
    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Location", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Container Registry is normally created instantly and the Portal navigates to the newly created service.

---------------------------------------------------
Creating the Vault Secret
---------------------------------------------------

You will now create a single secret (containing the keys for 4 of your services) and add it to your vault.  This will involve navigating 
between your newly created services.  For navigating to services in the Azure Portal, we suggest::

    - click on "Resource groups" in the left-most sidebar 
    - click on your team resource group
    - find and click on the desired service (ignore the service names with extra text appended to them)

1. Using a code or text editor, paste the following JSON dictionary string into an empty file::

    { 
        "phonenixstorage": "key",   
        "phoenixmongodb": "key",  
        "phonenixbatch": "key", 
        "phoenixregistry": "key"
    }

2. replace each of the service names in the above with your service names (suggestion: do an editor replace of "phonenix" to your team name)

3. for each of the "key" strings, replace them with the associated service key or connection string values.  For this step, you will 
need to navigate to each service in the Azure Portal and click on the "Keys" or "Connection string" tab in the left side panel and copy the 
primary key or conenction string value.  Here are the specifics::

    a. for the Storage service:
        - navigate to your storage service
        - click on the "Access Keys" tab in the service's side panel
        - click on the "Key 1" copy-to-clipboard button
        - paste into your editor for the storage service key value 

    b. for the Mongo DB service:
        - navigate to your mongodb service
        - click on the "Connection string" tab in the service's side panel
        - click on the "PRIMARY CONNECTION STRING" copy-to-clipboard button
        - paste into your editor for the mongodb key value 

    c. for the Azure Batch service:
        - navigate to your batch service
        - click on the "Keys" tab in the service's side panel
        - click on the "Primary access key" copy-to-clipboard button
        - paste into your editor for the batch key value 

    d. for the Container Registry service:
        - navigate to your registry service
        - click on the "Access Keys" tab in the service's side panel
        - click on the "Enable" Admin User button
        - click on the "Password" copy-to-clipboard button
        - paste into your editor for the registry service key value 

4. from your code/text editor, copy the JSON dictionary string that you modified (both service names and keys) into your clipboard

5. In the Azure Portal::

    - navigate to your team Key Vault service 
    - click on the "Secrets" sidebar tab
    - click on the "+ Generate/Import" button
    - for "Name", enter "xt-keys"
    - for "Value", paste it the clipboard string (of your JSON dictionary)
    - click on "Create"

6. Finally, clean up::

    - note the filename associated with the JSON dictionary string in your editor (if any)
    - close JSON dictionary string file in your editor
    - delete the file from your local hard drive (if it exists)

---------------------------------------------------
Adding the XT certs to the vault
---------------------------------------------------

1. In the Azure Portal::

    - navigate to your team Key Vault service 
    - click on the "Certificates" tab in the service sidebar 

    a. create the CLIENT CERT
    - click on the "+ Generate/Import" button
    - for "Method of Certificate Creation", select "Generate"
    - for "Certificate Name", enter "xt-clientcert"
    - for "Subject", enter "CN-xtclient.com"
    - for "Content Type", change it to "PEM"
    - click on "Create"

    b. create the SERVER CERT
    - click on the "+ Generate/Import" button
    - for "Method of Certificate Creation", select "Generate"
    - for "Certificate Name", enter "xt-servercert"
    - for "Subject", enter "CN-xtserver.com"
    - for "Content Type", change it to "PEM"
    - click on "Create"


-----------------------------------------------------------
Create a Compute Instance for your AML service
-----------------------------------------------------------

1. Navigate to your Azure ML service

2. Click on the "Compute" tab button in the service sidebar

3. Click on the "+ New" button

4. For "Compute Name", we suggest the team name followed by "compute" (e.g., phoenixcompute)

5. For "Virtual Machine Size", select the CPU/GPU configuration for the VMs your service will use

6. Click "Create"


-----------------------------------------------------------
Editing your local XT config file 
-----------------------------------------------------------

1. Edit your local XT config file ('xt config' cmd)

2. copy/paste the following sections (or merge them with existing sections of the same name)::

    external-services:
        phoenixbatch: {type: "batch", key: "$vault", url: "xxx"}
        phoenixaml: {type: "aml", subscription-id: "xxx", resource-group: "phoenix"}
        phoenixstorage: {type: "storage", provider: "azure-blob-21", key: "$vault"}
        phoenixmongodb: {type: "mongo", mongo-connection-string: "$vault"}
        phoenixkeyvault: {type: "vault", url: "xxx"}
        phoenixregistry: {type: "registry", login-server: "xxx", username: "xxx", password: "$vault", login: "true"}

    xt-services:
        storage: "phoenixstorage"        # storage for all services 
        mongo: "phoenixmongodb"          # database used for all runs across services
        vault: "phoenixkeyvault"         # where to keep sensitive data (service credentials)

    compute-targets:
        batch: {service: "phoenixbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", environment: "none"}
        philly: {service: "philly", vc: "msrlabs", cluster: "rr2", sku: "G1", nodes: 1, low-pri: true, environment: "philly-pytorch"}
        aml: {service: "phoenixaml", compute: "xxx", vm-size: "Standard_NC6", nodes: 1, low-pri: false}
        bigbatch: {service: "labcoatbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", environment: "none"}

    general:
        workspace: "xxx"
        experiment: "xxx"
        primary-metric: "test-acc"             # name of metric to optimize in roll-ups, hyperparameter search, and early stopping
        maximize-metric: true                  # how primary metric is aggregated for hp search, hp explorer, early stopping 
        xt-team-name: "phoenix"                # for use with XT Grok
        bigbatch: {service: "labcoatbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", environment: "none"}
        pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "seaborn", "pandas", "xtlib==*"]       # packages to be installed by pip (xtlib, etc.)

3. replace all "phonenix" names with your names of the associated service 

4. replace all "xxx" values with the associated property of the specified service, using information from the Azure Portal.

5. for the "compute-targets" and "general" sections, review the settings and adjust as desired.  See the XT Config File help topic for additional information about these properties.


-----------------------------------------------------------
Adding your team to XT Grok
-----------------------------------------------------------

For now, this is a manual process.  Send a copy of your local XT config file to rfernand2 and he will add your team to XT Grok.

-----------------------------------------------------------
Test your newly added team
-----------------------------------------------------------

Test your new XT team configuration by running XT in the directory that contains your local XT config file.  Try the
following commands in the specified order::

    - xt list workspaces:
        - this will test that your Key Value and Storage services are configured correctly
        - if an error occurs here, double check the Key Vault service properties and XT configuration file properties for these services

    - xt create workspace ws-test 
        - this will ensure your Storage account is writable 
        - if you see an error here about "Block blobs are not supported", you likely selected the wrong version of the storage "kind" property.  If this is the case,
          you will need to recreate the storage services.

    - xt run <script>
        - this will ensure that the Mongo DB service is configured correctly
        - if you see the error "getaddrinfo failed", you likely have specified the wrong connection string for mongodb.  if so, you 
          will have to update the xt-keys secret in the vault.

    - xt --target=batch run <script>
        - this will ensure that the Batch service is configured correctly

    - xt --target=aml run <script>
        - this will ensure that the Batch service is configured correctly


If you need to recreate 1 or more of the services::

    - delete the old service.
    - create the new service using the same name.  Note: some services may take 5-10 minutes before the name can be reused.
    - get the keys string from the "xt-keys" secret in the Key Vault.
    - use an editor to update the keys for any new services.
    - create a new version of the xt-keys secret with the updated JSON dictionary string.
    - on your local machine, be sure to run "xt kill cache" before trying further testing.


.. seealso:: 

    - :ref:`create team cmd <create_team>`
    - :ref:`XT Config file <xt_config_file>`
    - :ref:`Preparing A New Project <prepare_new_project>`
