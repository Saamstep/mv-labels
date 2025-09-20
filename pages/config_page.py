from nicegui import ui
from src.config_manager import ConfigManager
config = ConfigManager()

def config_page():
    ui.label('Multiview Labels - Configuration')

columns = [
    {'name': 'key', 'label': 'Key', 'field': 'key', 'required': True, 'align': 'left'},
    {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left'},
]
for section in config.get_config().sections():
    ui.label(f'{section}').classes('text-lg font-bold mt-4')
    rows = []
    for key, value in config.get_config().items(section):
        rows.append({'key': key, 'value': value})
    ui.table(columns=columns, rows=rows, row_key='key').classes('w-full')