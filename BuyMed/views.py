from django.shortcuts import render,get_object_or_404, get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Product,Category
from cart.forms import CartAddProductForm
from itertools import chain

# Create your views here.
def product_list(request,category_slug=None):
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category,slug=category_slug)
		products = products.filter(category=category)
	return render(request, 
				'BuyMed/product/list.html', 
				{'category': category,
				'categories': categories,
				'products': products})

def product_detail(request, id, slug):
	product=get_object_or_404(Product,id=id,slug=slug,available=True)
	cart_product_form = CartAddProductForm()
	print(product.price)
	return render(request,
				'BuyMed/product/detail.html',
				{'product':product,
				'cart_product_form': cart_product_form})

def product_name_search(request, search_thing=None):
	if search_thing == None:
		search_thing = request.GET.get('search_thing'）
	error_message = ''		
	print(search_thing)
	# search_condition = {'name__icontains': search_thing, 'description__icontains': search_thing}
	# products = Product.objects.filter(**search_condition)
	p_name = Product.objects.filter(name__iexact=search_thing)
	p_desc = Product.objects.filter(description__iexact=search_thing)
	
	products = chain(p_name, p_desc)
	return render(request,
			'BuyMed/product/list.html',
			{'products': products})

def back_to_login(request):
	return render(request, 'registration/login.html')
