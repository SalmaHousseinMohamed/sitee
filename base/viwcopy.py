from django.shortcuts import render, redirect, get_object_or_404
from .models import Category,Image,Product ,User ,Comment
from .forms import ProductForm, UserForm, MyUserCreationForm ,AuthenticationForm ,CommentForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from social_django.models import UserSocialAuth
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def signup_view(request):
    if 'google-oauth2' in request.POST:
        # This is a Google OAuth2 callback
        social = UserSocialAuth.get_social_auth_for_user(request.user, 'google-oauth2')
        if social:
            # The user authenticated with Google, you can log them in
            login(request, social.user)
            return redirect('index')  # Redirect to your home page
        else:
            # Handle the case where the OAuth2 callback didn't work as expected
            return redirect('signup')  # Redirect to the signup page with an error message
    elif request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to your home page after standard signup
    else:
        form = MyUserCreationForm()
    return render(request, 'base/signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if 'google-oauth2' in request.POST:
        # This is a Google OAuth2 callback
        social = UserSocialAuth.get_social_auth_for_user(request.user, 'google-oauth2')
        if social:
            # The user authenticated with Google, you can log them in
            login(request, social.user)
            return redirect('index')  # Redirect to your home page
        else:
            # Handle the case where the OAuth2 callback didn't work as expected
            error_message = "Google login failed. Please try again."
            return render(request, 'base/login.html', {'error_message': error_message})

    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to your home page after standard login
        else:
            # Handle the case of invalid login credentials
            error_message = "Invalid username or password. Please try again."
            return render(request, 'base/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    
    return render(request, 'base/login.html', {'form': form})

def login_form_view(request):
    return render(request, 'base/login.html')

def signup_form_view(request):
    return render(request, 'base/signup.html')

def login_form_view(request):
    return render(request, 'base/login.html')

def signup_form_view(request):
    return render(request, 'base/signup.html')

def logoutUser(request):
    logout(request)
    return redirect('index')

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    return render(request, 'base/index.html', {'categories': categories, 'products': products})

def product_form(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.advertiser = request.user
            product.save()

            # Save multiple images associated with the product
            for image_file in request.FILES.getlist('images'):
                Image.objects.create(product=product, image=image_file)

            # Redirect to the product detail page for the newly created product
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(initial={'category': category})
    return render(request, 'base/category_products.html', {'form': form, 'category': category})
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.filter(product=product)
    advertiser = product.advertiser

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, 'Invalid comment. Please try again.')

    else:
        form = CommentForm()

    return render(request, 'base/ad_detail.html', {'product': product, 'advertiser': advertiser, 'comments': comments, 'form': form})
def search_products(request):
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    category_id = request.GET.get('category')
    
    # Create a base query for products
    products = Product.objects.all()
    
    # Apply filters based on search criteria
    if keyword:
        # Use Q objects for OR-like queries
        products = products.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    
    if location:
        products = products.filter(location__icontains=location)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, 'base/search_results.html', {'products': products})






@login_required(login_url='login')
def add_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = CommentForm()
    
    comments = Comment.objects.filter(product=product)

    return render(request, 'base/ad_details.html', {'product': product, 'comments': comments, 'form': form})


def update_profile(request, username):
    user = User.objects.get(username=username)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')  # Add a success message
            return redirect('view_profile', username=username)
        else:
            messages.error(request, 'Profile update failed. Please correct the errors.')  # Add an error message if the form is not valid
    else:
        form = UserForm(instance=user)
    
    return render(request, 'base/update_profile.html', {'form': form, 'user': user})


def view_profile(request, username):
    user = User.objects.get(username=username)
    products = Product.objects.all()  # Fetch all products
    return render(request, 'base/profile.html', {'user': user,'products': products})


def view_advertiser_profile(request, username):
    user = User.objects.get(username=username)
    products = Product.objects.filter(advertiser=user)
    
    return render(request, 'base/view_advertiser_profile.html', {'advertiser': user, 'products': products})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_profile.html', {'form': form})



@login_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Ensure that only the user who posted the product can delete it
    if product.advertiser != request.user:
        messages.error(request, "You don't have permission to delete this product.")
        return redirect('product_detail', product_id=product_id)

    if request.method == 'POST':
        # Delete the product and associated images
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('view_profile', username=request.user.username)  # Redirect to the user's profile page


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        comment.delete()
        return redirect('index')
    return render(request, 'base/delete.html', {'obj': comment})