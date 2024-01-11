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
* Developing scalable, reusable applications to deploy in the field without spending development resources on operational components not specific to the application
* Low-cost data collection deployable on commodity hardware
Integration hub for connecting a diverse set of devices tog* ether in a common interface
* Testbed for developing applications for a simulated environment

![](image/volttron_diagram.png)

### Key features 
* A message bus allowing connectivity between agents on individual platforms and between platform instances in large scale deployments
* Integrated security features enabling the management of secure communication between agents and platform instances
* A flexible agent framework allowing users to adapt the platform to their unique use-cases
* A configurable driver framework for collecting data from and sending control signals to buildings and devices
* Automatic data capture and retrieval through our historian framework
* An extensible web framework allowing users and services to securely connect to the platform from anywhere
* Capability to interface with simulation engines and applications to evaluate applications prior to deployment


### Useful Links
* [Volttron website](https://volttron.org/)
* [Volttron Read The docs](https://volttron.readthedocs.io/en/main/)
* [Volttron Github](https://github.com/VOLTTRON/volttron)


## Raspberry Pi 3 B+
![](image/raspberryPI3B.png)
### Overview
The Raspberry Pi 3 B+ is a single-board computer developed by the Raspberry Pi Foundation. It delivers improved performance compared to its predecessors while maintaining the compact size characteristic of the Raspberry Pi family.

### Key features 

**Hardware components:**

- **Processor:** Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit SoC @ 1.4GHz
- **Memory:** 1GB LPDDR2 RAM
- **Network Connectivity:**
  - Gigabit Ethernet (via a USB controller)
  - Wi-Fi 802.11b/g/n/ac
  - Bluetooth 4.2/BLE
- **USB Ports:** 4 USB 2.0 ports
- **GPIO Ports:** 40 GPIO pins
- **Video Output:** Full-size HDMI, DSI port for touch screen display
- **Storage:** Micro-SD card slot for operating system and data storage
- **Power:** Micro-USB 5V/2.5A
- **Operating System:** Support for various operating systems, including Raspbian (now called Raspberry Pi OS), Ubuntu, etc.

**Common Uses:**

1. **Home Server:** Can be used as a web server, file server, or home media server.
2. **Educational Projects:** Ideal for learning programming and electronics.
3. **IoT (Internet of Things):** Widely used in IoT projects due to its compact size.
4. **Media Center:** Capable of streaming videos and managing media libraries.
5. **Home Automation:** Can be integrated into home automation projects.

### Useful Links

- [Official Raspberry Pi Foundation Website](https://www.raspberrypi.org/)
- [Official Documentation](https://www.raspberrypi.org/documentation/)


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


### RabiitMQ
In this section we will talk about our advancement in the installation of RabbitMQ, but we didn't manage to makE it work. Here we assume that you already cloned the repository.

0. Environment setup 

Install the virtual enironment with the python helper script 
```bash
cd volttron
python3 boostrap.py
```
Now activate the virtual environment
```bash
source env/bin/activate
```

1. Download erlang

RabbitMQ is written in erlang, so we need to install it. The volttron doc specify that only `erlang 24.1.7` is supported.

* Download erlang from [here](https://www.erlang.org/patches/otp-24.1.7)
* Untar the file (eg: tar -xvf <otp-24.1.7>)
* go to untared folder (eg: cd <otp_repository>)
* run the install script (eg: ./otp_build autoconf)

Now that these steps are done, there is 2 possibles output:
* Failure : missing dependencies (treated bellow)
* Success (skip missing dependencies steps)

We faced some missing dependencies while installing erlang

* ncurse
```bash
sudo apt install libncurses-dev
```

Once the missing dependencies installed we can proceed with the installation of erlang.

* run the execution script (eg: ./configure)
* ./make
* ./make install

2. Checking hostname consistency

As we have two raspberry with same honsmane (user or pi), we need to change hostname

* sudo nano /etc/hostname
change hostname's value (eg: RaspB)

* sudo nano /etc/hosts 
change the line : 127.0.1.1 "previous_name" to 127.0.1.1 <hostname>

3. Bootstrap the rabbitMQ env

bootstrap a second environment from the volttron home folder
```bash
python3 bootstrap.py --rabbitmq
```
4. Configure  

Go to your volttron home and write :
```bash
vcfg rabbitmq single # --config <path-to-rabbitmq_config.yml>
```
[!NOTE] you will have to provide at least: hostname and a unique common-name.

Go to rabbitmq repository (created at HOME) and check if rabbitMQ is working correctly.
```bash
cd rabbitmq_server/rabbitmq_server-3.9.7/sbin
./rabbitmqctl status
```
[!NOTE] Status should be okay

5. Starting Volttron

We can lauch volttron with RabbitMQ has the message bus.
```bash
./start-volttron
```
>[!NOTE] **CREATE A MULTIPLATFORM COMMUNICATION USING PUBSUB :**
>
>There are two ways to create a link between two volttron instances running RMQ : 
>* shovel plugin
>* federation plugin 
>
>In our case, we will use shovel plugin.
>
>Identify the instance that is going to act as the “publisher” instance and the one which will act as "subscriber" instance.
>
>On both, you will have to run
>```bash
>vcfg rabbitmq shovel
>```
>and provide the requested information, such as : 
>* hostname or ip address of remote platform you want to connect 
>* virtual host name of the remote platform
>* UID of the agent which will publish to the remote instance
>* device on which the agent should communicate
>
>Create the same link on the secon platform to create a bidirectiobal communication.

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

Run the command:
```bash
vctl auth <something>
```

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
> `PLATEFORM2_KEY` and `PLATEFORM3_KEY` both referer to the platerform key which can be found with in step 0.

> [!IMPORTANT]
> The Volttron doc says that it's possible do disable security and authentification but we were unable to make it work.

3. **Modifying the code**

Usually to Publish or Subscribe we use the annotations that comes from the `vip` library that is the  Message Bus API implemented by volttron.
```python 
@PubSub.subscribe('pubsub', '') # topic '' => every topics
``` 

To specify that we want to subscribe to topic from differents volttron instance, we need to add the `all_platforms` flag.
```python
@PubSub.subscribe('pubsub', '', all_platforms=True)
```

### Installing and launching an agent
1. **Lauching the plateform**

At the volttron plateform root
```bash
source env/bin/activate 
./start-volttron
```
This helper script is provided by volttron, but we can  use the command line to increase or decrease the log verbosity
```bash
volttron -vv -l volttron.log&  # add or rmove v flag
```

>[!NOTE]
>A stop script also exist. To stop the plateform run :
>```
>./stop-volttron
>``` 

2. **Install an agent**

The `vctl` command offer the possibility to install agent but as our agents are not part of volttron plateform, we prefer to pass by the `install-agent.py` script.
```bash
python scripts/install-agent.py -s ESISAR/ -c ESISAR/config -t PX505
```

To ensure that the agent is properly installed, we can run this command.
```bash
vctl status 
```
The output should be :
```bash
lgbfjhemzrf eehfùzerofeararh
```
3. **Start an agent**

To start an agent we use the `vctl` helper command, we can either use the `--tag` flag or we pass by the `uuid` generated by the plateform. Wa can find the uuid with the `vctl status` command.
```bash
vctl start --tag PX505
```
or
```bash
vctl start e5 
```

4. **Stop an agent**

We can stop an agent with the sop command. it has a similar comportment as the start command.
```bash
vctl stop --tag PX505
```
or
```bash
vctl stop e5 
```

5. **Uninstall an agent**

To uninstall an agent, we use the remove command, that also have a similar comportment as the start command.
```bash
vctl remove --tag PX505
```
or
```bash
vctl remove e5 
```

## Testing the Project

### Workflow
add bullshit image + photo test setup

### Raspberry A
1. [Install the plateform](##Installing-the-volttron-plateform)
2. [Do the Muti-plateform configarution](###Multi-Plateform-configuration)
3. Install our agent ([How to install an agents](###Installing-and-launching-an-agent))

In the current state of the repository our agent are located at `services/core`, to install it, we can use the `vctl` command.
```bash 
vctl install -c services/core/SenderReceiverAgent_RaspberryA/config services/core/SenderReceiverAgent_RaspberryA/
```
Before launching the agent we will go to [raspberry B](###Raspberry-B).

Now taht we launched the agent on raspberry B we can lauch our agent on this raspberry.
```bash 
vctl status
# Copy the UUID
vctl start <uuid>
```
Agents should be communicating
### Raspberry B
1. [Install the plateform](##Installing-the-volttron-plateform)
2. [Do the Muti-plateform configarution](###Multi-Plateform-configuration)
3. Install our agent ([How to install an agents](###Installing-and-launching-an-agent))

In the current state of the repository our agent are located at `services/core`, to install it, we can use the `vctl` command.
```bash 
vctl install -c services/core/ReceiverSenderAgent_RaspberryB/config services/core/ReceiverSenderAgent_RaspberryB/
```
We can now procede to launch our agents.
```bash
vctl status
# Copy the UUID
vctl start <uuid>
```
We are now subcribed to a topic comming from any volttron instance. We can now go back to the  [raspberry A](###Raspberry-A).

Agents should be communicating

### Results
Volltron come with a logging services. The logger print every logs on the plateform to a file `volttron.log` located at the volttron root. There is a lot of log so we decided to put ERROR log in our codes to properly see every exchange between ours agents.
```bash 
cat volttron.log | grep ERROR
```
We should have an output like this:
```bash
2023-12-15 18:01:05,040 (receiversenderagent-0.1 2719) __main__ ERROR: destination VIP is : (tcp://10.0.0.4:22916)
2023-12-15 18:01:05,040 (receiversenderagent-0.1 2719) __main__ ERROR: destination serverkey is : (None)
2023-12-15 18:01:05,040 (receiversenderagent-0.1 2719) __main__ ERROR: Destination serverkey not found in known hosts file, using config
2023-12-15 18:01:05,040 (receiversenderagent-0.1 2719) __main__ ERROR: destination serverkey is : (RhX8qIJWAeKFfVo85Qlxto0b4E2ieg5lkYhoTkNulnI)
2023-12-15 18:01:11,789 (senderreceiveragent-0.1 2729) __main__ ERROR: destination VIP is : (tcp://10.0.0.3:22916)
2023-12-15 18:01:11,789 (senderreceiveragent-0.1 2729) __main__ ERROR: destination serverkey is : (None)
2023-12-15 18:01:11,789 (senderreceiveragent-0.1 2729) __main__ ERROR: Destination serverkey not found in known hosts file, using config
2023-12-15 18:01:11,789 (senderreceiveragent-0.1 2729) __main__ ERROR: destination serverkey is : (MlT1bGQTbnuTUvatPECn1-wPNGXWvawT2n18ndP9KRQ)
```

We performed some tests and observed these results:

| Data Size (B)|    Time of unidirectinnal communication (ms)    | 
| :----:  |   :----:   | 
|1|	35,5|	
|5|	18	|
|100|	20|	
|1000|	21|	
|1440|	22|	
|1462|	23|	
|2000|	27|	
|5000|	46|	
|10000|	75|	
