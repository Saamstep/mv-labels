from nicegui import ui

from src.app_state import AppState


def build_config_page(state: AppState):
    controls = {}

    def save_configuration():
        current_host, current_port = state.atem.host, state.atem.port

        for (section, key), control in controls.items():
            value = control.value

            if section == 'app-settings':
                state.config.set_value(section, key, 'yes' if value else 'no')
                continue

            if section == 'atem' and key == 'port':
                if value is None:
                    ui.notify('ATEM port is required.', type='negative')
                    return
                state.config.set_value(section, key, str(int(value)))
                continue

            value = '' if value is None else str(value)
            if section == 'atem' and key == 'host' and not value.strip():
                ui.notify('ATEM host is required.', type='negative')
                return

            state.config.set_value(section, key, value)

        state.config.save()

        new_host, new_port = state.config.get_connection_information()
        if (new_host, new_port) != (current_host, current_port):
            success, message = state.reconnect_atem()
            ui.notify(message, type='positive' if success else 'negative')
            return

        ui.notify('Configuration saved.', type='positive')

    with ui.column().classes('w-full max-w-6xl gap-4'):
        ui.label('Multiview Labels Configuration').classes('mv-page-title')
        ui.label('Changes to prefixes and suffixes apply immediately. Connection changes reconnect the ATEM.').classes('mv-subtitle text-sm')

        with ui.element('div').classes('grid w-full grid-cols-1 gap-4 lg:grid-cols-2'):
            for section in state.config.get_config().sections():
                if section == 'input-mapping':
                    continue

                with ui.card().classes('w-full self-start'):
                    if section != 'atem':
                        ui.label(section.title().replace('-', ' ')).classes('mv-section-title')
                    else:
                        ui.label('ATEM Connection').classes('mv-section-title')

                    for key, value in state.config.get_config().items(section):
                        with ui.row().classes('w-full items-center gap-4'):
                            ui.label(key).classes('w-40 mv-muted mv-form-label')

                            if section == 'app-settings':
                                controls[(section, key)] = ui.switch(value=state.config.get_config().getboolean(section, key)).classes('ml-2')
                            elif section == 'atem' and key == 'port':
                                controls[(section, key)] = ui.number(value=int(value), min=1, step=1, precision=0).classes('w-48')
                            else:
                                controls[(section, key)] = ui.input(value=value).classes('flex-grow')

        ui.button('Save Configuration', on_click=save_configuration).props('color=primary unelevated no-caps').classes('mv-primary-btn self-start')
