from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product, Customer


# Create your views here.
def aview(request):
    customers = Customer.objects.filter(
        Q(first_name__startswith="A") & Q(last_name__contains="in")
    )
    return render(request, "indexx.html", {"customers": list(customers)})
