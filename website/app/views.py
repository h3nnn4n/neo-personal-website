from datetime import datetime
from os import path

from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.views.generic.base import View

from app.services import parse_md_file, read_file, render_markdown


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class PostView(View):
    def get(self, request, *args, **kwargs):
        file_contents = read_file(
            path.join(
                settings.CONTENT_FOLDER,
                "posts/hello-world.md",
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
                "content": content,
            },
        )
