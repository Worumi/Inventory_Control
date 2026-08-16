from nicegui import ui
from inventory_control.gui.item_entry import ProductEntryForm
from inventory_control.gui.purchase_return import PurchaseReturnForm


class MainMenu:
    def __init__(self, content_area: ui.column):
        result = ui.column()
        with ui.button(text="Actions", icon='menu'):
            with ui.menu():
                ui.menu_item('Purchase Product', on_click=purchase)
                ui.menu_item('Deliver Product')
                with ui.menu_item('Returning Product', auto_close=False):
                    with ui.item_section().props('side'):
                        ui.icon('keyboard_arrow_right')
                    with ui.menu().props('anchor="top end" self="top start" auto-close'):
                        ui.menu_item('Purchase Return')
                        ui.menu_item('Internal Return')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()