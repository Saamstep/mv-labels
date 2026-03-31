from nicegui import ui

from src.app_state import AppState


def build_sources_page(state: AppState):
    controls = {}

    def save_sources():
        for key, control in controls.items():
            value = '' if control.value is None else str(control.value)
            state.config.set_value('input-mapping', key, value)

        state.config.save()
        ui.notify('Sources saved.', type='positive')

    with ui.column().classes('w-full max-w-5xl gap-4'):
        ui.label('Sources').classes('mv-page-title')
        ui.label('Update the friendly names used for each ATEM input.').classes('mv-subtitle text-sm')

        with ui.card().classes('w-full'):
            ui.label('Input Mapping').classes('mv-section-title')

            for key, value in state.config.get_config().items('input-mapping'):
                with ui.row().classes('w-full items-center gap-4'):
                    ui.label(key).classes('w-32 mv-muted mv-form-label')
                    controls[key] = ui.input(value=value).classes('flex-grow')

        ui.button('Save Sources', on_click=save_sources).props('color=primary unelevated no-caps').classes('mv-primary-btn self-start')
