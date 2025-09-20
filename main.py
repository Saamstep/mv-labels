from nicegui import ui
from src.config_manager import ConfigManager

config = ConfigManager()

@ui.page('/')
def main_page():
    with ui.header().classes('items-center bg-blue-100'):
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Configuration', on_click=lambda: ui.navigate.to('/config')).props('flat')
        ui.space()
    home()

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

def home():
    ui.markdown('''
        This example shows inheritance from `ui.sub_pages` for decorator-based route protection and a custom 404 page.

        **Try it:** Navigate to "Configuration" for config.
    ''')

ui.run(title='Multiview Labels', dark=True, reload=True)


