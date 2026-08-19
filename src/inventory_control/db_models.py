from decimal import Decimal
from sqlmodel import Field, SQLModel, Session, create_engine, select, or_
from enum import Enum
from inventory_control.tools import ToDecimal, get_inventory_data
from pathlib import Path

class Operations(str, Enum):
    """
    It represent the avalaible type of operation.
    
    ### Types:
        PURCHASE = "Purchase"
        PURCHASE_RETURN = "Purchase Return"
        COST_RETURN = "Cost Return"
        DELIVERY = "Delivery"
    """
    PURCHASE = "Purchase"
    PURCHASE_RETURN = "Purchase Return"
    COST_RETURN = "Cost Return"
    DELIVERY = "Delivery"

class Products(str, Enum):
    PRODUCT_A = "Product A"
    PRODUCT_B = "Product B"
    PRODUCT_C = "Product C"
    PRODUCT_D = "Product D"

class ProductList(SQLModel, table=True):
    """
    It is the model to create and describe a table of a Product List

    ### Args
        **id_product**: int | None
        **product_name**: str
        **quantity**: int
        **price**: Decimal
        **total**: Decimal
        **operation**: str
        **related_id**: int | None
    """
    id_operation: int | None = Field(default=None, primary_key=True)
    product_name: str
    quantity: int
    price: Decimal
    total: Decimal
    operation: str
    related_id: int | None =Field(default=None)

# Connecting Database
ROOT = Path.cwd()
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{ROOT}/{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def purchase_item(product: ProductList):
    with Session(engine) as session:
        session.add(product)
        session.commit()

def deliver_item(product_name: str, quantity_to_deliver: int):
    data = get_inventory_data(product_name)
    unit_cost = data.iloc[-1,-1]
    max_to_deliver = data["quantity"].sum()
    if max_to_deliver >= quantity_to_deliver:
        with Session(engine) as session:
            total = quantity_to_deliver * unit_cost
            product_to_deliver = ProductList(
            product_name = product_name,
            quantity = -quantity_to_deliver,
            price = ToDecimal(unit_cost),
            total = total,
            operation = Operations.DELIVERY.value,
            )

            session.add(product_to_deliver)
            session.commit()

def purchase_return(id: int, quantity_returned: int):
    with Session(engine) as session:
        statement = select(ProductList).where(or_(
            ProductList.id_operation == id,
            ProductList.related_id == id
        ))
        
        results = session.exec(statement)
        products = results.all()
        product_to_record = products[0]

        max_quantity = sum([ product.quantity for product in products ])
        if max_quantity >= quantity_returned:
            total = product_to_record.price * -quantity_returned
            product_to_return = ProductList(
                product_name=product_to_record.product_name,
                quantity=-quantity_returned,
                price=ToDecimal(product_to_record.price),
                total=total,
                operation=Operations.PURCHASE_RETURN.value,
                related_id=product_to_record.id_operation
            )
            session.add(product_to_return)
            session.commit()

def cost_return(id: int, quantity_returned: int):
    with Session(engine) as session:
        statement = select(ProductList).where(or_(
            ProductList.id_operation == id,
            ProductList.related_id == id
        ))
        
        results = session.exec(statement)
        products = results.all()
        product_to_record = products[0]

        max_out = sum([ product.quantity for product in products if product.quantity < 0 ])

        if -max_out > quantity_returned:
            data = get_inventory_data(product_to_record.product_name)
            unit_cost = data.loc[data["id_product"] == id, "unit_cost"].item()
            total = unit_cost * quantity_returned
            product_to_return = ProductList(
                product_name=product_to_record.product_name,
                quantity=quantity_returned,
                price=ToDecimal(unit_cost),
                total=total,
                operation=Operations.COST_RETURN.value,
                related_id=id
            )

            session.add(product_to_return)
            session.commit()

def create_dummies():
    import random
    product_names = [ product.value for product in Products ]
    product_selected = random.choices(product_names, k=20)
    with Session(engine) as session:
        for product in product_selected:
            quantity = random.randint(1, 50)
            price = ToDecimal(random.uniform(10, 18))
            total = price * quantity
            product = ProductList(
                product_name = product,
                quantity = quantity,
                price = price,
                total = total,
                operation = Operations.PURCHASE.value
            )
            session.add(product)
            session.commit()
        

def main():  
    create_db_and_tables()  
    create_dummies()

if __name__ == "__main__":  
    main()  