from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item, ItemReview, CartItem
from .forms import CustomRegisterForm, CustomLoginForm

def home(request):
    items = Item.objects.all()

    # 1. კატეგორიების და ბრენდების ამოღება დროფდაუნისთვის
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
        
    # ფასის ლოგიკა დაცვით (მინ >= 0 და მინ <= მაქს)
    if min_price or max_price:
        try:
            min_p = float(min_price) if min_price else 0
            max_p = float(max_price) if max_price else 999999
            if min_p < 0: min_p = 0
            if max_p < 0: max_p = 0
            if min_p > max_p:
                # თუ მომხმარებელმა შეცდომით მინიმალური მეტი ჩაწერა, ვუცვლით ადგილებს
                min_p, max_p = max_p, min_p
            items = items.filter(price__gte=min_p, price__lte=max_p)
        except ValueError:
            pass
            
    # რეიტინგით გაფილტვრა (დაცვა 1-ზე ნაკლებზე)
    if min_rating:
        try:
            rating_val = float(min_rating)
            if rating_val < 1: rating_val = 1.0
            items = [item for item in items if item.average_rating >= rating_val]
        except ValueError:
            pass

    # 2. Pagination ლოგიკა (6 ნივთი თითო გვერდზე)
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
        'brands': brands,
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
            item=item, reviewer_name=reviewer_name,
            rating_stars=int(rating_stars), comment=comment
        )
        return redirect('item_detail', pk=item.id)
    return render(request, 'detail.html', {'item': item})

# კალათის ახალი ლოგიკა (მონაცემთა ბაზაზე დაფუძნებული)
@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required(login_url='login')
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, user=request.user, item_id=item_id)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    return redirect('cart_view')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    CartItem.objects.filter(user=request.user, item_id=item_id).delete()
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