from nicegui import ui
from inventory_control.db_models import Products, Operations
from inventory_control.tools import ToDecimal
from inventory_control.db_models import purchase_item, ProductList

class ProductEntryForm:
    def __init__(self):
        container = ui.column().classes("w-full mt-10 p-10 items-center")
        with container:
            ui.label("Item Entry").classes("text-4xl mb-8 text-blue-600")
            with ui.row().classes("w-full justify-center"):
                sub_container_1 = ui.column().classes("w-96 border-r-1")
                sub_container_2 = ui.column().classes("w-96 items-center")

                with sub_container_1:
                    self.product = ui.select(options=[ product.value for product in Products ], label="Select product").classes("w-40")

                    self.purchased_quantity = ui.number(label="Quantity", min=0, max=999, format="%.0f").on("keyup", handler=self.total_calculation).props("type=number").classes("w-40")

                    self.unit_price = ui.number(label="Price", min=0, max=999, format="%.2f").on("keyup", handler=self.total_calculation).classes("w-40")

                with sub_container_2:
                    ui.label(text="Total").classes("text-4xl")
                    self.total = ui.label(text=f"{0:,.2f}").classes("text-4xl text-blue-700")

                with ui.row().classes("w-full mt-12 justify-center"):
                    ui.button(text="Save").props("color=blue").classes("w-30").on_click(callback=self.save)
                    ui.button(text="Cancel").props("color=red").classes("w-30").on_click(callback=self.clear)

    def total_calculation(self):
        try:
            self.total_calulated =  int(self.purchased_quantity.value) * ToDecimal(self.unit_price.value)
        except (ValueError, TypeError):
            self.total_calulated = 0
        self.total.text = f"{self.total_calulated:,.2f} €"

    def clear(self):
        self.product.value = ""
        self.purchased_quantity.value = ""
        self.unit_price.value = ""

    def save(self):
        product = ProductList(
            product_name=self.product.value,
            quantity=self.purchased_quantity.value,
            price=self.unit_price.value,
            total=float(self.total_calulated),
            operation=Operations.PURCHASE.value,
        )
        purchase_item(product)


if __name__ in {"__main__", "__mp_main__"}:
    gui = ProductEntryForm()
    ui.run()