import json
from pathlib import Path
from typing import List, Dict

# one way to writing path fo your file
# PRODUCTS_FILE = Path("data","products.json")
# Path(__file__): It give the path to the current python file like this: C:\Users\Shradhey Meshram\OneDrive\Desktop\FastAPI\sheriyans\services\products.py
PRODUCTS_FILE = Path(__file__).parent.parent / "data" / "dummy_data.json"


def load_products() -> List[Dict]:
    if not PRODUCTS_FILE.exists():
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return load_products()


def save_product(products: List[Dict]) -> None:
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


def add_product(product: Dict) -> Dict:
    products = get_all_products()

    if any(p["productID"] == product["productID"] for p in products):
        raise ValueError("productID alreay exists")

    products.append(product)
    save_product(products)
    return product


def remove_product(id: str) -> str:
    products = get_all_products()

    for idx, p in enumerate(products):
        if p["productID"] == str(id):
            deleted = products.pop(idx)
            save_product(products)
            return {"message": "product deleted successfully", "data": deleted}


# def change_product(product_id:str,update_data:Dict):
    
#     products = get_all_products()
    
#     for index,product in enumerate(products):
#         if product.get("productID") != product_id:
#             continue
#         for key,value in update_data.items():
#             if value is None:
#                 continue
#             if isinstance(value,dict) and isinstance(product.get(key),dict):
#                 product[key].update(value)
#             else:
#                 product[key] = value
                
#         save_product(products)
#         return product
#     raise ValueError("Product not found!")

def change_product(product_id: str, update_data: Dict):
    
    products = get_all_products()
    
    for index, product in enumerate(products):

        if product["productID"] != product_id:
            continue
        
        for key, value in update_data.items():
            if value is None:
                continue
            
            if isinstance(value, dict) and isinstance(product.get(key), dict):
                product[key].update(value)
            else:
                product[key] = value
        dim = product.get("dimension_in_product")
        if dim and dim.get("length") is not None and dim.get("breath") is not None:
            product["computed_dimension"] =  round(dim["length"]*dim["breath"],2)
        save_product(products)
        return product
    
    raise ValueError(f"product not found for id = {product_id}")

    