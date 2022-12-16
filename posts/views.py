from django.shortcuts import render
from posts.models import Post, Product
# Create your views here.

def main_view(request):
    return render(request, 'layouts/index.html')

def posts_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        return render(request, 'posts/posts.html', context={'posts':posts})

def products_view(request):
    return render(request, 'products/products.html', context={'products': Product.objects.all()})









