from django.shortcuts import render
from .models import Product, Review, Category
# Create your views here.

def main_view(request):
    return render(request, 'layouts/index.html')

def products_view(request):
    if request.method == 'GET':
        category_id = int(request.GET.get('category_id',0))

        if category_id:
            products = Product.objects.filter(categories__in=[category_id])

        else:
            products = Product.objects.all()

        return render(request, 'products/products.html', context={
            'products': products
        })


def product_detail_view(request, id):
    if request.method =='GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'reviews': product.reviews.all(),
            'categories': product.categories.all()
        }

        return render(request, 'products/detail.html', context=context)

def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'categories/index.html', context=context)






