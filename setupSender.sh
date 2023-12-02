#!/bin/bash

vctl remove senderreceiveragent-0.1
rm volttron.log
vctl install --agent-config services/core/SenderReceiverAgent_RaspberryA/config services/core/SenderReceiverAgent_RaspberryA/
vctl start senderreceiveragent-0.1
vctl status
cat volttron.log | grep ERROR
