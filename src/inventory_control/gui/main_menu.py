from nicegui import ui

def menu():
    with ui.button(text="Actions", icon='menu'):
        with ui.menu():
            ui.menu_item('Purchase Product')
            ui.menu_item('Deliver Product')
            with ui.menu_item('Returning Product', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    ui.menu_item('Purchase Return')
                    ui.menu_item('Internal Return')

if __name__ in {"__main__", "__mp_main__"}:
    menu()
    ui.run()