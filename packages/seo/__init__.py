"""Ferramentas de SEO tecnico do Guia Produto Radar."""

from packages.seo.breadcrumbs import BreadcrumbItem, generate_breadcrumbs
from packages.seo.content import HeadingStructure, generate_heading_structure
from packages.seo.faq import FAQItem, generate_faq
from packages.seo.metadata import generate_canonical_url, generate_meta_description, generate_seo_title
from packages.seo.quality import ThinContentResult, validate_content_depth
from packages.seo.schema import (
    OfferData,
    OrganizationData,
    ProductSchemaInput,
    ReviewData,
    generate_breadcrumb_schema,
    generate_faq_schema,
    generate_item_list_schema,
    generate_organization_schema,
    generate_product_schema,
    generate_website_schema,
    validate_json_ld_schema,
)
from packages.seo.slug import generate_slug

__all__ = [
    "BreadcrumbItem",
    "FAQItem",
    "HeadingStructure",
    "OfferData",
    "OrganizationData",
    "ProductSchemaInput",
    "ReviewData",
    "ThinContentResult",
    "generate_breadcrumb_schema",
    "generate_breadcrumbs",
    "generate_canonical_url",
    "generate_faq",
    "generate_faq_schema",
    "generate_heading_structure",
    "generate_item_list_schema",
    "generate_meta_description",
    "generate_organization_schema",
    "generate_product_schema",
    "generate_seo_title",
    "generate_slug",
    "generate_website_schema",
    "validate_content_depth",
    "validate_json_ld_schema",
]
