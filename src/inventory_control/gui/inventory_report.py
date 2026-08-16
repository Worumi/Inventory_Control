from nicegui import ui
from inventory_control.tools import inventory_report

class InventoryReport:
    def __init__(self):
        container = ui.column()
        with container:
            ui.select()