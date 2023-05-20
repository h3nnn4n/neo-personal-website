import itertools
from datetime import datetime
from os import path

from django.conf import settings
from django.shortcuts import render
from django.template import Context, Template
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.views.generic.base import View

from app import services
from app.services import parse_md_file, read_file, render_markdown


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
            return self.render_tag(request, tag)

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
            return render_post(request, slug)

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
