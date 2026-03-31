from nicegui import ui

from src.app_state import AppState


def build_home_page(state: AppState):
    operator_name = {'value': ''}

    def on_input_change(e):
        operator_name['value'] = e.value

    def handle_operator_name(input_id: int):
        if not operator_name['value'].strip():
            ui.notify('Enter an operator name first.', type='warning')
            return

        status_msg = state.labels.assign_camera_operator(input_id, operator_name['value'])
        ui.notify(status_msg)
        operator_name['value'] = ''
        operator_input.set_value('')

    with ui.column().classes('w-full max-w-5xl gap-4'):
        ui.label('Multiview Labels').classes('mv-page-title')
        ui.label('Override an operator name and send it to any configured source.').classes('mv-subtitle text-sm')

        with ui.card().classes('w-full max-w-2xl'):
            ui.label('Override Operator Name').classes('mv-section-title')
            ui.label('Type the operator name, then pick the camera source to update.').classes('mv-subtitle text-sm')

            operator_input = ui.input(
                label='Camera Operator Name',
                placeholder='Enter operator name',
                on_change=on_input_change,
            ).classes('w-full')

            with ui.row().classes('w-full items-center gap-3'):
                with ui.dropdown_button('Select Source', auto_close=True).props('unelevated no-caps color=primary').classes('mv-primary-btn'):
                    for key, value in state.config.get_camera_mapping():
                        input_id = state.config.get_input_id(key)
                        ui.item(value, on_click=lambda id=input_id: handle_operator_name(id))

                ui.label(f'{len(state.config.get_camera_mapping())} sources available').classes('mv-muted text-sm')
