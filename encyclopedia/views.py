from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    entry = util.get_entry(title)
    if entry:
        html_content = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry_page.html", {
            "html_content": html_content,
            "title": title
        })
    else:
        return render(request, "encyclopedia/not_found.html")
        