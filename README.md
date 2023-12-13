# ESISAR Volttron Agents
The ESISAR Volttron Agents project was undertaken within the framework of the PX504 course. The primary goal of this project was to develop a Smart Building management platform using VOLTTRON™.

**Project Objectives :**
* __Communication and Interactions Testing :__ Evaluate and test the communication and interactions between different agents within the VOLTTRON™ platform.
* __Integration of Multi-Agent Algorithms:__ Implement the integration of pre-existing multi-agent algorithms onto embedded boards, specifically Raspberry Pi devices.
* __Documentation :__ Provide comprehensive documentation covering the setup, configuration, and functionality of the developed Smart Building management platform.

**Project Members :**
* Thibaut Oprinsen : apprentice student
* Syed Fahimuddin Alavi : MISTRE student
* Lucas Abad : apprentice student

# Introduction 
This section will provide the essential information necessary for utilizing our agents.

## The volttron plateform
VOLTTRON™ is an open source, scalable, and distributed platform that seamlessly integrates data, devices, and systems for sensing and control applications. It is built on extensible frameworks allowing contributors to easily expand the capabilities of the platform to meet their use cases. Features are implemented as loosely coupled software components, called agents, enabling flexible deployment options and easy customization.

### Overview
Developing scalable, reusable applications to deploy in the field without spending development resources on operational components not specific to the application

Low-cost data collection deployable on commodity hardware

Integration hub for connecting a diverse set of devices together in a common interface

Testbed for developing applications for a simulated environment

![](image/volttron_diagram.png)

### Key features 
A message bus allowing connectivity between agents on individual platforms and between platform instances in large scale deployments

Integrated security features enabling the management of secure communication between agents and platform instances

A flexible agent framework allowing users to adapt the platform to their unique use-cases

A configurable driver framework for collecting data from and sending control signals to buildings and devices

automatic data capture and retrieval through our historian framework

An extensible web framework allowing users and services to securely connect to the platform from anywhere

Capability to interface with simulation engines and applications to evaluate applications prior to deployment


### Useful Links
* [Volttron website](https://volttron.org/)
* [Volttron Read The docs](https://volttron.readthedocs.io/en/main/)
* [Volttron Github](https://github.com/VOLTTRON/volttron)


## The Raspberry Pi 3
### Overview
### Key features 
### Useful Links

# Getting started
To run the project a minimum of one Raspberry Pi is required for internal Volttron testing. For testing communication between two Volttron instances, a minimum of two Raspberry Pi boards is necessary.
## Booting the Raspberry
We have two options to boot a Raspberry :

1. Using the existing configuration
2. flashing a new Raspbian OS.

We opted to install a fresh Raspbian OS on our Raspberry Pi to ensure compatibility with factory configurations, making our project accessible to a wider audience.

## Installing the volttron plateform
Volttron is an IoT platform that operates based on a message bus infrastructure. The message bus employed by Volttron can utilize either ZMQ (ZeroMQ) or RabbitMQ for communication. This choice allows flexibility in adapting to different messaging technologies based on project requirements or preferences.

### ZeroMQ
1. Clone the repository 
```bash
git clone https://github.com/VOLTTRON/volttron
```

>[!TIP]
> We recommand to switch to last release branch and not remain on the `main` branch beecause it's used for development.
> 
>add this flag to the git command `--branch release/8.2`

2. Environment setup 
Install the virtual enironment with the python helper script 
```bash
cd volttron
python3 boostrap.py
```
Now activate the virtual environment
```bash
source env/bin/activate
```
>[!NOTE]
>If the command worked you should see this in your terminal:
>```bash
>(volttron)user@hostname:~/Desktop/volttron$ 
>```

3. 
### RabiitMQ
TODO

## Setting up our project
When the volttron platerform is installed on our two raspberry we can now proceed to running both agents.
### Project structure
```bash
Esiar_Agents/
├── ReceiverSenderAgent_RaspberryB
│   ├── config
│   ├── config_web_address
│   ├── receiversender
│   │   ├── agent.py
│   │   └── __init__.py
│   └── setup.py
└── SenderReceiverAgent_RaspberryA
    ├── config
    ├── config_web_address
    ├── senderreceiver
    │   ├── agent.py
    │   └── __init__.py
    └── setup.py
```
>[!NOTE]
>The project is decomposed like that because volttron agents need one or more config files. To execute our agents on differents target, we need to have differents configuration  mainly because of the `config_web_address` that will contains the key of our volttron instance.

### Multi-Plateform configuration
0. **Find the key of your volttron plateform**

TODO

1. **Enable the Multi-plateform communication**

We need to add some configuarion in the volttron global configuration file. The `$VOLTRON_HOME` environment variale should point at the folder where the config file is located. Otherwise by default it will be installed at `$HOME/.volttron`.
```bash 
nano $VOLTRON_HOME/config
```
Now that the file is open we can add our configuration :
```plaintext
[volttron]
vip-address = tcp://127.0.01:22916  # In our case it is 10.0.0.x
instance-name = "platformA" # Whatever name you want
```

2. **Setup Configuration and Authentication Manually**

If you do not need web servers in your setup, then you will need to build the platform discovery config file manually. The config file should contain an entry containing VIP address, instance name and serverkey of each remote platform connection. Create the file at `$VOLTRON_HOME/`.
```bash
touch external_platform_discovery.json && nano external_platform_discovery.json
```
Now that the file is open we can add our configuration (here it's an example it's  not our values):
```json
{
    "platform2": {"vip-address":"tcp://127.0.0.2:22916",
                  "instance-name":"platform2",
                  "serverkey":"PLATEFORM2_KEY"
                 },
    "platform3": {"vip-address":"tcp://127.0.0.3:22916", 
                  "instance-name":"platform3",
                  "serverkey":"PLATEFORM3_KEY"
                 }
}
```
>[!NOTE]
> `PLATEFORM2_KEY` and `PLATEFORM3_KEY` both referer to the platerform key whiwh can be found with in step 0.

> [!IMPORTANT]
> The Volttron doc says that it's possible do disable security and authentification but we were unable to make it work.


