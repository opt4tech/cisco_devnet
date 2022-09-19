# Network to Code Technical Interview Challenge
*Ethan Angele - Sr. Consultant*

## Environment Setup
The first thing that I did before writing any code was read the full instructions and get the environment setup. 

- I was happy to see that visual studio code was setup on the Ubunut machine.
- With visual studio code on the machine, I saw no reason to do anything with git since I am both executing and developing the code locally. 
- To complete my code development space, I used the Remote-SSH extention from my own machine so that I wouldn't have to work through an RDP session. 
- Got the folders setup as directed. 
- Next, I setup the python virtual environment and installed napalm and ansible. I also did a pip freeze to build a requirements file for future use. 

`python -m venv ./ntc`
`source ntc/bin/activate`
`pip install napalm`
`pip install ansible`
`pip install napalm-ansible`
`pip install ansible-pylibssh`
`pip freeze >> requirements.txt`


## Exercise 1 - Python
### Program Design Considerations
As I started to consider the program requirements. I saw three separate functions that needed to occur:

1. Configure interfaces
2. Configure BGP
3. Validations

Those three components drove the modular design of the program at first, but I quickly realized that doing the program that way ended up with a lot of code reuse. For example, both configure interfaces and configure bgp needed to render configurations and apply them. I ended up switching the design to enhance code reuse, code readability, and code modularity. The program follows the following three components:

1. Render
2. Configure
3. Validate

The main function handles the calls to the sub functions within the program and those subfunctions call the modules with the appropriate information needed to complete each task. The goal of this design was to maximize code reuse, plus setting the config_option variable allows for task specific log output at the same time. This makes it easy to see what the program is doing each step of the way. 

The main function begins by creating the router objects that will store the main methods for what we will configure and test. I chose to do a object-oriented program structure because of the flexibility and brings after the objects are created for simply calling attributes and executed the router methods without having to create separate structures to store that information for each router in a list or dictionary. 

### Inventory
I decided to keep the inventory modular as opposed to one large file. I always tend to do this for readability and the ease of being able to add config items to devices for other programs in the future. 

### Program Workflow

![program flow](./media/python_program_flow.png)

- Main()
The main function directs the flow and order of the program. It also set's up the objecs and the logging used throughout. 

The objects are setup compelte with the bgp and interface attributes that are used throughout the program. This step made constantly using yaml load unnecessary. Load these attributes once and use them for the rest of the program.

The program needs to completley setup the interface configuration and verify that it is as expected before moving to the bgp configuration. The main function directs that. 

- Logging
The logging setup was simply to report messages in a simple to read format to the stdout for the user to follow the program. This setup is ideal over print statements because you can change the format in one config line and you can redirect to an output file for log recording.

Each log begins with what part of the program it is under. MAIN, BUILD, CONFIG, or VALIDATE. This is simply for readability for the user. 

- Run()
The run function was created to reuse code between the config tasks. Otherwise the method calls were very repetative. 

- Connect()
This method simply establishes a connection with the remote device.
    - Timeout
    I set the timeout to 30 to give interfaces and the napalm ping more time to complete. The program would intermittently fail due a timeout at that stage. 

- Build()
This method takes the config option as input, either interfaces and bgp, and then grabs the respective attributes to merge them with the corresponding jinja2 template. This produces the config to be applied, which also gets stored within each device object.

- Config()
This method takes the config option as input again, grabs that config and calls the ConfigureDevice module. This module uses napalm to apply the config that was created in the build function.

- Validate()
This method takes the config option as well and continues to run the tests appropriate for that config option. For interfaces, it checks the state of the interfaces using napalm get_interfaces() and then performs a napalm ping reachability tests to its neighbors. For bgp, it uses the napalm get_bgp_neighbors to ensure that each neighor is up. 

    - Retries

    For the validation stage, it was necessary to incorporate a simple retry mechanism with a pause to allow time for the bgp neighbors or interfaces to come online. The logging in the program shows this flow. 

- Close()
This function closes the connection to the device. 

### Security Considerations

I think its important to note, that I would not normally leave the username and password information in the variable files or within the code. That was left this way so that the program can be ran without user input as a part of the challenge. What I have done in the past to make the program CLI friendly and pipeline friendly (Azure Devops or Github) was to use environment variables or input prompts. Have the pipeline tool set those environment variables at runtime and if they do not exist, prompt for the information.

### RUN BASH
The bash script contains everything a user should need to run the program including the environment setup. This script could easily be used in a pipeline tool like Azure Devops to ensure that which ever agent picked up the job, the results would be consistent.  

## Excersie 2 - Ansible
### Program Design and Structure

The Ansible program design only had two components that I needed to ensure happened in a specific order. First, configure interfaces and test them. Second, configure BGP and test. Ansible made the flow easier because the strategy is by default linear which means that each task will be executed on every device before moving forward. Plus, less consideration needed to be made with building/rendering configurations because by default ansible pulls in the host variables and group variables if they are in the right folder structures. 

The program structure was as follows:
1. Configure and Validate
    -   Configure interface settings using the Cisco ios_config module with the SRC option for a jinja template.
    - Validate interfaces according to the validation files. 
    - Ensure L3 reachability to it's neighbors. 
    - Configure BGP Settings using the ios_config module with the jinja template.
    - Validate that BGP is up according to the Napalm validation file. 
2. Save the configurations

### Inventory
The inventory setup consists of host_vars for each device with sub yml files for bgp attributes or interface attributes of that device. The group_vars has one group for now, the ios group which all three devices belong to. 

### Validations
The validation files were somewhat frustrating to me because they contained the same information that exists in the inventory variable files. I could not use them as ansible variable files because of the "-" in front of the getter and I could not use them for napalm validate without that "-" in front of the getter. Since I cannot stand the idea of have more then one location with the same information, I switched to using jinja templates to auto-generate those napalm validate files based on the host variables. This allows those files to be dynamic and based on the inventory, which in this program is the source of truth.

- Retries
    Ansible provides a method for performing retries and pauses between attempts. This was used for each of the validation steps to give the interfaces and/or the bgp sessions time to come up.

### Ansible Config
Simple config was all that was required. Added an entry for the ansible hosts file and entries to use napalm within the python virtual environment. 

### RUN BASH
The bash script contains everything a user should need to run the program including the environment setup. This script could easily be used in a pipeline tool like Azure Devops to ensure that which ever agent picked up the job, the results would be consistent. 