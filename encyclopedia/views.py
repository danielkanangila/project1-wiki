from django import forms
from django.shortcuts import render
from django.http import Http404
from markdown2 import Markdown

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404(f"We are enable to to found the article  '{title}'.")

    markdowner = Markdown()
    html_content = markdowner.convert(entry)

    return render(request, "encyclopedia/wiki_show.html", {
        "title": title,
        "html_content": html_content,
    })


def create(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })
