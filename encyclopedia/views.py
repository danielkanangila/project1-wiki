from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True, min_length=2)
    content = forms.CharField(label="Markdown Content",
                              widget=forms.Textarea, required=True, min_length=2)


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
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": f"Article '{title}' already exist."
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(
                'show',
                kwargs={"title": title}
            ))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm(),
        })
