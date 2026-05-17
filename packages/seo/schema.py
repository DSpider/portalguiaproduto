from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from packages.seo.breadcrumbs import BreadcrumbItem
from packages.seo.faq import FAQItem


@dataclass(frozen=True)
class OfferData:
    price: Decimal | float | str | None
    currency: str
    availability: str | None
    url: str | None
    price_is_reliable: bool
    last_checked_at: str | None = None


@dataclass(frozen=True)
class ReviewData:
    rating_value: float | None
    review_count: int | None
    source_is_reliable: bool
    tested_by_guia_produto: bool = False


@dataclass(frozen=True)
class ProductSchemaInput:
    name: str
    url: str
    brand: str | None = None
    description: str | None = None
    image_url: str | None = None
    sku: str | None = None
    updated_at: str | None = None
    offer: OfferData | None = None
    review: ReviewData | None = None


@dataclass(frozen=True)
class OrganizationData:
    name: str
    url: str
    logo_url: str | None = None


def generate_product_schema(product: ProductSchemaInput) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "url": product.url,
    }

    if product.brand:
        schema["brand"] = {"@type": "Brand", "name": product.brand}
    if product.description:
        schema["description"] = product.description
    if product.image_url:
        schema["image"] = product.image_url
    if product.sku:
        schema["sku"] = product.sku
    if product.updated_at:
        schema["dateModified"] = product.updated_at

    if product.offer and product.offer.price_is_reliable and product.offer.price is not None:
        offer: dict[str, Any] = {
            "@type": "Offer",
            "price": str(product.offer.price),
            "priceCurrency": product.offer.currency,
        }
        if product.offer.url:
            offer["url"] = product.offer.url
        if product.offer.availability:
            offer["availability"] = f"https://schema.org/{product.offer.availability}"
        if product.offer.last_checked_at:
            offer["priceValidUntil"] = product.offer.last_checked_at
        schema["offers"] = offer

    if (
        product.review
        and product.review.source_is_reliable
        and product.review.rating_value is not None
        and product.review.review_count is not None
        and product.review.review_count > 0
    ):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": product.review.rating_value,
            "reviewCount": product.review.review_count,
        }

        if product.review.tested_by_guia_produto:
            schema["review"] = {
                "@type": "Review",
                "author": {"@type": "Organization", "name": "Guia Produto"},
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": product.review.rating_value,
                    "bestRating": 5,
                },
            }

    return schema


def generate_faq_schema(faq_items: list[FAQItem]) -> dict[str, Any] | None:
    if not faq_items:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.answer,
                },
            }
            for item in faq_items
        ],
    }


def generate_breadcrumb_schema(items: list[BreadcrumbItem]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": item.name,
                "item": item.url,
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def generate_item_list_schema(name: str, items: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": item["name"],
                "url": item["url"],
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def generate_organization_schema(data: OrganizationData) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": data.name,
        "url": data.url,
    }
    if data.logo_url:
        schema["logo"] = data.logo_url
    return schema


def generate_website_schema(name: str, url: str) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": name,
        "url": url,
    }


def validate_json_ld_schema(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if schema.get("@context") != "https://schema.org":
        errors.append("contexto_invalido")
    if "@type" not in schema:
        errors.append("tipo_ausente")

    schema_type = schema.get("@type")
    if schema_type == "Product":
        if not schema.get("name"):
            errors.append("product_name_ausente")
        if "offers" in schema:
            offer = schema["offers"]
            if not offer.get("price") or not offer.get("priceCurrency"):
                errors.append("offer_incompleta")
        if "aggregateRating" in schema:
            rating = schema["aggregateRating"]
            if not rating.get("ratingValue") or not rating.get("reviewCount"):
                errors.append("rating_incompleto")

    if schema_type == "FAQPage" and not schema.get("mainEntity"):
        errors.append("faq_vazio")

    if schema_type == "BreadcrumbList" and not schema.get("itemListElement"):
        errors.append("breadcrumbs_vazio")

    return errors
