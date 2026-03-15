import os

import yaml
from django.conf import settings


def get_portfolio(slug: str = "general") -> dict:
    portfolio_path = os.path.join(settings.CONTENT_FOLDER, "portfolio", f"{slug}.md")

    with open(portfolio_path, "rt") as f:
        raw = f.read()

    headers, statement = _parse_yaml_frontmatter(raw)

    bio_path = os.path.join(settings.CONTENT_FOLDER, "portfolio", "bio.md")
    with open(bio_path, "rt") as f:
        bio_raw = f.read()

    bio_headers, bio_text = _parse_yaml_frontmatter(bio_raw)

    for piece in headers.get("pieces", []):
        piece["image_path"] = os.path.join(settings.BASE_DIR, piece["file"])

    artist_photo = headers.get("artist_photo", "")
    if artist_photo:
        artist_photo = os.path.join(settings.BASE_DIR, artist_photo)

    return {
        "title": headers.get("title", ""),
        "artist_photo": artist_photo,
        "pieces": headers.get("pieces", []),
        "statement": statement.strip(),
        "bio": bio_text.strip(),
        "bio_photo": os.path.join(settings.BASE_DIR, bio_headers.get("artist_photo", "")) if bio_headers.get("artist_photo") else "",
    }


def _parse_yaml_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---"):
        return {}, raw

    end = raw.find("---", 3)
    if end == -1:
        return {}, raw

    frontmatter = raw[3:end]
    content = raw[end + 3:]

    headers = yaml.safe_load(frontmatter) or {}
    return headers, content
