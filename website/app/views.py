import itertools
from datetime import datetime
from os import path

import humanize
import pytz
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Context, Template
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.views.generic.base import View

from app import services
from app.services import kiln, parse_md_file, read_file, render_markdown


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        file_contents = read_file(
            path.join(
                settings.CONTENT_FOLDER,
                "about.md",
            ),
        )

        headers, markdown_data = parse_md_file(file_contents)
        md_content = mark_safe(  # nosec
            render_markdown(
                markdown_data,
            )
        )

        # Render any tags from the markdown files
        md_content = "{% load static %}\n" + md_content
        template = Template(md_content)
        content = template.render(Context({}))

        return render(
            request,
            "about.html",
            context={
                "content": content,
            },
        )


class TagView(View):
    def get(self, request, *args, **kwargs):
        tag = kwargs.get("tag")

        if tag:
            try:
                return self.render_tag(request, tag)
            except FileNotFoundError:
                raise Http404()

        posts = services.list_posts(order_field="date", hide_drafts=True)
        all_tags = sorted(set(itertools.chain.from_iterable(p["tags"] for p in posts)))
        tags = []

        for tag_name in all_tags:
            tag = {}
            tag["name"] = tag_name
            tag["name__escaped"] = tag_name.replace(" ", "_")
            tag["post_count"] = len([True for post in posts if tag_name in post["tags"]])
            tags.append(tag)

        return render(
            request,
            "tags.html",
            context={
                "tags": tags,
            },
        )

    def render_tag(self, request, tag):
        tag = tag.replace("_", " ")

        posts = services.list_posts(order_field="date", hide_drafts=True)
        posts = [post for post in posts if tag in post["tags"]]

        # No posts for a tag means that the tag doesn't exist
        if len(posts) == 0:
            raise Http404()

        return render(
            request,
            "posts.html",
            context={
                "posts": posts,
                "custom_title": f'tagged "{tag}"',
            },
        )


class PostView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")

        if slug:
            try:
                return render_post(request, slug)
            except FileNotFoundError:
                raise Http404()

        posts = services.list_posts(order_field="date", hide_drafts=True)
        all_tags = sorted(set(itertools.chain.from_iterable(p["tags"] for p in posts)))
        tags = []

        for tag_name in all_tags:
            tag = {}
            tag["name"] = tag_name
            tag["name__escaped"] = tag_name.replace(" ", "_")
            tag["post_count"] = len([post for post in posts if tag_name in post["tags"]])
            tags.append(tag)

        tags = sorted(tags, key=lambda t: t["post_count"], reverse=True)

        return render(
            request,
            "posts.html",
            context={
                "posts": posts,
                "tags": tags,
            },
        )


class ProjectsView(View):
    def get(self, request, *args, **kwargs):
        projects = services.list_projects(order_field="weight", hide_drafts=True)

        return render(
            request,
            "projects.html",
            context={
                "projects": projects,
                "base_repo_url": settings.BASE_REPO_URL,
            },
        )


class GamesView(View):
    def get(self, request, *args, **kwargs):
        return render_post(request, "games", base_folder="")


def render_post(request, slug: str, base_folder: str = "posts"):
    print(f"rendering post {slug}")
    file_contents = read_file(
        path.join(
            settings.CONTENT_FOLDER,
            path.join(base_folder, f"{slug}.md"),
        ),
    )

    headers, markdown_data = parse_md_file(file_contents)
    __import__("pprint").pprint(headers)

    date = datetime.strptime(headers["date"], "%Y-%m-%d")
    pretty_date = date.strftime("%B %d, %Y")

    md_content = mark_safe(  # nosec
        render_markdown(
            markdown_data,
        )
    )

    md_content = "{% load static %}\n" + md_content
    template = Template(md_content)
    content = template.render(Context({}))

    return render(
        request,
        "post.html",
        context={
            "title": headers.get("title"),
            "date": pretty_date,
            "tags": headers.get("tags"),
            "content": content,
        },
    )


class KilnView(View):
    def get(self, request, *args, **kwargs):
        temperature_date, temperature = kiln.get_temperature()
        _, setpoint = kiln.get_setpoint()

        if temperature_date is not None:
            temperature_date = parse_datetime(temperature_date).astimezone(pytz.utc)
            print(temperature_date)
            print(timezone.now())
            last_temp_update_time_ago = humanize.naturaltime(timezone.now() - temperature_date)
        else:
            last_temp_update_time_ago = ""

        if setpoint is not None and temperature is not None:
            error = setpoint - temperature
            error = round(error, 2)
            error = f"{error}°C"
        else:
            error = None

        if setpoint is not None:
            setpoint = round(setpoint, 2)
            setpoint = f"{setpoint}°C"

        if temperature is not None:
            temperature = round(temperature, 2)
            temperature = f"{temperature}°C"

        return render(
            request,
            "kiln.html",
            context={
                "setpoint": setpoint,
                "temperature": temperature,
                "error": error,
                "last_temp_update": temperature_date,
                "last_temp_update_time_ago": last_temp_update_time_ago,
            },
        )
