# change
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request
from fastapi.responses import JSONResponse 
from services.products import (
    get_all_products,
    add_product,
    remove_product,
    change_product,
    load_products
)
from schema.products_schema import ProductsUpdate, Products
from uuid import UUID, uuid4
from datetime import datetime

load_dotenv()
app = FastAPI()


# @app.middleware("http")
# async def lifecycle(request: Request, call_next):
#     print("Before request")
#     print(f"Request URL: {request.url}")
#     response = await call_next(request)
#     print("After request")
#     response.headers["CUSTOM-HEADER"] = "was inside middleware"
#     print(response)
#     return response


def common_logic():
    return("hello")


DB_Path = os.getenv("BASE_URL")

print(f"DB_Path: {DB_Path}")


@app.get("/",response_model="dict")
def root(dep=Depends(common_logic)):
    DB_Path = os.getenv("BASE_URL")
    return {"message": "Hii, I am learning FastAPI",
            "Dependencies": dep,"URL":DB_Path}


# getting products by using filter and pagination,sorting, offset which mean skipping
@app.get("/products")
def by_name(
    dep = Depends(load_products),
    name: str = Query(
        default=None, min_length=1, max_length=40, description="Using name only"
    ),
    sort: str = Query(
        default=None, description="sorting could be done using: category, price"
    ),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
    limit: int = Query(default=5, ge=1, le=20),
    offset: int = Query(default=0, ge=0, description="Tells where to start from"),
):
    products = dep

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("productName", "").lower()]

        if not products:
            raise HTTPException(status_code=404, detail=f"No found {name} ")

    # sorting price logic
    if sort == "price":
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)
    # sorting category logic
    elif sort == "category":
        reverse = order == "desc"
        products = sorted(
            products, key=lambda p: p.get("category", "").lower(), reverse=reverse
        )

    total = len(products)
    products = products[offset : offset + limit]

    return {"offset": offset, "limit": limit, "total": total, "items": products}


# getting a single product by id
@app.get("/products/{id}",response_model=Products)
def get_product_by_id(
    id: str = Path(..., min_length=36, max_length=36, examples="0000001"),
):
    products = get_all_products()

    product = next((p for p in products if p.get("productID") == id), None)

    if not product:
        raise HTTPException(status_code=404, detail=f"product not found at id = {id}")
    return product


# creating a product using POST request
@app.post("/products")
def create_product(product: Products):
    product_dict = product.model_dump(mode="json")
    product_dict["productID"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat()

    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product.model_dump(mode="json")


# delete a product using productID
@app.delete("/products/{product_id}")
def delete_product(product_id: UUID = Path(..., description="productID")):
    try:
        res = remove_product(str(product_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# updating the product details
@app.patch("/products/{product_id}")
def update_product(
    product_id: UUID = Path(..., description="Product UUID"),
    payload: ProductsUpdate = ...
):
    update_data = payload.model_dump(exclude_unset=True )
    try:
        updated_product = change_product(
            str(product_id), update_data)
    
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
