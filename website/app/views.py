from datetime import datetime
from os import path

from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.views.generic.base import View

from app import services
from app.services import parse_md_file, read_file, render_markdown


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class PostView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")

        if slug:
            return self.render_post(request, slug)

        # TODO: Should show tags
        # TODO: Should show the public date
        # TODO: Should skip drafts
        posts = services.list_posts(ordered=True)

        return render(
            request,
            "posts.html",
            context={
                "posts": posts,
            },
        )

    def render_post(self, request, slug):
        print(f"rendering post {slug}")
        file_contents = read_file(
            path.join(
                settings.CONTENT_FOLDER,
                f"posts/{slug}.md",
            ),
        )

        headers, markdown_data = parse_md_file(file_contents)
        __import__("pprint").pprint(headers)

        date = datetime.strptime(headers["date"], "%Y-%m-%d")
        pretty_date = date.strftime("%B %d, %Y")

        content = mark_safe(
            render_markdown(
                markdown_data,
            )
        )

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
