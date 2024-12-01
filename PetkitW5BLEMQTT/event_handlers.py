import logging
from .utils import Utils
from .parsers import Parsers

class EventHandlers:
    def __init__(self, device, commands, logger, callback=None):
        self.logger = logger
        self.device = device
        self.callback = callback        
        
        # Registry of command values to handler methods
        self.handlers = {
            66: Parsers.device_battery,
            #73: Parsers.device_init,
            86: Parsers.device_synchronization,
            200: Parsers.device_firmware,
            210: Parsers.device_state,
            211: Parsers.device_configuration,
            213: Parsers.device_identifiers,
            230: Parsers.device_status,
        }
        
        # Messages we want to forward
        self.forward_messages = [
            220,
            221, 
            230
        ]

    async def handle_notification(self, sender, message):
        parsed_data = Utils.parse_bytearray(message)
        cmd = parsed_data['cmd']
        self.logger.info(f"Received command {cmd}")
        
        self.logger.debug(f"Parsed data:\n{parsed_data}")
        
        data = None
        
        if cmd in self.handlers:
            handler = self.handlers[cmd]
            data = handler(parsed_data['data'], self.device.alias)
            self.logger.debug(f"Parsed data\n{data}")
            
            # Update config
            if cmd in [86, 200, 213]:
                self.device.info = data

            # Update status
            if cmd in [66, 210, 211, 230]:
                self.device.status = data
                
        if self.callback and cmd in self.forward_messages:
            self.callback(self.device.mac_readable, self.device.status)
        
        return parsed_data