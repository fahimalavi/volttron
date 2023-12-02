#!/bin/bash

vctl remove receiversenderagent-0.1
rm volttron.log
vctl install --agent-config services/core/ReceiverSenderAgent_RaspberryB/config services/core/ReceiverSenderAgent_RaspberryB/
vctl start receiversenderagent-0.1
vctl status
cat volttron.log | grep ERROR
