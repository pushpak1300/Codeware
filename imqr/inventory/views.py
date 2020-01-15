from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from .models import Item
from .forms import LoginForm, RegisterForm


# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(data=request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#             print(form.cleaned_data)
#             user = authenticate(username=cd['username'], password=cd['password'])
#
#             if user is not None:
#                 login(request, user)
#                 return render(request, "inventory/item_form.html")
#     else:
#         loginform = LoginForm()
#     return render(request, "inventory/registration/login.html", {"loginform": loginform})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'inventory/registration/register.html', {"form": form})


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['name', 'serial_number', 'category', 'details']
    success_url = '/items/create_item'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("login")

    def test_func(self):
        post = self.get_object()  # This will return the post which we are going to update
        if post.author == self.request.user:
            return True
        return False
