from django.shortcuts import render
from .models import Product, Review
# Create your views here.

def main_view(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    return render(request, 'products/products.html', context={'products': Product.objects.all()})


def product_detail_view(request, id):
    if request.method =='GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'reviews': Review.objects.filter(product=product)
        }

        return render(request, 'products/detail.html', context=context)







