from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item, ItemReview
from .forms import CustomRegisterForm, CustomLoginForm

def home(request):
    items = Item.objects.all()

    # 1. კატეგორიების და ბრენდების ამოღება დროფდაუნისთვის (Dropdown)
    categories = Item.objects.values_list('category', flat=True).distinct()
    brands = Item.objects.values_list('brand', flat=True).distinct()

    # საძიებო და ფილტრაციის პარამეტრები
    search_query = request.GET.get('q')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    if search_query:
        items = items.filter(name__icontains=search_query)
    if category:
        items = items.filter(category=category)
    if brand:
        items = items.filter(brand=brand)
        
    # ფასის ლოგიკა დაცვით (არ შეიძლება უარყოფითი ან მინიმალური > მაქსიმალურზე)
    if min_price and max_price:
        try:
            min_p = float(min_price)
            max_p = float(max_price)
            if min_p > max_p:
                # თუ მომხმარებელმა შეცდომით მინიმალური მეტი ჩაწერა, ვუცვლით ადგილებს
                min_p, max_p = max_p, min_p
            items = items.filter(price__gte=min_p, price__lte=max_p)
        except ValueError:
            pass
    else:
        if min_price:
            items = items.filter(price__gte=min_price)
        if max_price:
            items = items.filter(price__lte=max_price)
            
    # რეიტინგით გაფილტვრა (დაცვა 1-ზე ნაკლებზე)
    if min_rating:
        try:
            rating_val = float(min_rating)
            if rating_val < 1:
                rating_val = 1.0
            items = [item for item in items if item.average_rating >= rating_val]
        except ValueError:
            pass

    # 2. პაგინაციის (Pagination) ლოგიკა (მაგ: 6 ნივთი თითო გვერდზე)
    paginator = Paginator(items, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ვინახავთ ძველ ფილტრებს, რომ გვერდის გადართვისას არ დაიკარგოს
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands, # გადავცემთ ბრენდებს 
        'query_string': query_string,
    }
    return render(request, 'home.html', context)

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST' and 'rating_stars' in request.POST:
        reviewer_name = request.POST.get('reviewer_name')
        rating_stars = request.POST.get('rating_stars')
        comment = request.POST.get('comment', '')
        
        ItemReview.objects.create(
            item=item,
            reviewer_name=reviewer_name,
            rating_stars=int(rating_stars),
            comment=comment
        )
        return redirect('item_detail', pk=item.id)

    return render(request, 'detail.html', {'item': item})

@login_required(login_url='login')
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        try:
            item = Item.objects.get(id=item_id)
            total = item.price * quantity
            total_price += total
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total': total
            })
        except Item.DoesNotExist:
            pass
            
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('cart_view')

@login_required(login_url='login')
def update_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    action = request.POST.get('action')

    if item_id_str in cart:
        if action == 'increase':
            cart[item_id_str] += 1
        elif action == 'decrease':
            cart[item_id_str] -= 1
            if cart[item_id_str] <= 0:
                del cart[item_id_str]

    request.session['cart'] = cart
    return redirect('cart_view')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        del cart[item_id_str]

    request.session['cart'] = cart
    return redirect('cart_view')

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')