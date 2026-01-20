#change
from fastapi import FastAPI, HTTPException, Query, Path
from services.products import get_all_products, add_product, remove_product
from schema.products_schema import Products
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hii, I am learning FastAPI"}


# creating a product using POST request
@app.post("/product")
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


# getting a single product by id
@app.get("/product/{id}")
def get_product_by_id(
    id: str = Path(..., min_length=36, max_length=36, examples="0000001"),
):
    products = get_all_products()

    product = next((p for p in products if p.get("productID") == id), None)

    if not product:
        raise HTTPException(status_code=404, detail=f"product not found at id = {id}")
    return product


# getting products by using filter and pagination,sorting, offset which mean skipping
@app.get("/products")
def by_name(
    name: str = Query(
        default=None, min_length=1, max_length=40, description="Using name only"
    ),
    sort: str = Query(
        default=None, description="sorting could be done using: category, price"
    ),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
    limit: int = Query(default=2, ge=1, le=4),
    offset: int = Query(default=0, ge=0, description="Tells where to start from"),
):
    products = get_all_products()

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
