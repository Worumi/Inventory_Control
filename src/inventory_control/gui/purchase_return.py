from nicegui import ui
from inventory_control.tools import ToDecimal, inventory_report
from inventory_control.db_models import Operations, ProductList, Products
import pandas as pd
from inventory_control.db_models import purchase_return

class PurchaseReturnForm:
    def __init__(self):
        container = ui.column().classes("w-full justify-center items-center p-10")
        with container:
            with ui.row().classes("mb-5"):
                with ui.column().classes("columns-4"):
                    self.selected_product_input = ui.select(label="Select product", options= [product.value for product in Products ]).classes("w-40")
                    ui.button(text="Load information").on_click(callback=self.showTable)

                with ui.column().classes("mx-20 columns-4"):
                    self.operation_id_input = ui.number(label="Operation ID", min=1)
                    self.quantity_input = ui.number(label="Quantity to return", min=1).on(type="keyup", handler=self.calculate_total)
                    ui.button(text="Return", on_click=self.save)

                with ui.column().classes("columns-4"):
                    ui.label(text="Total").classes("text-4xl")
                    self.total_returned = ui.label(text="0.00").classes("text-4xl w-1 max-w-3")

            self.table_container = ui.column().classes("w-2/3") 


    def get_information(self) -> pd.Dataframe:
        df = inventory_report(self.selected_product_input.value)
        df = df.loc[df["operation"] == "Purchase"]
        df = df.drop(columns=["related_id"])
        return df

    def get_price(self, id) -> float:
        data = self.get_information()
        try:
            price = data.loc[data["id_operation"] == id, "price"].item()
        except ValueError:
            ui.notify("Operation ID not found", type="negative", position="top")
            return 0
        return price

    def calculate_total(self):
        try:
            self.operation_id = int(self.operation_id_input.value)
            self.quantity = int(self.quantity_input.value)
            self.price = self.get_price(self.operation_id)
            self.total_calculated = self.quantity * self.price
            self.total_returned.text = f"{self.total_calculated:,.2f}"
            return self.total_calculated
        except TypeError:
            ui.notify("Invalid quantity", type="negative", position="top")
            raise "Invalid quantity"

    def showTable(self):
        # Validar que exista una opción seleccionada
        if not self.selected_product_input.value:
            ui.notify("Please, select a product.", type="warning", position="top")
            return

        # Limpiar el contenido previo del contenedor
        self.table_container.clear()

        # Obtener el DataFrame con la opción seleccionada
        df = self.get_information()

        # Dibujar la tabla dentro del contenedor
        with self.table_container:
            ui.table.from_pandas(df).classes("w-full").props('pagination="{rowsPerPage: 0}" virtual-scroll')

    def save(self):
        if self.calculate_total():
            purchase_return(self.operation_id, self.quantity)
            ui.notify("Purchase return saved successfully.", type="positive", position="top")
            del self.quantity
            del self.price
            del self.operation_id
            self.operation_id_input.value = None
            self.selected_product_input.value = None
            self.quantity_input.value = None

if __name__ in {"__main__", "__mp_main__"}:
    gui = PurchaseReturnForm()
    ui.run()