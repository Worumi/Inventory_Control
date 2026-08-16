from nicegui import ui
from inventory_control.gui.item_entry import ProductEntryForm
from inventory_control.gui.purchase_return import PurchaseReturnForm


class MainMenu:
    def __init__(self):
        with ui.row().classes("w-full"):
            with ui.column():
                with ui.button(text="Actions", icon='menu'):
                    with ui.menu():
                        ui.menu_item('Purchase Product', on_click=self.add_purchase)
                        ui.menu_item('Deliver Product')
                        with ui.menu_item('Returning Product', auto_close=False):
                            with ui.item_section().props('side'):
                                ui.icon('keyboard_arrow_right')
                            with ui.menu().props('anchor="top end" self="top start" auto-close'):
                                ui.menu_item('Purchase Return', on_click=self.purchase_return)
                                ui.menu_item('Internal Return')
                        ui.separator()
                        ui.menu_item("Inventory Report")

            self.result = ui.column().classes("w-full mt-5")

    def add_purchase(self):
        self.result.clear()
        with self.result:
            ProductEntryForm()

    def purchase_return(self):
        self.result.clear()
        with self.result:
            PurchaseReturnForm()

if __name__ in {"__main__", "__mp_main__"}:
    gui = MainMenu()
    ui.run()