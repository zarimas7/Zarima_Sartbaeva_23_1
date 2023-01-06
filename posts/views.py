from django.shortcuts import HttpResponse, render, redirect

from posts.forms import ProductCreateForm, ReviewCreateForm
from .models import Product, Review, Category
from django.views.generic import ListView, CreateView

# Create your views here.

PAGINTION_LIMIT = 3

def main_view(request):
    return render(request, 'layouts/index.html')

class ProductsCBV(ListView):
    queryset = Product.objects.all()
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'products': kwargs['products'],
            'max_page': kwargs['max_page'],
            'user': kwargs['user']
        }

    def get(self, request, **kwargs):
        if request.method == 'GET':
            category_id = int(request.GET.get('category_id', 0))
            search = request.GET.get('search')
            page = int(request.GET.get('page', 1))

            if category_id:
                products = Product.objects.filter(categories__in=[category_id])

            else:
                products = Product.objects.all()

            if search:
                products = products.filter(name__icontains=search)

            max_page = products.__len__() // PAGINTION_LIMIT

            if round(max_page) < max_page:
                max_page = round(max_page) + 1

            products = products[PAGINTION_LIMIT * (page - 1):PAGINTION_LIMIT * page]

            return render(request, self.template_name, context=self.get_context_data(
                products=products,
                user=None if request.user.is_anonymous else request.user,
                max_page=range(1, max_page + 1)
            ))


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

        # if search:
        #     products = products.filter(name__icontains=search)

        return render(request, 'products/products.html', context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page+1)
        })


class ProductDetailCBV(ListView):
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    model = Product
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product':kwargs['product'],
            'reviews':kwargs['reviews'],
            'categories':kwargs ['categories'],
            'review_form':kwargs['review_form']

        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author_id=request.user.id,
                text=form.cleaned_data.get('text'),
                product_id=kwargs['id'],
            )
            return redirect(f'/products/{kwargs["id"]}/')

        else:
            return render(request, self.template_name, context=self.get_context_data(
                form=form,
                product=Product.objects.get(id=kwargs['id'])
            ))

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs["id"])
        reviews = Review.objects.filter(product_id=kwargs["id"])
        categories = product.categories.all()


        return render(request, self.template_name, context=self.get_context_data(
            reviews=reviews,
            categories=categories,
            product=Product.objects.get(id=kwargs['id']),
            review_form=ReviewCreateForm
        ))

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


class CategoriesCBV(ListView):
    model = Category
    template_name = 'categories/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'categories': self.get_queryset(),
            'user': self.request.user if not self.request.user.is_anonymous else None
        }


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'categories/index.html', context=context)


class ProductsCreateCBV(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'user': self.request.user if not self.request.user.is_anonymous else None,
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
            )
            return redirect('/products')
        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))
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




