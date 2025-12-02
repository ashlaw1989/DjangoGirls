from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post
from .forms import PostForm

# Create your views here.

# views always take in a request, and they almost always render and return a response
def post_list(request):
    # we can query the database for all the published posts in our Post table
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    # when rendering a webpage we return a render of the request, athe html page we want to load, and any data we want to pass to that webpage (usually in the form of a db query)
    return render(request, "blog/post_list.html", {"posts" : posts})

# see one post details
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post" : post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)

    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form" : form})