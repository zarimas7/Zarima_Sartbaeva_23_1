from django.shortcuts import HttpResponse, render, redirect

from posts.forms import ProductCreateForm, ReviewCreateForm
from .models import Product, Review, Category
# Create your views here.

PAGINTION_LIMIT = 3

def main_view(request):
    return render(request, 'layouts/index.html')

def products_view(request):
    if request.method == 'GET':
        category_id = int(request.GET.get('category_id',0))
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = Product.objects.filter(categories__in=[category_id])

        else:
            products = Product.objects.all()

        max_page = products.__len__() // PAGINTION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        products = products[PAGINTION_LIMIT*(page-1):PAGINTION_LIMIT * page]

        if search:
            products = products.filter(name__icontains=search)

        return render(request, 'products/products.html', context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page+1)
        })


def product_detail_view(request, id):
    if request.method =='GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'reviews': product.reviews.all(),
            'categories': product.categories.all(),
            'review_form': ReviewCreateForm
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        product = Product.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author=request.user,
                product_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'reviews': product.reviews.all(),
                'categories': product.categories.all(),
                'review_form': form
            })

def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'categories/index.html', context=context)

def product_create_view(request):
    if request.method == 'GET':
        return render(request, 'products/create.html', context={
            'form': ProductCreateForm
        })


    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                author=request.user,
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('rate', 0)
            )
            return redirect('/products/')
        else:
            return render(request, 'products/create.html', context={
                'form': form
            })




