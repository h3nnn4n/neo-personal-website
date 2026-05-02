import os
from urllib.parse import quote

import yaml
from django.conf import settings

from app.utils import cached


def get_portfolio(slug: str = "general") -> dict:
    portfolio_path = os.path.join(settings.CONTENT_FOLDER, "portfolio", f"{slug}.md")
    portfolio_mtime = os.path.getmtime(portfolio_path)

    bio_path = os.path.join(settings.CONTENT_FOLDER, "portfolio", "bio.md")
    bio_mtime = os.path.getmtime(bio_path)

    return cached(
        ["get_portfolio", slug, portfolio_mtime, bio_mtime],
        lambda: _get_portfolio_impl(slug, portfolio_path, bio_path),
    )


def _get_portfolio_impl(slug, portfolio_path, bio_path):
    with open(portfolio_path, "rt") as f:
        raw = f.read()

    headers, statement = _parse_yaml_frontmatter(raw)

    with open(bio_path, "rt") as f:
        bio_raw = f.read()

    bio_headers, bio_text = _parse_yaml_frontmatter(bio_raw)

    pieces = []
    for piece in headers.get("pieces", []):
        piece = piece.copy()
        piece["image_path"] = os.path.join(settings.BASE_DIR, piece["file"])
        piece["image_url"] = settings.STATIC_URL + quote(piece["file"].removeprefix("content/").removeprefix("static/"))
        pieces.append(piece)

    artist_photo = headers.get("artist_photo", "")
    artist_photo_url = ""
    if artist_photo:
        artist_photo_url = settings.STATIC_URL + quote(artist_photo.removeprefix("content/").removeprefix("static/"))
        artist_photo = os.path.join(settings.BASE_DIR, artist_photo)

    return {
        "title": headers.get("title", ""),
        "artist_photo": artist_photo,
        "artist_photo_url": artist_photo_url,
        "pieces": pieces,
        "statement": statement.strip(),
        "bio": bio_text.strip(),
        "bio_photo": os.path.join(settings.BASE_DIR, bio_headers.get("artist_photo", "")) if bio_headers.get("artist_photo") else "",
        "bio_photo_url": (settings.STATIC_URL + quote(bio_headers["artist_photo"].removeprefix("content/").removeprefix("static/"))) if bio_headers.get("artist_photo") else "",
    }


def get_piece(piece_slug: str, portfolio_slug: str = "general") -> dict | None:
    data = get_portfolio(portfolio_slug)
    for piece in data["pieces"]:
        slug = piece.get("slug") or os.path.splitext(os.path.basename(piece["file"]))[0]
        if slug == piece_slug:
            return piece

    return None


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
