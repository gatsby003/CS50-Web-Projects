from django.shortcuts import render
from django import forms
from django.urls import reverse
from random import randint

from . import util
from markdown import markdown


class CreateEntry(forms.Form):
    title = forms.CharField()
    entry = forms.CharField(widget=forms.Textarea)




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def fetch(request, name):
    entries = util.list_entries()
    clean_entries = [x.lower() for x in entries]
    clean_name = name.lower()
    if clean_name in clean_entries:
        entry = util.get_entry(entries[clean_entries.index(clean_name)])
        clean_entry = markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry" : clean_entry,
            "title" : entries[clean_entries.index(clean_name)]
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : False
        })

def search(request):
    query = request.POST['q'].lower()
    entries = util.list_entries()
    clean_entries = [x.lower() for x in entries]
    if query in clean_entries:
        return fetch(request, query)
    else:
        close_results = [x for x in entries if query in x.lower()]
        return render(request, "encyclopedia/search.html", {
            'entries' : close_results
        })

def create(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = CreateEntry(request.POST)
        if form.is_valid():
            clean_entry = form.cleaned_data["entry"]
            clean_title = form.cleaned_data["title"]
            if clean_title.lower() not in [x.lower() for x in entries]:
                util.save_entry(clean_title, clean_entry)
                return index(request)
            else:
                return render(request, "encyclopedia/error.html",{
                    "error" : "Entry Already Exists"
                })
    else:
        return render(request, "encyclopedia/create.html",{
            "form" : CreateEntry()
            })

def edit(request,title):
    if request.method == "POST":
        form = CreateEntry(request.POST)
        if form.is_valid():
            clean_entry = form.cleaned_data["entry"]
            clean_title = form.cleaned_data["title"]
            util.save_entry(clean_title, clean_entry)
            return fetch(request, clean_title)
    else:
        entry = util.get_entry(title)
        initial = {"title": title, "entry": entry}
        form01 = CreateEntry(initial)
        print(entry)
        print(form01)
        return render(request, 'encyclopedia/edit.html',{
            "form" : form01,
            "title": title
        })

def random(request):
    all_entries = util.list_entries()
    entry = randint(0,len(all_entries)-1)
    return fetch(request, all_entries[entry])
