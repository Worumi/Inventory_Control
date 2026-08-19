def ToDecimal(value: str | float, digits: int = 2):
    import decimal
    return decimal.Decimal(value).quantize(decimal.Decimal(f"0.{"0"*digits}"))

def get_inventory_data(product: str):
    import pandas as pd
    from inventory_control.db_models import engine
    
    df = pd.read_sql_query(f"SELECT * FROM productlist WHERE product_name = '{product}'", engine)

    for index in df.index:
        if index > 0:
            current_index = index
            prior_index = index - 1

            prior_units_available = df.loc[df.index == prior_index, "units_available"].item()
            current_units_available = df.loc[df.index == current_index, "quantity"].item()

            new_units_available = int(current_units_available) + int(prior_units_available)

            prior_inventory_value = df.loc[df.index == prior_index, "inventory_value"].item()
            current_total = df.loc[df.index == current_index, "total"].item()

            new_inventory_value = float(current_total) + float(prior_inventory_value)

            new_unit_cost = new_inventory_value / new_units_available

            df.loc[df.index == current_index, "units_available"] = new_units_available
            df.loc[df.index == current_index, "inventory_value"] = round(new_inventory_value, 2)
            df.loc[df.index == current_index, "unit_cost"] = round(new_unit_cost, 2)
            
        else:
            df.loc[df.index == 0, "units_available"] = int(df.loc[df.index == 0, "quantity"].item())
            df.loc[df.index == 0, "inventory_value"] = float(df.loc[df.index == 0, "total"].item())
            df.loc[df.index == 0, "unit_cost"] = float(df.loc[df.index == 0, "price"].item())

    return df