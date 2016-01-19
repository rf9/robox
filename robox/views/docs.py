import os

from django.shortcuts import render

from mainsite import settings


def index(request):
    return render(request, "robox/docs/index.html")


def api(request):
    return render(request, "robox/docs/markdown.html", {
        'title': 'API docs',
        'markdown_content': "\n".join(open(os.path.join(settings.BASE_DIR, "robox/static/robox/docs/md/api.md")))
    })


def parsers(request):
    return render(request, "robox/docs/markdown.html", {
        'title': 'Parser docs',
        'markdown_content': "\n".join(open(os.path.join(settings.BASE_DIR, "robox/static/robox/docs/md/parsers.md")))
    })
