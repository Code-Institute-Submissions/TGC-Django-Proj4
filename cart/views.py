from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages

from books.models import Book, Category

# Create your views here.


def add_to_cart(request, book_id):
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
        messages.success(request, "Book has been added to cart!")
        return redirect(reverse('view_cart'))
    else:
        book = get_object_or_404(Book, pk=book_id)
        cart[book_id]['qty'] += 1
        cart[book_id]['subtotal'] += book.price
        request.session['shopping_cart'] = cart
        return redirect(reverse('view_cart'))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for item in cart:
        grand_total += cart[item]['subtotal']

    return render(request, 'cart/view_cart.template.html', {
        'shopping_cart': cart,
        'grand_total': grand_total,
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
            messages.success(request, "Item removed from cart successfully!")
            return redirect(reverse('homepage'))
        else:
            messages.success(request, "Reduce qty of item by 1 successfully!")
            return redirect(reverse('view_cart'))
    else:
        return redirect(reverse('homepage'))


def remove_from_cart(request, book_id):
    cart = request.session.get("shopping_cart", {})
    if book_id in cart:
        del cart[book_id]
        request.session["shopping_cart"] = cart
        messages.success(request, "Item removed from cart successfully!")
        return redirect(reverse('homepage'))
