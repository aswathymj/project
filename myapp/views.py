from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import Category,SubCategory,Product,Cart,Payment
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import paypalrestsdk
from django.conf import settings
import razorpay
# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_view(request):
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    

    context = {
        'category_count': category_count,
        'product_count': product_count,
        
        'username': request.user.username,
    }

    return render(request, 'admin_dash.html', context)
   

@login_required
def user_view(request):
    return render(request, 'user.html', {'user': request.user})
@login_required
def technician_view(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['semail']
        password = request.POST['spassword']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_view')
            elif user.role == 'user':
                return redirect('user_view')
            elif user.role == 'technician':
                return redirect('technician_view')
        else:
            return render(request, 'login.html', {'msg': 'Invalid email or password'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role']
        password = request.POST['password']
        
        user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=name, phone=phone, address=address, role=role)
        user.save()
        return redirect('login')
        
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        if not name:
            messages.error(request, 'Category name is required.')
        elif not image:
            messages.error(request, 'Image is required.')
        else:
            category = Category(name=name, image=image)
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add_category')
    
    return render(request, 'add_category.html')

def accessories(request):
    categories = Category.objects.all()
    products = Product.objects.all()  # Fetch all products
    context = {
        'categories': categories,
        'products': products  # Add all products to the context
    }
    return render(request, 'accessories.html', context)
def view_category(request):
    categories = Category.objects.all()
    return render(request, 'view_category.html', {'categories': categories})

def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found.')
    return redirect('view_category')   
def add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        brand = request.POST.get('brand')
        
        if not category_id:
            messages.error(request, "Category is required.")
        elif not brand:
            messages.error(request, "Brand is required.")
        else:
            try:
                category = Category.objects.get(id=category_id)
                SubCategory.objects.create(category=category, brand=brand)
                messages.success(request, "SubCategory added successfully.")
                return redirect('add_subcategory')
            except Category.DoesNotExist:
                messages.error(request, "Invalid category selected.")
    
    categories = Category.objects.all()
    return render(request, 'add_subcategory.html', {'categories': categories})
def view_subcategory(request):
    subcategories = SubCategory.objects.select_related('category').all()
    context = {
        'subcategories': subcategories
    }
    return render(request, 'view_subcategory.html', context)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')

        if not name:
            messages.error(request, 'Category name is required.')
        else:
            category.name = name
            if image:
                category.image = image
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('view_category')

    return render(request, 'edit_category.html', {'category': category})

def edit_subcategory(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        brand = request.POST.get('brand')

        if not category_id:
            messages.error(request, 'Category is required.')
        elif not brand:
            messages.error(request, 'Brand is required.')
        else:
            try:
                category = Category.objects.get(id=category_id)
                subcategory.category = category
                subcategory.brand = brand
                subcategory.save()
                messages.success(request, 'SubCategory updated successfully.')
                return redirect('view_subcategory')
            except Category.DoesNotExist:
                messages.error(request, 'Invalid category selected.')

    return render(request, 'edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})
# Delete SubCategory View
def delete_subcategory(request,id):
    try:
        subcategory = SubCategory.objects.get(id=id)
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully.')
    except Subcategory.DoesNotExist:
        messages.error(request, 'Subcategory not found.')
    return redirect('view_subcategory')

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        subcategory_id = request.POST.get('subcategory')
        image = request.FILES.get('image')

        # Validation
        if not all([name, description, price, quantity, subcategory_id, image]):
            messages.error(request, "All fields are required.")
            return redirect('add_product')

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messages.error(request, "Invalid price or quantity.")
            return redirect('add_product')

        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            product = Product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                image=image,
                subcategory=subcategory
            )
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('add_product')
        except SubCategory.DoesNotExist:
            messages.error(request, "Invalid subcategory.")
            return redirect('add_product')

    # Handle GET request
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, 'add_product.html', {
        'categories': categories,
        'subcategories': subcategories
    })

def view_product(request):
    products = Product.objects.all()
    return render(request, 'view_product.html', {'products': products})
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.subcategory = SubCategory.objects.get(id=request.POST['subcategory'])

        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('view_product')

    subcategories = SubCategory.objects.all()
    return render(request, 'edit_product.html', {'product': product, 'subcategories': subcategories})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('view_product')
def get_subcategories(request):
    category_id = request.GET.get('category_id')  # Get the category_id from the request
    if category_id:
        # Filter subcategories based on the selected category
        subcategories = SubCategory.objects.filter(category_id=category_id)
        # Prepare the data to send as JSON response
        data = list(subcategories.values('id', 'brand'))  # Change 'brand' to the appropriate field
        return JsonResponse(data, safe=False)  # Return JSON response
    else:
        return JsonResponse([], safe=False) 

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Exclude the current product from the list
    related_products = Product.objects.exclude(id=product_id)
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'product_detail.html', context)
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        

        # Check if the cart item already exists
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # If the item already exists, update the quantity
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('view_cart')
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    grand_total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
    })
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')
@login_required
def buy_now(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    amount = cart_item.product.price * cart_item.quantity
    payment = Payment.objects.create(
        cart=cart_item,
        amount=amount,
        status='Pending'
    )
    # Redirect to a page that displays the product details from the payment
    return redirect('payment_detail', payment_id=payment.id)

@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payment_detail.html', {'payment': payment})
@csrf_exempt
@login_required
def update_user_details(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=request.user.pk)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.pincode = request.POST.get('pincode', user.pincode)
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def create_paypal_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('paypal_execute')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancelled'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Item Name",
                        "sku": "item",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "This is the payment transaction description."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            return render(request, 'payment_error.html', {'error': payment.error})
    return redirect('index')

def execute_paypal_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_error.html', {'error': payment.error})

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def payment_details(request):
    # Fetch payment details for rendering
    payment = Payment.objects.get(id=request.GET.get('payment_id'))  # Adjust as per your logic
    return render(request, 'payment_detail.html', {'payment': payment})

def create_payment(request):
    if request.method == "POST":
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        amount = cart.product.price * cart.quantity  # Calculate amount
        amount_in_paisa = int(amount * 100)  # Convert to paisa
        
        # Create Razorpay Order
        order = client.order.create(dict(
            amount=amount_in_paisa,
            currency='INR',
            payment_capture='1'
        ))
        
        # Create Payment record in DB
        payment = Payment.objects.create(
            cart=cart,
            amount=amount,
            status='Pending'
        )
        
        return JsonResponse({
            'order_id': order['id'],
            'amount': amount_in_paisa
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def verify_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            payment = Payment.objects.get(id=payment_id)
            payment.status = 'Completed'
            payment.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)})
    return JsonResponse({'error': 'Invalid request'}, status=400)