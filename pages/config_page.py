from nicegui import ui

from src.app_state import AppState


def build_config_page(state: AppState):
    controls = {}
    config = state.config.get_config()

    def format_section_title(section: str) -> str:
        if section == 'atem':
            return 'ATEM Connection'
        return section.title().replace('-', ' ')

    def render_standard_section(section: str) -> None:
        with ui.card().classes('w-full self-start'):
            ui.label(format_section_title(section)).classes('mv-section-title')

            for key, value in config.items(section):
                with ui.row().classes('w-full items-center gap-4'):
                    ui.label(key).classes('w-40 mv-muted mv-form-label')

                    if section == 'app-settings':
                        controls[(section, key)] = ui.switch(
                            value=config.getboolean(section, key)
                        ).classes('ml-2')
                    elif section == 'atem' and key == 'port':
                        controls[(section, key)] = ui.number(
                            value=int(value), min=1, step=1, precision=0
                        ).classes('w-48')
                    else:
                        controls[(section, key)] = ui.input(value=value).classes('flex-grow')

    def render_labels_section() -> None:
        prefix_section = 'labels.prefix'
        suffix_section = 'labels.suffix'

        with ui.card().classes('w-full self-start lg:col-span-2'):
            ui.label('Labels').classes('mv-section-title')
            ui.label('Prefix and suffix settings are grouped by source so each label format is easier to scan and edit.').classes('mv-subtitle text-sm')

            with ui.row().classes('w-full items-center gap-6 pt-2'):
                ui.label('Show Prefix').classes('mv-muted mv-form-label')
                controls[('app-settings', 'prefix')] = ui.switch(
                    value=config.getboolean('app-settings', 'prefix')
                )
                ui.label('Show Suffix').classes('mv-muted mv-form-label')
                controls[('app-settings', 'suffix')] = ui.switch(
                    value=config.getboolean('app-settings', 'suffix')
                )

            with ui.element('div').classes('mv-config-table w-full'):
                with ui.row().classes('mv-config-table-head w-full items-center gap-4'):
                    ui.label('Source').classes('mv-config-table-source')
                    ui.label('Prefix').classes('mv-config-table-column')
                    ui.label('Suffix').classes('mv-config-table-column')

                for key, camera_name in state.config.get_camera_mapping():
                    prefix_value = config.get(prefix_section, key, fallback='')
                    suffix_value = config.get(suffix_section, key, fallback='')

                    with ui.row().classes('mv-config-table-row w-full items-center gap-4'):
                        with ui.column().classes('mv-config-table-source gap-0'):
                            ui.label(camera_name).classes('font-medium')
                            ui.label(key).classes('mv-muted text-xs')

                        controls[(prefix_section, key)] = ui.input(
                            value=prefix_value,
                            placeholder='Prefix',
                        ).classes('mv-config-table-column')
                        controls[(suffix_section, key)] = ui.input(
                            value=suffix_value,
                            placeholder='Suffix',
                        ).classes('mv-config-table-column')

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
            for section in config.sections():
                if section in {'input-mapping', 'labels.prefix', 'labels.suffix', 'app-settings'}:
                    continue
                render_standard_section(section)

            render_labels_section()

        ui.button('Save Configuration', on_click=save_configuration).props('color=primary unelevated no-caps').classes('mv-primary-btn self-start')
