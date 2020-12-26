from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    reverse)
from django.contrib import messages

from books.models import Book

# Create your views here.


def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        cart = request.session.get('shopping_cart', {})
        if book_id not in cart:
            book = get_object_or_404(Book, pk=book_id)
            cart[book_id] = {
                'id': book_id,
                'title': book.title,
                'category': str(book.category),
                'price': book.price,
                'qty': 1,
                'subtotal': book.price,
            }
            request.session['shopping_cart'] = cart
            messages.success(
                request, f"Book - {book.title} has been added to cart!")
            return redirect(reverse('view_cart'))
        else:
            book = get_object_or_404(Book, pk=book_id)
            cart[book_id]['qty'] += 1
            cart[book_id]['subtotal'] += book.price
            request.session['shopping_cart'] = cart
            messages.success(
                request, f"Book {book.title} quantity increased by 1")
            return redirect(reverse('view_cart'))
    else:
        messages.warning(request, "Kindly log in to purchase items !")
        return redirect('account_login')


def view_cart(request):
    books_nav = Book.objects.order_by('-release_date')[:2]
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for item in cart:
        grand_total += cart[item]['subtotal']

    return render(request, 'cart/view_cart.template.html', {
        'shopping_cart': cart,
        'grand_total': grand_total,
        'books_nav': books_nav,
    })


def minus_from_cart(request, book_id):
    cart = request.session.get("shopping_cart", {})
    if book_id in cart:
        book = get_object_or_404(Book, pk=book_id)
        cart[book_id]['qty'] -= 1
        cart[book_id]['subtotal'] -= book.price
        request.session["shopping_cart"] = cart
        if cart[book_id]['qty'] == 0:
            del cart[book_id]
            request.session["shopping_cart"] = cart
            messages.warning(
                request, f"Item {book.title} removed from cart !")
            return redirect(reverse('view_cart'))
        else:
            messages.warning(
                request, f"Reduce {book.title} quantity by 1 !")
            return redirect(reverse('view_cart'))
    else:
        return redirect(reverse('homepage'))


def remove_from_cart(request, book_id):
    cart = request.session.get("shopping_cart", {})
    if book_id in cart:
        book = get_object_or_404(Book, pk=book_id)
        del cart[book_id]
        request.session["shopping_cart"] = cart
        messages.error(request, f"Item {book.title} removed from cart !")
        return redirect(reverse('view_cart'))
