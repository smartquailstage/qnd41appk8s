from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from sbmcart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'sbmorders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    sbmorder = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/sbmorders/order/detail.html',
                  {'sbmorder': sbmorder})


@staff_member_required
def admin_order_pdf(request, order_id):
    sbmorder = get_object_or_404(Order, id=order_id)
    html = render_to_string('sbmorders/order/pdf.html',
                            {'sbmorder': sbmorder})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(sbmorder.id)
    weasyprint.HTML(string=html,  base_url=request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS('sbmorders/static/css/pdf.css')], presentational_hints=True)
    return response
