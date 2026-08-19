from nicegui import ui
from inventory_control.db_models import Products
from inventory_control.tools import get_inventory_data

class InventoryReport:
    def __init__(self):
        with ui.column().classes("w-full ml-40 mt-5 p-10 justify-center"):
            self.product = ui.select(options=[product.value for product in Products], label="Select a Product").classes("w-40")
            ui.button(text="Get Inventory", on_click=self.get_inventory)

        self.container = ui.column().classes("w-full ml-40 justify-center")

    def get_inventory(self):
        self.container.clear()
        with self.container:
            ui.table.from_pandas(get_inventory_data(self.product.value))

if __name__ in {"__main__", "__mp_main__"}:
    gui = InventoryReport()
    ui.run()