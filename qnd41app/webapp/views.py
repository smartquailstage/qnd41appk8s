from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .models import solutions, solutions_categories
from solutions_blog.models import BlogPage
from .models import SolutionsBlogPage, JobsFormDetailOpeningPage
from .forms import CVCreateForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'webapp/products/smartbusinessmedia/index/smartbusinesmedia.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def CV_Detail(request):
    # Handle file upload
    if request.method == 'POST':
        cv_form = CVCreateForm(request.POST, request.FILES)
        if cv_form.is_valid():
            newdoc = JobsFormDetailOpeningPage(uploadcv = request.FILES['uploadcv'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('webapp.views.CV_Detail'))
    else:
        cv_form = CVCreateForm() # A empty, unbound form

    # Load documents for the list page
    documents = JobsFormDetailOpeningPage.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'webapp/jobdetailopening.html',
        {'documents': documents, 'cv_form': cv_form},
        context_instance=RequestContext(request)
    )




def blog_index(request):
    posts = SolutionsBlogPage.objects.live().public().order_by('-date')
    return render(request, 'webapp/solutions/solutions_carousel.html', {
        'posts': posts,
    })

def blog_post(request, slug):
    post = SolutionsBlogPage.objects.live().public().get(slug=slug)
    return render(request, 'webapp/solutions/solutions_carousel.html', {
        'post': post,
    })


def solution_items(request):
    solution = solutions_categories.objects.live().public().order_by('-date ')
    return render(request, 'solutions/meet_solutions.html', {'solution':solution})

def solutions_items(request):
    solutions = solutions_categories.objects.live().public().order_by('category')
    return render(request, 'solutions/meet_solutions.html', {'solutions':solutions})