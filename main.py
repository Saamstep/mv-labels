from time import sleep
from nicegui import ui
from pages.custom_sub_pages import custom_sub_pages, protected
from src.config_manager import ConfigManager
from src.ATEM import PyAtemMax
from src.LabelController import LabelController
import os

config = ConfigManager()
[host, port] = config.get_connection_information()
atem = PyAtemMax(host, port)
labels = LabelController(atem, config)

@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    with ui.header().classes('items-center').style('text-color: white;'):
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat color=white')
        ui.button('Configuration', on_click=lambda: ui.navigate.to('/config')).props('flat color=white')
        ui.space()

    custom_sub_pages({
        '/': home,
        '/config': config_page,
    }).classes('flex-grow p-4')

@ui.page('/config')
def config_page():
    ui.label('Multiview Labels - Configuration')
    columns = [
        {'name': 'key', 'label': 'Key', 'field': 'key', 'required': True, 'align': 'left'},
        {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left'},
    ]
    for section in config.get_config().sections():
        ui.label(f'Section: {section}').classes('text-lg font-bold mt-4')
        rows = []
        for key, value in config.get_config().items(section):
            rows.append({'key': key, 'value': value})
        ui.table(columns=columns, rows=rows, row_key='key').classes('w-full')

def handle_operator_name(name: str, id: int):
    print(f"Setting operator name to: {name} for input {id}")
    status_msg = labels.assign_camera_operator(id, name)
    ui.notify(status_msg)
    if 'operator_input' in globals():
        operator_input.set_value('')

def home():
    global operator_input
    operator_name = {'value': ''}
    def on_input_change(e):
        operator_name['value'] = e.value
    operator_input = ui.input(label='Camera Operator Name', on_change=on_input_change)

    with ui.dropdown_button('Select Camera', auto_close=True):
        for key, value in config.get_camera_mapping():
            input_id = config.get_input_id(key)
            ui.item(value, on_click=lambda id=input_id: handle_operator_name(operator_name['value'], id))

def app():
    try:
        if not config.validate_config():
            raise Exception("Invalid configuration. Please check the config file.")

        if not atem.connect():
            raise Exception(f"Failed to connect to ATEM switcher at {atem.host}:{atem.port}. Please check connection settings.")
        else:
            ui.run(storage_secret="hi", title='Multiview Labels', dark=True, reload=False)

    except KeyboardInterrupt:
        atem.disconnect()
        print("\nExiting on keyboard interrupt.")

if __name__ == '__main__':
    app()

