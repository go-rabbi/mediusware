from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from product.models import *


def productlist(request):
    #all_product=Product.objects.all()
    #all_variant=Variant.objects.all()
    #all_productimage=ProductImage.objects.all()
    #all_productvariant=ProductVariant.objects.all()
    title = request.GET.get('title')
    variant = request.GET.get('variant')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    date = request.GET.get('date')

    print(variant)

    # Filter the ProductVariantPrice queryset based on form inputs
    filtered_prices = ProductVariantPrice.objects.all()

    if title:
        filtered_prices = filtered_prices.filter(product__title__icontains=title)

    if variant:
        filtered_prices = filtered_prices.filter(
            Q(product_variant_one__variant_title__icontains=variant) |
            Q(product_variant_two__variant_title__icontains=variant) |
            Q(product_variant_three__variant_title__icontains=variant)
        )
    print(filtered_prices)

    if price_from:
        filtered_prices = filtered_prices.filter(price__gte=price_from)

    if price_to:
        filtered_prices = filtered_prices.filter(price__lte=price_to)

    if date:
        filtered_prices = filtered_prices.filter(created_at__date=date)

    all_productvariantprice=filtered_prices
    
    product_details_dict={}
    id=0
    used_id={}
    for prodct in all_productvariantprice:
        tem_dict={}
        tem_dict['title']=prodct.product.title
        tem_dict['created_at']=prodct.product.created_at
        tem_dict['description']=prodct.product.description
        tem_dict['var1']=prodct.product_variant_one.variant_title
        tem_dict['var2']=prodct.product_variant_two.variant_title
        if prodct.product_variant_three!=None:
            tem_dict['var3']=prodct.product_variant_three.variant_title
        else:
            tem_dict['var3']='None'
        tem_dict['price']=prodct.price
        tem_dict['stock']=prodct.stock

        if tem_dict['title'] in product_details_dict:
            tem_dict['id']=used_id[tem_dict['title']]
            product_details_dict[tem_dict['title']].append(tem_dict)
        else:
            id+=1
            tem_dict['id']=id
            used_id[tem_dict['title']]=id
            product_details_dict[tem_dict['title']]=[]
            product_details_dict[tem_dict['title']].append(tem_dict)
    
    product_detailes=[]
    for key in product_details_dict:
        tem_dict={}
        tem_dict['title']=key
        tem_arr=[]
        for data in product_details_dict[key]:
            tem_dict['id']=data['id']
            tem_dict['created_at']=data['created_at']
            tem_dict['description']=data['description']
            tem_dict2={}
            tem_dict2['var1']=data['var1']
            tem_dict2['var2']=data['var2']
            tem_dict2['var3']=data['var3']
            tem_dict2['price']=data['price']
            tem_dict2['stock']=data['stock']
            tem_arr.append(tem_dict2)
        tem_dict['variant']=tem_arr
        product_detailes.append(tem_dict)

    items_per_page = 5
    paginator = Paginator(product_detailes, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/list.html",
        {
            "page_obj": page_obj,
        },
    )
