from typing import Annotated, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr, UrlConstraints, HttpUrl, AfterValidator
from pydantic.alias_generators import to_camel

from utilities.assertion_helpers import assert_host

PRODUCT_CATEGORIES: tuple[str] = ('beauty', 'fragrances', 'furniture', 'groceries', 'home-decoration',
                                  'kitchen-accessories', 'laptops', 'mens-shirts', 'mens-shoes',
                                  'mens-watches', 'mobile-accessories', 'motorcycle', 'skin-care',
                                  'smartphones', 'sports-accessories', 'sunglasses', 'tablets', 'tops',
                                  'vehicle', 'womens-bags', 'womens-dresses', 'womens-jewellery',
                                  'womens-shoes', 'womens-watches')

PRODUCT_AVAILABILITY_STATUS: tuple[str] = ("In Stock", "Low Stock", "Out of Stock")


URL_ANNOTATION = Annotated[HttpUrl,
                           UrlConstraints(allowed_schemes=["https"]),
                           AfterValidator(assert_host)]


class NestedProductDimension(BaseModel):
    width: Annotated[float, Field(ge=0)]
    height: Annotated[float, Field(ge=0)]
    depth: Annotated[float, Field(ge=0)]


class NestedProductReviews(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    rating: Annotated[int, Field(ge=0, le=5)]
    comment: str
    date: datetime
    reviewer_name: str
    reviewer_email: Annotated[EmailStr, Field(min_length=1, max_length=50)]


class NestedProductMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    created_at: datetime
    updated_at: datetime
    barcode: Annotated[str, Field(max_length=13)]
    qr_code: URL_ANNOTATION


class ProductSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: Annotated[int, Field(gt=0)]
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str, Field(min_length=1, max_length=250)]  # Assumption
    category: Literal[PRODUCT_CATEGORIES]
    price: Annotated[float, Field(ge=0)]
    discount_percentage: Annotated[float, Field(ge=0)]
    rating: Annotated[float, Field(ge=0, le=5)]
    stock: Annotated[int, Field(ge=0)]
    tags: list[str]
    brand: Annotated[str | None, Field(min_length=1, max_length=50)] = None
    sku: Annotated[str, Field(min_length=1, max_length=50)]
    weight: Annotated[int, Field(ge=0)]
    dimensions: NestedProductDimension
    warranty_information: Annotated[str, Field(min_length=1)]
    shipping_information: Annotated[str, Field(min_length=1)]
    availability_status: Literal[PRODUCT_AVAILABILITY_STATUS]
    reviews: list[NestedProductReviews]
    return_policy: Annotated[str, Field(min_length=1, max_length=50)]
    minimum_order_quantity: Annotated[int, Field(ge=0)]
    meta: NestedProductMeta
    images: list[URL_ANNOTATION]
    thumbnail: URL_ANNOTATION
