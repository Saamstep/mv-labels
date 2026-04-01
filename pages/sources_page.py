from nicegui import ui

from src.app_state import AppState


def build_sources_page(state: AppState):
    config = state.config.get_config()
    available_sources = []
    rows = []
    next_row_id = {'value': 0}

    def get_available_sources() -> list[str]:
        try:
            sources = [str(source) for source in state.atem.get_all_video_sources()]
            return sources
        except Exception:
            return [key for key, _ in config.items('input-mapping')]

    def get_next_source_id() -> str | None:
        used_sources = {row['source_id'] for row in rows if row['source_id']}
        for source_id in available_sources:
            if source_id not in used_sources:
                return source_id
        return None

    def prefill_new_source(source_id: str | None) -> str:
        if not source_id:
            return ''
        normalized_source = source_id.strip()
        lowered_source = normalized_source.lower()
        digits = ''.join(character for character in normalized_source if character.isdigit())

        if lowered_source.startswith('input'):
            return f'Camera {digits}' if digits else 'Camera'

        if lowered_source.startswith('auxilary'):
            return f'Out {digits}' if digits else 'Out'

        return normalized_source

    def add_row() -> None:
        source_id = get_next_source_id()
        rows.append({
            'id': next_row_id['value'],
            'original_key': None,
            'source_id': source_id,
            'friendly_name': prefill_new_source(source_id),
        })
        next_row_id['value'] += 1
        render_rows.refresh()

    def remove_row(row_id: int) -> None:
        rows[:] = [row for row in rows if row['id'] != row_id]
        render_rows.refresh()

    def update_row_source(row: dict, source_id: str | None) -> None:
        row['source_id'] = source_id
        row['friendly_name'] = prefill_new_source(source_id)
        render_rows.refresh()

    def save_sources():
        prefix_values = dict(config.items('labels.prefix'))
        suffix_values = dict(config.items('labels.suffix'))
        new_mapping = {}
        new_prefix = {}
        new_suffix = {}

        for row in rows:
            source_id = '' if row['source_id'] is None else str(row['source_id'])
            friendly_name = '' if row['friendly_name'] is None else str(row['friendly_name']).strip()

            if not source_id:
                ui.notify('Each row needs a source.', type='negative')
                return

            if not friendly_name:
                ui.notify('Each row needs a friendly name.', type='negative')
                return

            if source_id in new_mapping:
                ui.notify(f'Duplicate source selected: {source_id}.', type='negative')
                return

            old_key = row['original_key']
            new_mapping[source_id] = friendly_name
            new_prefix[source_id] = prefix_values.get(old_key or source_id, '')
            new_suffix[source_id] = suffix_values.get(old_key or source_id, '')

        config['input-mapping'].clear()
        config['labels.prefix'].clear()
        config['labels.suffix'].clear()

        for source_id, friendly_name in new_mapping.items():
            state.config.set_value('input-mapping', source_id, friendly_name)
            state.config.set_value('labels.prefix', source_id, new_prefix[source_id])
            state.config.set_value('labels.suffix', source_id, new_suffix[source_id])

        state.config.save()
        ui.notify('Sources saved.', type='positive')

    @ui.refreshable
    def render_rows() -> None:
        with ui.element('div').classes('mv-config-table w-full'):
            with ui.row().classes('mv-config-table-head w-full items-center gap-4'):
                ui.label('Source').classes('mv-config-table-source')
                ui.label('Friendly Name').classes('mv-config-table-column')
                ui.label('').classes('mv-config-table-actions')

            for row in rows:
                with ui.row().classes('mv-config-table-row w-full items-center gap-4'):
                    ui.select(
                        options=available_sources,
                        value=row['source_id'],
                        with_input=True,
                        on_change=lambda e, row=row: update_row_source(row, e.value),
                    ).classes('mv-config-table-source')
                    ui.input(
                        value=row['friendly_name'],
                        on_change=lambda e, row=row: row.__setitem__('friendly_name', e.value),
                    ).classes('mv-config-table-column')
                    ui.button(
                        icon='delete',
                        on_click=lambda row_id=row['id']: remove_row(row_id),
                    ).props('flat round color=negative').classes('mv-row-action')

    available_sources = get_available_sources()
    for key, value in config.items('input-mapping'):
        rows.append({
            'id': next_row_id['value'],
            'original_key': key,
            'source_id': key,
            'friendly_name': value,
        })
        next_row_id['value'] += 1

    with ui.column().classes('w-full max-w-5xl gap-4'):
        ui.label('Sources').classes('mv-page-title')
        ui.label('Update both the source and the friendly name used throughout the app.').classes('mv-subtitle text-sm')

        with ui.card().classes('w-full self-start lg:col-span-2'):
            with ui.row().classes('w-full items-center justify-between gap-4'):
                with ui.column().classes('gap-1'):
                    ui.label('Input Mapping').classes('mv-section-title')
                    ui.label('Choose the ATEM source for each row, then assign the friendly name you want to see elsewhere in the app.').classes('mv-subtitle text-sm')
                ui.button('Add Source', icon='add', on_click=add_row).props('color=primary unelevated no-caps').classes('mv-primary-btn')

            render_rows()

        ui.button('Save Sources', on_click=save_sources).props('color=primary unelevated no-caps').classes('mv-primary-btn self-start')
