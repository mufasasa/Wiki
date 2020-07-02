from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, TITLE):
    message = "THIS ENTRY DOES NOT EXIST"
    entry = util.get_entry(TITLE)
    entry = markdown2.markdown(entry)
    if not entry:
        return render(request, "encyclopedia/error.html",{
            "message":message
        })
    
    return render(request, "encyclopedia/entrypage.html", {
        "entry":entry,
        "title":TITLE
    } )

def search(request):
    querry = request.POST["q"]
    search = util.get_entry(querry)
    if search:
        return HttpResponseRedirect(reverse("entrypage", args=(querry,)))
    
    entries = util.list_entries()
    res =  [i for i in entries if querry in i]
    return render(request, "encyclopedia/search.html", {
        "res":res
    })

def newpage(request):
    message = "This title already exists"
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")

    title = request.POST["title"]
    exists = util.get_entry(title)
    if exists:
        return render(request, "encyclopedia/error.html",{
            "message":message
        })
    body = request.POST["body"]
    util.save_entry(title, body)
    return HttpResponseRedirect(reverse("entrypage",args=(title,))) 

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "content":content,
            "title":title
        })

    else:
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entrypage", args=(title,)))

def randompage(request):
    entries = util.list_entries()
    i = len(entries) 
    index = random.randint(0,i)
    title = entries[index]
    return HttpResponseRedirect(reverse("entrypage", args=(title,)))


     

