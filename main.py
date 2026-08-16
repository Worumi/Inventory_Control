from nicegui import ui
from inventory_control.gui.main_menu import MainMenu

@ui.page('/')
def index():
    content = ui.column().classes('w-full')
    MainMenu(content)

ui.run()