from pathlib import Path

from nicegui import app as nicegui_app, ui
from pages.config_page import build_config_page
from pages.custom_sub_pages import custom_sub_pages
from pages.home_page import build_home_page
from pages.sources_page import build_sources_page
from src.app_state import AppState
from src.theme import apply_theme

ASSETS_DIR = Path(__file__).resolve().parent / 'assets'
LOGO_CANDIDATES = ('logo.svg', 'logo.png', 'logo.jpg', 'logo.jpeg', 'logo.webp')

state = AppState()
apply_theme()
nicegui_app.add_static_files('/assets', ASSETS_DIR)


def get_logo_src() -> str | None:
    for filename in LOGO_CANDIDATES:
        if (ASSETS_DIR / filename).exists():
            return f'/assets/{filename}'
    return None

@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    logo_src = get_logo_src()

    with ui.header().classes('mv-topbar'):
        with ui.row().classes('mv-app-shell w-full items-center gap-2 py-3'):
            with ui.row().classes('mv-brand-group items-center gap-3').on('click', lambda: ui.navigate.to('/')):
                if logo_src:
                    ui.image(logo_src).classes('mv-brand-logo')
                else:
                    with ui.element('div').classes('mv-logo-placeholder'):
                        ui.label('Logo').classes('mv-logo-placeholder-text')
                ui.label('MV Labels').classes('text-lg font-black tracking-wide text-white')
            ui.button('Sources', on_click=lambda: ui.navigate.to('/sources')).props('flat no-caps').classes('mv-nav-btn')
            ui.button('Configuration', on_click=lambda: ui.navigate.to('/config')).props('flat no-caps').classes('mv-nav-btn')
            ui.space()
            ui.label('Studio control').classes('mv-badge')

    with ui.column().classes('mv-app-shell mv-panel w-full gap-6'):
        custom_sub_pages({
            '/': home_page,
            '/sources': sources_page,
            '/config': config_page,
        }).classes('w-full')

def home_page():
    build_home_page(state)

@ui.page('/sources')
def sources_page():
    build_sources_page(state)

@ui.page('/config')
def config_page():
    build_config_page(state)

def app():
    try:
        if not state.config.validate_config():
            raise Exception("Invalid configuration. Please check the config file.")

        if not state.atem.connect():
            raise Exception(f"Failed to connect to ATEM switcher at {state.atem.host}:{state.atem.port}. Please check connection settings.")
        else:
            ui.run(storage_secret="hi", title='Multiview Labels', dark=True, reload=True, show=False, favicon=get_logo_src())

    except KeyboardInterrupt:
        state.atem.disconnect()
        print("\nExiting on keyboard interrupt.")

if __name__ in {'__main__', '__mp_main__'}:
    app()
