from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Product, ProductImages, Variant
from .forms import SearchForm


@require_POST
def search_view(request):
    search = SearchForm(request.POST)
    if search.is_valid():
        data = search.cleaned_data['search']
        if data.isdigit():
            products = Product.objects.filter(Q(price__exact=data) | Q(discount__exact=data))
        else:
            products = Product.objects.filter(Q(name__icontains=data) | Q(content__icontains=data))

        return render(request, 'product/product_list.html', {"products": products})


def product_list_view(request):
    products = Product.objects.active_products
    
    context = {
        'products' : products
    }

    return render(request, 'product/product_list.html', context)


def product_detail_view(request, product_id):
    # product_queryset = Product.objects.prefetch_related("comments").select_related("category").filter(is_active=True)
    
    product = get_object_or_404(Product, id=product_id)
    
    product_images = ProductImages.objects.filter(product__id = product_id)
    
    if request.method == "POST":
        product_variants = Variant.objects.filter(product__id = product_id)
        
        user_select = request.POST.get("select")
        
        variant_select = Variant.objects.select_related("size").get(id= user_select)
        
        variant_sizes = Variant.objects.select_related("size").filter(product__id=product_id).distinct('size__id')
        
        variant_colors = Variant.objects.select_related("color").filter(product__id= product.id, size__id= variant_select.size.id)
        
    else:
        product_variants = Variant.objects.filter(product__id = product_id)
        
        variant_select = Variant.objects.get(id= product_variants[0].id)
        
        variant_sizes = Variant.objects.select_related("size").filter(product__id=product_id).distinct('size__id')

        variant_colors = Variant.objects.select_related("color").filter(product__id= product.id, size__id= product_variants[0].size_id)


    context = {
        "product": product,
        "product_images": product_images,
        "product_variants": product_variants,
        "variant_select": variant_select,
        "variant_sizes": variant_sizes,
        "variant_colors": variant_colors,
    }
    
    return render(request, 'product/product_detail.html', context)


