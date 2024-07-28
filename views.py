from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import Category,SubCategory,Product
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_view(request):
    return render(request, 'admin_dash.html')

@login_required
def user_view(request):
    return render(request, 'user.html')
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
    products = Product.objects.filter(subcategory__category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})
