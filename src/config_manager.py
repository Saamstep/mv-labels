import configparser
from pathlib import Path

CONFIG_FILE_NAME = 'config.ini'

class ConfigManager:
    def __init__(self):
        # Load or create config file
        self.config = configparser.ConfigParser()
        if(Path(CONFIG_FILE_NAME).is_file()):
            # Load existing config
            self.config.read(CONFIG_FILE_NAME)
        else:
            # Create default config if path does not exist
            self._default_config()
            with open(CONFIG_FILE_NAME, 'w') as configfile:
                self.config.write(configfile)

    def _default_config(self):
        """Create a default config structure
        """
        self.config['atem'] = {
            'host': '0.0.0.0',
            'port': '9910'
        }
        self.config['app-settings'] = {
            'prefix': 'yes',
            'suffix': 'no'
        }
        self.config['labels.prefix'] = {
            'input1': 'C1',
            'input2': 'C2',
            'input3': 'C3',
            'input4': 'C4',
            'input5': 'C5',
            'input6': 'C6',
            'input7': 'C7',
            'input8': 'C8'
        }
        self.config['labels.suffix'] = {
            'input1': 'C200',
            'input2': 'C200',
            'input3': 'C200',
            'input4': 'C200',
            'input5': 'C200',
            'input6': 'C200',
            'input7': 'C200',
            'input8': 'C200'
        }

    def get_config(self):
        return self.config
    
    def _save_config(self):
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            self.config.write(configfile)

    def get_label_prefix(self, key):
        return self.config['labels.prefix'].get(key, "Unknown").replace('"', '')
    
    def get_label_suffix(self, key):
        return self.config['labels.suffix'].get(key, "Unknown").replace('"', '')
    
    def get_config_headers(self):
        return self.config.sections()
    
    def is_prefix_enabled(self):
        return self.config['app-settings'].getboolean('prefix', fallback=True)
    
    def is_suffix_enabled(self):
        return self.config['app-settings'].getboolean('suffix', fallback=False)