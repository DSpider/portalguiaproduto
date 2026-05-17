from __future__ import annotations

from dataclasses import dataclass

from packages.seo.metadata import generate_canonical_url


@dataclass(frozen=True)
class BreadcrumbItem:
    name: str
    url: str


def generate_breadcrumbs(
    base_url: str,
    items: list[tuple[str, str]],
) -> list[BreadcrumbItem]:
    breadcrumbs = [BreadcrumbItem(name="Inicio", url=base_url.rstrip("/") + "/")]

    for name, path_or_title in items:
        breadcrumbs.append(
            BreadcrumbItem(
                name=name.strip(),
                url=generate_canonical_url(base_url, path_or_title),
            )
        )

    return breadcrumbs
