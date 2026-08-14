from nicegui import ui
from inventory_control.tools import inventory_report
from inventory_control.db_models import Products

class PurchaseReturnForm:
    def __init__(self):
        container = ui.column().classes("w-full justify-center")

        with container:
            self.selected_product = ui.select(label="Select product", options= [product.value for product in Products ]).classes("w-40")

            ui.button(text="Load information").on_click(callback=self.showTable)

            self.table_container = ui.column().classes("w-full") 

    def showTable(self):
        # Validar que exista una opción seleccionada
        if not self.selected_product.value:
            ui.notify("Por favor, selecciona un producto", type="warning")
            return

        # Limpiar el contenido previo del contenedor
        self.table_container.clear()

        # Obtener el DataFrame con la opción seleccionada
        df = inventory_report(self.selected_product.value)

        # Dibujar la tabla dentro del contenedor
        with self.table_container:
            ui.table.from_pandas(df).classes("w-full").props('pagination="{rowsPerPage: 0}" virtual-scroll header-class="sticky top-0 bg-white z-10"')

if __name__ in {"__main__", "__mp_main__"}:
    gui = PurchaseReturnForm()
    ui.run()