from django.shortcuts import redirect, render
from random import choice

from . import util
from .forms import CreateNewPageForm, EditPageForm

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

def search(request):
    query = request.GET.get("q")
    print(query)
    if query:
        entry = util.get_entry(query)
        if entry:
            return redirect('wiki:entry_page', title=query)
        
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)
        if results:
            return render(request, "encyclopedia/search_results.html", {
                "results": results,
                "query": query
            })
        
        return render(request, "encyclopedia/results_not_found.html", {
            "query": query
        })
        
def new_page(request):
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["text_input"]
            content = form.cleaned_data["textarea_input"]

            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/file_already_exists.html")
            
            util.save_entry(title, content)
            return redirect('wiki:entry_page', title=title)

        else:
            #work on this later
            return 1

    else:
        form = CreateNewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["textarea_input"]

            util.save_entry(title, content)
            return redirect("wiki:entry_page", title=title)
    
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/not_found.html")
    
    form = EditPageForm(initial={"textarea_input": content})
    return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "form": form
        })

def random_page(request):
    entries = util.list_entries()

    random_entry = choice(entries)
    return redirect("wiki:entry_page", title=random_entry)
