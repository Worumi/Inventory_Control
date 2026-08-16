from nicegui import ui
from inventory_control.tools import ToDecimal, inventory_report
from inventory_control.db_models import Products
import pandas as pd

class PurchaseReturnForm:
    def __init__(self):
        container = ui.column().classes("w-full justify-center")
        with container:
            with ui.row().classes("mx-auto mb-5"):
                with ui.column():
                    self.selected_product = ui.select(label="Select product", options= [product.value for product in Products ]).classes("w-40")
                    ui.button(text="Load information").on_click(callback=self.showTable)

                with ui.column().classes("mx-20"):
                    self.operation_id_input = ui.number(label="Operation ID", min=1, value=2)
                    self.quantity_input = ui.number(label="Quantity to return", min=1, value=1).on(type="keyup", handler=self.calculate_total)
                    ui.button(text="Return")

                with ui.column():
                    ui.label(text="Total").classes("text-4xl")
                    self.total_returned = ui.label(text="").classes("text-4xl")

            self.table_container = ui.column().classes("w-full") 


    def get_information(self) -> pd.Dataframe:
        df = inventory_report(self.selected_product.value)
        df = df.loc[df["operation"] == "Purchase"]
        return df

    def get_price(self, id) -> float:
        data = self.get_information()
        try:
            price = data.loc[data["id_operation"] == id, "price"].item()
        except ValueError:
            return 0
        return price

    def calculate_total(self):
        self.operation_id = int(self.operation_id_input.value)
        self.quantity = int(self.quantity_input.value)
        price = self.get_price(self.operation_id)
        self.total_calculated = self.quantity * price
        self.total_returned.text = self.total_calculated
        # self.total_returned.text = price


    def showTable(self):
        # Validar que exista una opción seleccionada
        if not self.selected_product.value:
            ui.notify("Please, select a product.", type="warning")
            return

        # Limpiar el contenido previo del contenedor
        self.table_container.clear()

        # Obtener el DataFrame con la opción seleccionada
        df = self.get_information()

        # Dibujar la tabla dentro del contenedor
        with self.table_container:
            ui.table.from_pandas(df).classes("w-full").props('pagination="{rowsPerPage: 0}" virtual-scroll header-class="sticky top-0 bg-white z-10"')

if __name__ in {"__main__", "__mp_main__"}:
    gui = PurchaseReturnForm()
    ui.run()