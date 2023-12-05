# Sender-Receiver Agent on Raspberry A

import datetime
import time
import logging
import gevent 
from array import array
from volttron.platform.vip.agent import Agent, Core, PubSub
from volttron.platform.keystore import KnownHostsStore
from volttron.platform.messaging.health import STATUS_GOOD, STATUS_BAD
from volttron.platform.agent import utils

DEFAULT_MESSAGE = 'Listener Message'
DEFAULT_AGENTID = "listener"
DEFAULT_HEARTBEAT_PERIOD = 5

utils.setup_logging()
_log = logging.getLogger(__name__)

__version__ = '0.1'

class SenderAgent(Agent):
    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        config = utils.load_config(config_path)
        self._agent_id = config.get('agentid', DEFAULT_AGENTID)
        self._message = config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = config.get('heartbeat_period',
                                            DEFAULT_HEARTBEAT_PERIOD)
        
        # This part of config is not working and casue some errors
        #---------------------------------------------------------
        destination_serverkey = None
        # Juste pour tester, le try catch sera supprimé par la suite
        try:
            destination_vip = config.pop('destination-vip')
            _log.error("destination VIP is : ({})".format(destination_vip))
        except KeyError:
            destination_vip = None
            _log.error('destination address is uninitialized ZEUBI')

        try:
            destination_address = config.pop('destination-address')
        except KeyError:
            destination_address = None

        if destination_vip:
            hosts = KnownHostsStore()
            destination_serverkey = hosts.serverkey(destination_vip)
            _log.error("destination serverkey is : ({})".format(destination_serverkey))
        if destination_serverkey is None:
            _log.error("Destination serverkey not found in known hosts file, using config")
            destination_serverkey = config.pop('destination-serverkey')
            _log.error("destination serverkey is : ({})".format(destination_serverkey))
        else:
            config.pop('destination-serverkey', None)
        try:
            if destination_address:
                address = destination_address
            elif destination_vip:
                address = destination_vip

            value = self.core.connect_remote_platform(address, serverkey=destination_serverkey)
        except gevent.Timeout:
            _log.error("Couldn't connect to address. gevent timeout: ({})".format(address))
            self.vip.health.set_status(STATUS_BAD, "Timeout in setup of agent")
        except Exception as ex:
            _log.error(ex.args)
            self.vip.health.set_status(STATUS_BAD, "Error message: {}".format(ex))
        else:
            if isinstance(value, Agent):
                self._target_platform = value

                self.vip.health.set_status(
                    STATUS_GOOD, "Connected to address ({})".format(address))
            else:
                _log.error("Couldn't connect to address. Got Return value that is not Agent: ({})".format(address))
                self.vip.health.set_status(STATUS_BAD, "Invalid agent detected.")
        #---------------------------------------------------------   
        
        runtime_limit = int(config.get('runtime_limit', 0))
        if runtime_limit and runtime_limit > 0:
            stop_time = datetime.datetime.now() + datetime.timedelta(seconds=runtime_limit)
            _log.info('Listener agent will stop at {}'.format(stop_time))
            self.core.schedule(stop_time, self.core.stop)
        else:
            _log.info('No valid runtime_limit configured; listener agent will run until manually stopped')

        try:
            self._heartbeat_period = int(self._heartbeat_period)
        except:
            _log.warning('Invalid heartbeat period specified setting to default')
            self._heartbeat_period = DEFAULT_HEARTBEAT_PERIOD
        log_level = config.get('log-level', 'INFO')
        if log_level == 'ERROR':
            self._logfn = _log.error
        elif log_level == 'WARN':
            self._logfn = _log.warn
        elif log_level == 'DEBUG':
            self._logfn = _log.debug
        else:
            self._logfn = _log.info

    start_time = None
    @Core.receiver('onstart')
    def onstart(self, sender, **kwargs):
        # Logic to send data to Raspberry B
        #data_to_send = "Hello from Raspberry A!"
        data_to_send = bytes([0xFF]*1000)
        data_to_send_100 = data_to_send.hex()
        global start_time
        start_time = time.time_ns()
        _log.error("time start is : ({})".format(start_time))
        
        self.vip.pubsub.publish('pubsub', "devices", message=data_to_send_100)
        self.vip.health.set_status(STATUS_GOOD, "Sender agent is runnig good on raspb A")

    #@Core.receiver('on_receive')
    @PubSub.subscribe('pubsub', "analysis", all_platforms=True)
    def on_receive(self, peer, sender, bus, topic, headers, message):
        # Callback to handle received data from Raspberry B
        print(f"Received data on Raspberry A: {message}")
        end_time = time.time_ns()
        time_difference = ((end_time - start_time)/1000)/2
        _log.error("time reception is : ({})".format(end_time))
        _log.error("time difference in microseconds is : ({})".format(time_difference))
        self.vip.health.set_status(STATUS_GOOD, "Receiver agent is runnig good on raspb A")

# Entry point for the script
def main():
    try:
        utils.vip_main(SenderAgent, version=__version__)
    except Exception as e:
        print(f"Unhandled excpetion: {e}")
        _log.exception('unhandled exception')

if __name__ == '__main__':
    main()
