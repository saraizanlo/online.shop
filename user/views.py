from django.shortcuts import render
from user.models import Costumer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from cart.views import generate_unique_cart_code
from cart.models import Cart
def costumers(request):
    costumers_ = Costumer.objects.all()
    costumers_list = []
    for costumer in costumers_:
        costumer_dict = {
            "name": costumer.name,
            "last_name": costumer.last_name,
            "email": costumer.email,
            "phone_number": costumer.phone_number,
            'city' : costumer.city,
            'address' : costumer.address
        }
        costumers_list.append(costumer_dict)
    return JsonResponse(costumers_list, safe=False)
@csrf_exempt
def add_costumer(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body['name']
            last_name = body['last_name']
            username = body['username']
            email = body['email']
            phone_number = body['phone_number']
            city = body['city']
            address = body['address']
            password = body['password']
            if Costumer.objects.filter(email=email).exists():
                return JsonResponse({'error': 'A customer with this email already exists.'}, status=400)

            if Costumer.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'error': 'A customer with this phone number already exists.'}, status=400)
            
            if Costumer.objects.filter(username=username).exists():
                return JsonResponse({'error': 'A customer with this username already exists.'}, status=400)

            costumer = Costumer.objects.create(name=name,
                                                last_name=last_name,
                                                username=username, 
                                                email=email, 
                                                phone_number=phone_number, 
                                                city=city, 
                                                address=address, 
                                                password=make_password(password),
                                                wallet = 0
                                                )
            costumer.save()

            new_cart = Cart.objects.create(
                code=generate_unique_cart_code(),  # Assuming a function to generate a unique cart code
                costumer=costumer,
                is_finalized = False,
            )
            new_cart.save()
            return JsonResponse({'message': 'Customer added successfully', 'costumer_id': costumer.id}, status=201)


        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
    else :
        return JsonResponse({'error' : 'invalid request method'}, status = 405)
@csrf_exempt    
def add_money_to_wallet(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            costumer_id = body['costumer_id']
            added_money = body['added_money']
            if added_money <= 0:
                return JsonResponse({'error': 'Invalid amount. It should be a positive number.'}, status=400)
            costumer = Costumer.objects.get(id=costumer_id)
            costumer.wallet += added_money
            costumer.save()
            return JsonResponse({'message': 'Money added successfully'}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error' : 'invalid request method'}, status = 405)

@csrf_exempt
def update_costumer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            costumer_id = data['costumer_id']
            costumer =  Costumer.objects.get(id=costumer_id)
            
            costumer.name = data.get('name', costumer.name)
            costumer.last_name = data.get('last_name', costumer.last_name)
            costumer.email = data.get('email', costumer.email)
            costumer.phone_number = data.get('phone_number', costumer.phone_number)
            costumer.city = data.get('city', costumer.city)
            costumer.address = data.get('address', costumer.address)
            costumer.save()

            return JsonResponse({'message': 'Customer updated successfully'}, status=200)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_costumer(request, costumer_id):
    try:
        costumer = Costumer.objects.get(id=costumer_id)
        costumer_dict = {
            "first_name": costumer.name,
            "last_name": costumer.last_name,
            "email": costumer.email,
            "phone_number": costumer.phone_number,
            "city": costumer.city,
            "address": costumer.address
        }
        return JsonResponse(costumer_dict, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            email = body['email']
            new_password = body['new_password']

            costumer = Costumer.objects.get(email=email)
            costumer.password = make_password(new_password)
            costumer.save()

            return JsonResponse({'message': 'Password reset successfully'}, status=200)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


    
