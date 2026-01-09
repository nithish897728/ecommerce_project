from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product




  # Default True


from .models import Product, Cart, Order, OrderItem


# ---------------- HOME PAGE ----------------
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


# ---------------- ADD TO CART ----------------

def add_to_cart(request, id):
    print("ADD TO CART VIEW HIT")  # 👈 ADD THIS

    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    print("SESSION CART:", request.session['cart'])  # 👈 ADD THIS

    return redirect('cart')



# ---------------- CART PAGE ----------------
def cart_view(request):
    print("🔥 CART VIEW EXECUTED 🔥")

    session_cart = request.session.get('cart', {})
    print("SESSION CART:", session_cart)

    products = []
    total = 0

    for product_id, quantity in session_cart.items():
        product = Product.objects.get(id=int(product_id))
        product.quantity = quantity
        product.subtotal = product.price * quantity
        total += product.subtotal
        products.append(product)

    print("PRODUCTS LENGTH:", len(products))

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })



# ---------------- INCREASE QTY ----------------
@login_required
def increase_qty(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


# ---------------- DECREASE QTY ----------------
@login_required
def decrease_qty(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


# ---------------- CHECKOUT ----------------
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = 0
    products = []

    for pid, qty in cart.items():
        product = Product.objects.get(id=int(pid))
        subtotal = product.price * qty
        total += subtotal
        products.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )

        for item in products:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['product'].price
            )

        request.session['cart'] = {}  # clear cart
        return redirect('payment_success')

    return render(request, 'store/checkout.html', {
        'products': products,
        'total': total
    })
    





# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'store/login.html')


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cart(request):
    return render(request, 'store/cart.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'store/signup.html', {'form': form})



from django.shortcuts import render

def payment_success(request):
    return render(request, 'store/success.html')










