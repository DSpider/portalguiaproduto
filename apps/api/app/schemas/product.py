from pydantic import BaseModel, Field


class ProductSummary(BaseModel):
    slug: str
    name: str
    brand: str
    category: str
    trend_score: int = Field(ge=0, le=100)
    confidence: str


class ProductDetail(ProductSummary):
    summary: str
    data_sources: list[str]
    last_updated: str
