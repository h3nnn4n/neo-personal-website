from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.views.generic.base import View

from app.services import load_markdown, render_markdown


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class PostView(View):
    def get(self, request, *args, **kwargs):
        content = mark_safe(render_markdown(load_markdown("test.md")))

        return render(
            request,
            "post.html",
            context={
                "title": "hi this is post",
                "content": content,
            },
        )
