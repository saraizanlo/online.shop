from django.shortcuts import render
from product.models import Product, Comment, Rate, Category
from user.models import Costumer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError

def products(request):
    products_ = Product.objects.all()
    products_list = []
    for product in products_:
        product_dict = {
            'name' : product.name,
            'price' : product.price,
            'category' : product.category.name,
            'description' : product.description,
            'stock' : product.stock,
        }
        products_list.append(product_dict)
    return JsonResponse(products_list, safe=False)

def products_comments(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product)
    comments_list = []
    for comment in comments:
        comment_dict = {
            'comment' : comment.comment_text,
            'costumer' : comment.costumer.name,
            'product' : comment.product.name,
        }
        comments_list.append(comment_dict)
    return JsonResponse(comments_list, safe=False)

def rate_product(request, product_id):
    product = Product.objects.get(id=product_id)
    rates = Rate.objects.filter(product=product)
    i = 0
    ssum = 0
    for rate in rates:
        i += 1
        ssum += rate.rate
    if i == 0:
        return JsonResponse({'message' : 'no rate for this product'}, safe=False)
    else :
        return JsonResponse({'rate' : round(ssum/i, 2)})
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            comment = Comment.objects.create(
                comment_text = data['comment'],
                costumer = Costumer.objects.get(id=data['costumer_id']),
                product = Product.objects.get(id=data['product_id']),
            )
            comment.save()
            return JsonResponse({'message' : 'comment added successfully'}, safe=False)
        except IntegrityError:
            return JsonResponse({'message' : 'comment already exists'}, safe=False)
        except KeyError:
            return JsonResponse({'message' : 'please check the data you sent'}, safe=False)
    else:
        return JsonResponse({'message' : 'please send a POST request'}, safe=False)
@csrf_exempt   
def add_rate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rate = Rate.objects.create(
                rate = data['rate'],
                costumer = Costumer.objects.get(id=data['costumer_id']),
                product = Product.objects.get(id=data['product_id']),
            )
            rate.save()
            return JsonResponse({'message' : 'rate added successfully'}, safe=False)
        except IntegrityError:
            return JsonResponse({'message' : 'rate already exists'}, safe=False)
        except KeyError:
            return JsonResponse({'message' : 'please check the data you sent'}, safe=False)
        except Costumer.DoesNotExist:
            return JsonResponse({'message' : 'costumer does not exist'}, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'product does not exist'}, safe=False)
    else:
        return JsonResponse({'message' : 'please send a POST request'}, safe=False)
@csrf_exempt
def add_product(request):
    if request.method == "POST":
        
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                name = data['name'],
                description = data['description'],
                price = data['price'],
                stock = data['stock'],
                category = Category.objects.get(id=data['category_id']),
            )
            product.save()
            return JsonResponse({'message' : 'product added successfully'}, safe=False)
        except IntegrityError:
            return JsonResponse({'message' : 'product already exists'}, safe=False)
        except KeyError:
            return JsonResponse({'message' : 'please check the data you sent'}, safe=False)
        except Category.DoesNotExist:
            return JsonResponse({'message' : 'category does not exist'}, safe=False)
    else:
        return JsonResponse({'message' : 'please send a POST request'}, safe=False)
    

def get_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product_dict = {
            'name' : product.name,
            'price' : product.price,
            'category' : product.category.name,
            'description' : product.description,
        'stock' : product.stock,
        }
        return JsonResponse(product_dict, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'message' : 'product does not exist'}, safe=False)

