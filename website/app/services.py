import json
import logging
import os
from os import path

from django.conf import settings
from markdown import markdown


logger = logging.getLogger(__name__)


def read_file(filename: str) -> str:
    with open(filename, "rt") as f:
        return f.read()


def render_markdown(markdown_str: str):
    return markdown(markdown_str)


def list_posts(ordered: bool = False):
    def _sorter(post):
        file_contents = read_file(path.join(posts_folder, post))
        headers, _ = parse_md_file(file_contents)
        return headers["date"]

    posts_folder = path.join(settings.CONTENT_FOLDER, "posts")
    posts = os.listdir(posts_folder)

    if ordered:
        posts = sorted(posts, key=_sorter, reverse=True)

    return [p.partition(".md")[0] for p in posts]


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
        except Exception:
            pass

        headers[key] = value

    if parsing_header:
        logger.warning("finished parsing file but found no end of header marker")

    return headers, content
