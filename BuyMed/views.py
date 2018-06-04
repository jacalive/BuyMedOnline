from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Product,Category
from cart.forms import CartAddProductForm

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

def product_detail(request,id,slug):
	product=get_object_or_404(Product,id=id,slug=slug,available=True)
	cart_product_form = CartAddProductForm()
	print(product.price)
	return render(request,
				'BuyMed/product/detail.html',
				{'product':product,
				'cart_product_form': cart_product_form})

def product_name_search(request):
	search_thing=request.GET.get('search_thing')
	error_message=''

	if not search_thing:
		error_message='请输入您要查找的药品名称'
		return render(request,'BuyMed/product/error.html',
		{'error_message':error_message})

	product=get_object_or_404(Product,name__contains=search_thing,available=True)
	return render(request,
				'BuyMed/product/candidate.html',
				{'product',product})

def product_category_search(request):
	search_thing=request.GET.get('search_thing')
	error_message=''

	if not search_thing:
		error_message='请输入您要查找的疾病'
		return render(request,'BuyMed/product/error.html',
		{'error_message':error_message})

	category_id=Category.objects.get(name__contains=search_thing)
	product_find=category_id.product_set.all

	product=get_object_or_404(product_find,available=True)
	return render(request,
				'BuyMed/product/candidate.html',
				{'product',product})
