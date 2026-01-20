from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
    computed_field,
)
from typing import Annotated, Literal, Optional
from uuid import UUID
from datetime import datetime


class dimension(BaseModel):
    length: Annotated[int, Field(ge=1, le=9, examples=[3])]
    breath: Annotated[int, Field(ge=1, le=9, examples=[5])]


class Products(BaseModel):
    productID: UUID

    manufacturer: Annotated[
        Literal["zara"],
        Field(
            default="zara",
            min_length=4,
            max_length=4,
            description="Only ZARA",
        ),
    ]

    img: Annotated[
        Optional[HttpUrl],
        Field(
            description="product img url ",
            examples=[
                "https://static.zara.net/photos///2023/I/0/2/p/5320/355/800/2/w/563/5320355800_1_1_1.jpg?ts=1697787915583"
            ],
        ),
    ]

    Url: Annotated[
        Optional[HttpUrl],
        Field(
            description="site url",
            examples=["https://www.zara.com/in/en/man-outerwear-l715.html"],
        ),
    ]

    productName: Annotated[
        str,
        Field(
            min_length=1,
            max_length=20,
            title="hippo",
            description="Product Name",
            examples=["stripped shirt"],
        ),
    ]

    Description: Annotated[
        Optional[str], Field(description="In 100 - 250 words", examples=["Oversize"])
    ]

    price: Annotated[int, Field(gt=0, examples=[1000])]

    category: Annotated[
        str,
        Field(
            min_length=1,
            max_length=10,
            description="what product is it",
            examples=["perfumes", "clothes", "bags"],
        ),
    ]

    dimension_in_product: dimension

    @field_validator("productID", mode="before")
    @classmethod
    def validate_productID(cls, value):
        if "-" not in value:
            raise ValueError("'-' must be present")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_price(cls, model: "Products"):
        if not len(str(model.price)) == 4:
            raise ValueError("Either price is < 1000")

        if model.category not in ["bags", "perfumes", "clothes"]:
            raise ValueError("category is not one of these: bags, perfumes, clothes")

        return model

    @computed_field
    @property
    def final_price(self) -> float:
        discount = 20
        return round((1 - discount / 100) * self.price, 2)

    @computed_field
    @property
    def computed_dimension(self) -> float:
        d = self.dimension_in_product
        return round(d.length * d.breath, 2)

    created_at: datetime



class dimensionUpdate(BaseModel):
    length: Annotated[Optional[int], Field(ge=1, le=9, examples=[3])]
    breath: Annotated[Optional[int], Field(ge=1, le=9, examples=[5])]


class ProductsUpdate(BaseModel):
    # productID: Optional[UUID]

    manufacturer: Annotated[
        Optional[Literal["zara"]],
        Field(
            default="zara",
            min_length=4,
            max_length=4,
            description="Only ZARA",
        ),
    ]

    img: Annotated[
        Optional[HttpUrl],
        Field(
            description="product img url ",
            examples=[
                "https://static.zara.net/photos///2023/I/0/2/p/5320/355/800/2/w/563/5320355800_1_1_1.jpg?ts=1697787915583"
            ],
        ),
    ]

    Url: Annotated[
        Optional[HttpUrl],
        Field(
            description="site url",
            examples=["https://www.zara.com/in/en/man-outerwear-l715.html"],
        ),
    ]

    productName: Annotated[
        Optional[str],
        Field(
            min_length=1,
            max_length=20,
            title="hippo",
            description="Product Name",
            examples=["stripped shirt"],
        ),
    ]

    Description: Annotated[
        Optional[str], Field(description="In 100 - 250 words", examples=["Oversize"])
    ]

    price: Annotated[Optional[int], Field(gt=0, examples=[1000])]

    category: Annotated[
        Optional[str],
        Field(
            min_length=1,
            max_length=10,
            description="what product is it",
            examples=["perfumes", "clothes", "bags"],
        ),
    ]

    dimension_in_product: Optional[dimensionUpdate]

    @field_validator("productID", mode="before")
    @classmethod
    def validate_productID(cls, value):
        if "-" not in value:
            raise ValueError("'-' must be present")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_price(cls, model: "Products"):
        if not len(str(model.price)) == 4:
            raise ValueError("Either price is < 1000")

        if model.category not in ["bags", "perfumes", "clothes"]:
            raise ValueError("category is not one of these: bags, perfumes, clothes")

        return model

    @computed_field
    @property
    def final_price(self) -> float:
        discount = 20
        return round((1 - discount / 100) * self.price, 2)

    @computed_field
    @property
    def computed_dimension(self) -> float:
        d = self.dimension_in_product
        return round(d.length * d.breath, 2)

    # created_at: datetime
