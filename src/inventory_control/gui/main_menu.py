from nicegui import ui

def menu():
    with ui.button(text="Actions", icon='menu'):
        with ui.menu():
            ui.menu_item('Option 1')
            ui.menu_item('Option 2')
            with ui.menu_item('Option 3', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    ui.menu_item('Sub-option 1')
                    ui.menu_item('Sub-option 2')
                    ui.menu_item('Sub-option 3')

if __name__ in {"__main__", "__mp_main__"}:
    menu()
    ui.run()