from nicegui import ui
from inventory_control.models import Products, Operations
from inventory_control.tools import ToDecimal

def item_entry():
    operation = Operations.PURCHASE.value
    container = ui.column().classes("w-full mt-10 p-10 items-center")

    with container:
        def total_calculation():
            try:
                total_calulated =  int(purchased_quantity.value) * ToDecimal(unit_price.value)
            except ValueError, TypeError:
                total_calulated = 0

            total.text = f"Total: {total_calulated} €"

        ui.label("Item Entry").classes("text-4xl mb-8 text-blue-600")
        with ui.row().classes("w-full justify-center"):
            sub_container_1 = ui.column().classes("w-96 border-r-1")
            sub_container_2 = ui.column().classes("w-96 items-center")

            with sub_container_1:
                product = ui.select(options=[ product.value for product in Products ], label="Select product").classes("w-40")

                purchased_quantity = ui.number(label="Quantity", min=0, max=999, format="%.0f").on("keyup", handler=total_calculation).props("type=number").classes("w-40")

                unit_price = ui.number(label="Price", min=0, max=999, format="%.2f").on("keyup", handler=total_calculation).classes("w-40")

            with sub_container_2:
                total = ui.label(text=f"Total: {0:,.2f} €").classes("text-4xl text-blue-700")

            with ui.row().classes("w-full mt-12 justify-center"):
                btn_save = ui.button(text="Save").props("color=blue").classes("w-30")
                btn_cancel = ui.button(text="Cancel").props("color=red").classes("w-30")

if __name__ in {"__main__", "__mp_main__"}:
    item_entry()
    ui.run()