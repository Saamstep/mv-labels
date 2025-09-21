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
    with ui.header().classes('items-center bg-black'):
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Configuration', on_click=lambda: ui.navigate.to('/config')).props('flat')
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

def home():
    operator_name = {'value': ''}
    def on_input_change(e):
        operator_name['value'] = e.value
    ui.input(label='Camera Operator Name', on_change=on_input_change)

    with ui.dropdown_button('Camera', auto_close=True):
        ui.item('Input 1', on_click=lambda: handle_operator_name(operator_name['value'], 1))
        ui.item('Input 2', on_click=lambda: handle_operator_name(operator_name['value'], 2))

def main():
    try:
        # ui.run(storage_secret="hi", title='Multiview Labels', dark=True, reload=False)
        atem.connect()
        id = 1
        name = "Nick"
        print(f"Setting operator name to: {name} for input {id}")
        status_msg = labels.assign_camera_operator(id, name)
        print(status_msg)

        id = 2
        name = "Tristan"
        print(f"Setting operator name to: {name} for input {id}")
        status_msg = labels.assign_camera_operator(id, name)
        print(status_msg)
        atem.disconnect()
    except KeyboardInterrupt:
        print("\nExiting on keyboard interrupt.")

if __name__ == '__main__':
    main()

