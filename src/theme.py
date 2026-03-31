from nicegui import app, ui

PRIMARY_COLOR = '#2B738B'
PRIMARY_DARK = '#1F5668'
PRIMARY_LIGHT = '#8EB9C7'
SURFACE_COLOR = '#122027'
SURFACE_ELEVATED = '#162A33'
TEXT_MUTED = '#8FAEB8'

_THEME_APPLIED = False


def apply_theme() -> None:
    global _THEME_APPLIED
    if _THEME_APPLIED:
        return

    app.colors(
        primary=PRIMARY_COLOR,
        secondary=PRIMARY_DARK,
        accent=PRIMARY_LIGHT,
        dark='#091217',
        positive='#3A936E',
        negative='#C56161',
        warning='#D2A34F',
    )

    ui.add_head_html(f'<meta name="theme-color" content="{PRIMARY_COLOR}">', shared=True)
    ui.add_css(f'''
        :root {{
            --mv-primary: {PRIMARY_COLOR};
            --mv-primary-dark: {PRIMARY_DARK};
            --mv-primary-light: {PRIMARY_LIGHT};
            --mv-surface: {SURFACE_COLOR};
            --mv-surface-elevated: {SURFACE_ELEVATED};
            --mv-border: rgba(142, 185, 199, 0.18);
            --mv-text: #F3FAFC;
            --mv-text-muted: {TEXT_MUTED};
            --mv-shadow: 0 18px 48px rgba(3, 10, 14, 0.28);
            --mv-input-pad-x: 0.9rem;
        }}

        body {{
            background:
                radial-gradient(circle at top left, rgba(43, 115, 139, 0.24), transparent 32%),
                radial-gradient(circle at top right, rgba(142, 185, 199, 0.12), transparent 26%),
                linear-gradient(180deg, #081116 0%, #0D171C 100%);
            color: var(--mv-text);
            font-family: Helvetica, Arial, sans-serif;
        }}

        .nicegui-content {{
            color: var(--mv-text);
        }}

        .mv-app-shell {{
            width: min(1120px, calc(100vw - 2rem));
            margin: 0 auto;
        }}

        .mv-topbar {{
            background: linear-gradient(135deg, rgba(17, 38, 47, 0.94), rgba(24, 59, 72, 0.84));
            border-bottom: 1px solid rgba(142, 185, 199, 0.16);
            box-shadow: var(--mv-shadow);
            backdrop-filter: blur(14px);
        }}

        .mv-panel {{
            padding: 1.25rem 0 2rem;
        }}

        .mv-page-title {{
            font-size: clamp(1.85rem, 1.3rem + 1.2vw, 2.6rem);
            font-weight: 800;
            letter-spacing: 0.01em;
            color: var(--mv-text);
            line-height: 1.05;
        }}

        .mv-section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--mv-text);
            letter-spacing: 0.01em;
        }}

        .mv-subtitle,
        .mv-muted {{
            color: var(--mv-text-muted);
        }}

        .mv-form-label {{
            padding: 0.6rem 0.85rem 0.6rem 0;
            line-height: 1.2;
        }}

        .mv-config-table {{
            margin-top: 1rem;
            border-top: 1px solid rgba(142, 185, 199, 0.14);
        }}

        .mv-config-table-head {{
            padding: 0.8rem 0 0.7rem;
            color: var(--mv-text-muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .mv-config-table-row {{
            padding: 0.9rem 0;
            border-top: 1px solid rgba(142, 185, 199, 0.1);
        }}

        .mv-config-table-source {{
            flex: 1 1 220px;
            min-width: 180px;
        }}

        .mv-config-table-column {{
            flex: 1 1 220px;
            min-width: 180px;
        }}

        .mv-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(43, 115, 139, 0.16);
            border: 1px solid rgba(142, 185, 199, 0.18);
            color: #D7EDF4;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .mv-card.q-card {{
            background: linear-gradient(180deg, rgba(18, 32, 39, 0.95), rgba(22, 42, 51, 0.92));
            border: 1px solid var(--mv-border);
            border-radius: 20px;
            box-shadow: var(--mv-shadow);
            backdrop-filter: blur(10px);
        }}

        .mv-card.q-card .q-card__section,
        .mv-card.q-card {{
            color: var(--mv-text);
        }}

        .q-btn {{
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.01em;
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }}

        .q-btn:hover {{
            transform: translateY(-1px);
        }}

        .mv-primary-btn.q-btn,
        .mv-primary-btn .q-btn {{
            background: linear-gradient(135deg, var(--mv-primary), #3C88A2);
            color: #F8FCFD;
            box-shadow: 0 12px 28px rgba(43, 115, 139, 0.28);
        }}

        .mv-nav-btn.q-btn {{
            color: #EAF7FB;
            border: 1px solid transparent;
            border-radius: 999px;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }}

        .mv-brand-group {{
            cursor: pointer;
            border-radius: 12px;
            padding: 0.2rem 0.35rem 0.2rem 0;
            transition: background 0.18s ease;
        }}

        .mv-brand-group:hover,
        .mv-brand-group:focus-within {{
            background: rgba(142, 185, 199, 0.08);
        }}

        .mv-brand-logo,
        .mv-logo-placeholder {{
            width: 40px;
            height: 40px;
            flex: 0 0 40px;
            border-radius: 8px;
        }}

        .mv-brand-logo {{
            object-fit: contain;
        }}

        .mv-logo-placeholder {{
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(43, 115, 139, 0.22), rgba(142, 185, 199, 0.12));
            border: 1px dashed rgba(142, 185, 199, 0.3);
        }}

        .mv-logo-placeholder-text {{
            color: #D7EDF4;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .mv-nav-btn.q-btn:hover,
        .mv-nav-btn.q-btn:focus-visible {{
            background: rgba(142, 185, 199, 0.12);
            border-color: rgba(142, 185, 199, 0.18);
        }}

        .mv-input .q-field__control,
        .mv-input .q-field__marginal {{
            color: var(--mv-text);
        }}

        .mv-input .q-field__control {{
            background: rgba(9, 18, 23, 0.68);
            border-radius: 0;
            border: 1px solid rgba(142, 185, 199, 0.12);
            box-shadow: inset 0 0 0 1px transparent;
            transition: box-shadow 0.18s ease, border-color 0.18s ease;
        }}

        .mv-input .q-field__native,
        .mv-input input,
        .mv-input textarea {{
            padding-left: var(--mv-input-pad-x);
            padding-right: var(--mv-input-pad-x);
        }}

        .mv-input .q-field__label {{
            left: var(--mv-input-pad-x);
        }}

        .mv-input.q-field--focused .q-field__control {{
            border-color: rgba(142, 185, 199, 0.28);
            box-shadow: inset 0 0 0 1px rgba(43, 115, 139, 0.7);
        }}

        .mv-input input,
        .mv-input textarea,
        .mv-input .q-field__native,
        .mv-input .q-field__prefix,
        .mv-input .q-field__suffix,
        .mv-input .q-field__label,
        .mv-input .q-field__append,
        .mv-input .q-field__prepend {{
            color: var(--mv-text);
        }}

        .mv-input.q-field--float .q-field__label,
        .mv-input .q-field__label {{
            color: var(--mv-text-muted);
        }}

        .mv-input .q-field__bottom,
        .mv-input .q-field__messages,
        .mv-input .q-field__counter {{
            color: var(--mv-text-muted);
        }}

        .q-toggle__track {{
            opacity: 0.32;
        }}

        .q-menu,
        .q-dialog__inner > div,
        .q-list {{
            background: var(--mv-surface-elevated);
            color: var(--mv-text);
        }}

        .q-item.q-manual-focusable--focused,
        .q-item:hover {{
            background: rgba(43, 115, 139, 0.14);
        }}

        .q-notification {{
            background: rgba(16, 31, 38, 0.94);
            color: var(--mv-text);
            border: 1px solid var(--mv-border);
            border-radius: 14px;
            box-shadow: var(--mv-shadow);
        }}
    ''', shared=True)

    ui.card.default_classes('mv-card')
    ui.input.default_classes('mv-input')
    ui.number.default_classes('mv-input')

    _THEME_APPLIED = True
