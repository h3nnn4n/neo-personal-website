import json
import logging
import os
import typing as t
from datetime import datetime
from os import path
from typing import Any

from django.conf import settings
from markdown import markdown
from memoize import memoize


logger = logging.getLogger(__name__)


@memoize(timeout=settings.POST_MEMOIZE_TIME)
def read_file(filename: str) -> str:
    with open(filename, "rt") as f:
        return f.read()


@memoize(timeout=settings.POST_MEMOIZE_TIME)
def render_markdown(markdown_str: str):
    return markdown(markdown_str, extensions=["attr_list"])


@memoize(timeout=settings.POST_MEMOIZE_TIME)
def list_projects(order_field: t.Optional[str] = None, hide_drafts: bool = False) -> list[dict[str, Any]]:
    projects_folder = path.join(settings.CONTENT_FOLDER, "projects")
    return parse_and_list_md_files(projects_folder, order_field=order_field, hide_drafts=hide_drafts)


@memoize(timeout=settings.POST_MEMOIZE_TIME)
def list_posts(order_field: t.Optional[str] = None, hide_drafts: bool = False) -> list[dict[str, Any]]:
    posts_folder = path.join(settings.CONTENT_FOLDER, "posts")
    return parse_and_list_md_files(posts_folder, order_field=order_field, hide_drafts=hide_drafts)


def parse_and_list_md_files(
    base_folder: str, order_field: t.Optional[str] = None, hide_drafts: bool = False
) -> list[dict[str, Any]]:
    def _parse(post: str) -> dict:
        post_path = path.join(base_folder, post)
        file_contents = read_file(post_path)
        headers, _ = parse_md_file(file_contents)

        if headers.get("date"):
            date = datetime.strptime(headers["date"], "%Y-%m-%d")
            headers["pretty_date"] = date.strftime("%B %d, %Y")
            headers["filename"] = post.partition(".")[0]

        return headers

    posts = [_parse(p) for p in os.listdir(base_folder)]

    if hide_drafts:
        posts = [p for p in posts if not p["draft"]]

    if order_field:
        posts = sorted(posts, key=lambda x: x[order_field], reverse=True)

    return posts


@memoize(timeout=settings.POST_MEMOIZE_TIME)
def parse_md_file(markdown_str: str):
    """
    Poor man's parsing
    """

    to_process = markdown_str
    line_number = -1  # So the first iteration is zero
    parsing_header = False
    headers = {}

    while to_process:
        line, _, to_process = to_process.partition("\n")
        line_number += 1
        print(f"line {line_number}: " + line)

        if line_number == 0 and line == "---":
            parsing_header = True
            logger.info("started parsing header")
            continue

        if line == "---" and parsing_header:
            parsing_header = False
            content = to_process
            logger.info("finished parsing header")
            break

        key, _, value = line.partition(":")
        value = value.strip()

        try:
            # If it is a list, this will work :)
            value = json.loads(value)
        except Exception:  # nosec
            pass

        headers[key] = value

    if parsing_header:
        logger.warning("finished parsing file but found no end of header marker")

    return headers, content
