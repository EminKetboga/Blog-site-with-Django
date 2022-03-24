from distutils.errors import CompileError
from email import message
from pickletools import read_uint1
from django.shortcuts import redirect, render,HttpResponse,get_object_or_404,reverse
from matplotlib.pyplot import title
from matplotlib.style import context
from django.contrib.auth.decorators import login_required
import article
from .forms import ArticleForm
from .models import Article,Comment

from django.contrib import messages
# Create your views here.
def index(request):
    resim = "https://images.wallpaperscraft.com/image/single/street_night_wet_155637_1920x1080.jpg"
    
    return render(request,"index.html",{"resim":resim})

def about(request):
    return render(request,"about.html")


def detail(request,id):
    articles = get_object_or_404(Article,id = id)
    comments = articles.comments.all()
    return render(request,"detail.html",{"articles":articles,"comments":comments})

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }

    return render(request,"dashboard.html",context)
@login_required(login_url="user:login")
def  addarticle(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        form.save()
        messages.success(request,"Makale Başarı İle Oluşturuldu.")
        return redirect("index")

    return render(request,"addarticle.html",{"form": form})
@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,instance=article)
    if form.is_valid():
        articles = form.save(commit = False)
        articles.author = request.user
        form.save()
        messages.success(request,"Makaleniz Başarı ile Güncellendi!")
        return redirect("index")

    return render(request,"update.html",{"form":form})
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makaleniz Başarı İle Silindi!")
    return redirect("dashboard")

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def addComment(request,id):
    article = get_object_or_404(Article,id = id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author  = comment_author, comment_content = comment_content)

        newComment.article = article

        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))