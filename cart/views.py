from django.shortcuts import render
from product.models import Product, Comment, Rate, Category
from cart.models import Cart
from user.models import Costumer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from order.models import Order, Discount
import uuid
from django.db.models import Sum
@csrf_exempt
def add_product_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            costumer = Costumer.objects.get(username=data['costumer_username'])
            cart = Cart.objects.get(costumer = costumer, is_finalized = False)
            product = Product.objects.get(id = data['product_id'])
            cart.products.add(product)
            cart.save()
            return JsonResponse({"success": "Product added to cart"})
        except Costumer.DoesNotExist:
            return JsonResponse({"error": "Costumer does not exist"})
        
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product does not exist"})
        
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Cart does not exist"})
        
        except IntegrityError:
            return JsonResponse({"error": "Product already in cart"})

    return JsonResponse({"error": "request must be post"})

@csrf_exempt
def remove_product_from_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            costumer = Costumer.objects.get(username=data['costumer_username'])
            cart = Cart.objects.get(costumer = costumer, is_finalized = False)
            product = Product.objects.get(id = data['product_id'])
            if product not in cart.products.all():
                return JsonResponse({'error': 'Product not found in cart'}, status=400)
            cart.products.remove(product)
            cart.save()
            return JsonResponse({"success": "Product removed from cart"})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'No active cart found for this customer'}, status=404)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Request must be POST'}, status=405)

def generate_unique_order_code():
    while True:
        code = str(uuid.uuid4())[:16]  # Generate a random 16-character string
        if not Order.objects.filter(code=code).exists():
            return code

def generate_unique_cart_code():
    while True:
        code = str(uuid.uuid4())[:16]
        if not Cart.objects.filter(code = code).exists():
            return code


@csrf_exempt  
def finalize_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            costumer = Costumer.objects.get(username=data['costumer_username'])
            cart = Cart.objects.get(costumer = costumer, is_finalized = False)
            if not cart.products.exists():
                return JsonResponse({"error": "Cart is empty, cannot finalize"}, status=400)
            cart.is_finalized = True
            cart.save()
            order = Order.objects.create(
                code=generate_unique_order_code(),  # Assuming a function to generate a unique order code
                costumer=costumer,
                cart=cart,
                is_received=False 
            )
            order.products.set(cart.products.all())
            order.save()
            new_cart = Cart.objects.create(
                code=generate_unique_cart_code(),  # Assuming a function to generate a unique cart code
                costumer=costumer,
                is_finalized = False,
            )
            new_cart.save()
            return JsonResponse({"success": "Cart finalized and order created and a new empty cart is created for the costumer", "order_code": order.code}, status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'No active cart found for this customer'}, status=404)
        
        except Costumer.DoesNotExist:
            return JsonResponse({'error': 'Customer does not exist'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt   
def view_active_cart(request, costumer_username):
    try:
        costumer = Costumer.objects.get(username=costumer_username)
        cart = Cart.objects.get(costumer = costumer, is_finalized = False)
        total_price = cart.products.aggregate(total=Sum('price'))['total'] or 0
        
        return JsonResponse({
                            "products": cart.products.values('name'),
                            "bill" : total_price
                             },status=200)
    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    