from pydantic import BaseModel, Field

from app.schemas.product import ProductSummary


class RadarSummary(BaseModel):
    status: str
    mode: str
    generated_at: str
    total_products: int = Field(ge=0)
    top_categories: list[str]
    highlighted_products: list[ProductSummary]
