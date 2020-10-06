from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Count
from django.contrib.auth.models import Group, User
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .email import Email
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .forms import ContactForm

def home(request):
    return render(request, 'shop/home.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,'shop/product/detail.html',
                  {'product': product,
                  'cart_product_form':cart_product_form})

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_email = form.cleaned_data['email']
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop:product_list')
            else:
                return redirect('accounts:signup')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html',{'form':form })

def signoutView(request):
    logout(request)
    return redirect('signin')

def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('/profile')
    
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request,'accounts/edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        
        else:
            return redirect('/change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'accounts/change_password.html', args)

def success(request):
    return render(request, 'shop/success.html')

def contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            template = get_template('shop/contact_form.txt')
            context = {
                'contact_name' : contact_name,
                'contact_email' : contact_email,
                'contact_content' : contact_content,
            }
            
            content = template.render(context)

            email = EmailMessage(
                "New contact form email",
                content,
                "Creative web" + '',
                ['hamis9474@gmail.com'],
                headers = { 'Reply To': contact_email }
            )

            email.send()

            return redirect('/success')
    return render(request, 'shop/contact.html', {'form':Contact_Form })

