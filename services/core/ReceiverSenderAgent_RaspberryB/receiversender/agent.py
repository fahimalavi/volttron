# Receiver-Renvertoir Agent on Raspberry B

import datetime
import logging
from volttron.platform.vip.agent import Agent, Core, PubSub
from volttron.platform.messaging.health import STATUS_GOOD, STATUS_BAD
from volttron.platform.agent import utils

utils.setup_logging()
_log = logging.getLogger(__name__)

__version__ = '0.1'

DEFAULT_MESSAGE = 'Listener Message'
DEFAULT_AGENTID = "listener"
DEFAULT_HEARTBEAT_PERIOD = 5

class ReceiverRenvertoirAgent(Agent):
    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)
        
        runtime_limit = int(self.config.get('runtime_limit', 0))
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
        log_level = self.config.get('log-level', 'INFO')
        if log_level == 'ERROR':
            self._logfn = _log.error
        elif log_level == 'WARN':
            self._logfn = _log.warn
        elif log_level == 'DEBUG':
            self._logfn = _log.debug
        else:
            self._logfn = _log.info

    @PubSub.subscribe('pubsub', "devices")
    def on_receive_data(self, peer, sender, bus, topic, headers, message):
        # Callback to handle received data from Raspberry A
        print(f"Received data on Raspberry B: {message}")

        # Logic to process the received data

        # Logic to send the data back to Raspberry A
        data_to_send_back = "Hello from Raspberry B!"
        self.vip.pubsub.publish('pubsub', "analysis", message=data_to_send_back)
        self.vip.health.set_status(STATUS_GOOD, "ReceiverSender agent is runnig good on raspb B")

# Entry point for the script
def main():
    #receiver_renvertoir_agent = ReceiverRenvertoirAgent(address="tcp://127.0.0.1:22917")
    try:
        utils.vip_main(ReceiverRenvertoirAgent, version=__version__)
    except Exception as e:
        print(e)
        _log.exception('unhandled exception')

if __name__ == '__main__':
    main()
