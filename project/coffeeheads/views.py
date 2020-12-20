from .forms import OpinionForm
from .models import Coffee, UserCoffee, Opinion
from typing import List
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.db.models import Avg, Count, Max
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import datetime


class HomeView(View):
    def get(self, request: HttpRequest, format=None) -> HttpResponse:
        recent_coffees = Coffee.objects.filter().order_by('-add_date')[:3]
        top_coffees = Coffee.objects.filter().order_by('-average')[:3]
        context = {"recent_coffees": recent_coffees, "top_coffees": top_coffees}
        return render(request, "home.html", context=context)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class UserCoffeeHistoryList(ListView):
    def get(self, request: HttpRequest, pk, format=None) -> HttpResponse:
        user = User.objects.get(pk=pk)
        user_coffees = UserCoffee.objects.filter(owner = user)
        context = {"user_coffees": user_coffees, "user_info" : user}
        return render(request, "user_coffee_list.html", context=context)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class UserCoffeeHistoryDetail(View):
    def get(self, request: HttpRequest, pk, format=None) -> HttpResponse:
        # storage = messages.get_messages(request)
        user_coffee = UserCoffee.objects.get(pk=pk, owner=request.user)
        coffee_opinion = self._get_opinion(user_coffee.coffee, request.user)
        context = {"user_coffee": user_coffee, "coffee_opinion": coffee_opinion}
        return render(request, "user_coffee_detail.html", context=context)

    def _get_opinion(self, coffee: Coffee, user: "User"):
        try:
            coffee_opinions = Opinion.objects.get(user =user, coffee = coffee)
        except Opinion.DoesNotExist:
            coffee_opinions = None
        return coffee_opinions



@method_decorator(login_required(login_url="/login/"), name="dispatch")
class AddUserCoffee(View):
    def get(self, request: HttpRequest, pk, format=None) -> HttpResponse:
        form = OpinionForm()
        return render(request, "add_user_coffee.html", {"form": form, "exists": False})

    def post(self, request: HttpRequest, pk, format=None) -> HttpResponse:
        coffee = Coffee.objects.get(pk=pk)
        user = request.user
        user_coffee = UserCoffee.objects.filter(coffee=coffee, owner= request.user)
        if user_coffee:
            messages.add_message(request,messages.ERROR,"Coffee already added to history")
            return redirect('user_coffee_detail',pk=user_coffee[0].pk)
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.coffee = coffee
            opinion.user = user
            opinion.save()
            user_coffee = self.create_user_coffee(coffee, request.user, opinion)
            self._update_average(coffee)
        else:
            return render(request, "add_user_coffee.html", {'form': form})
        messages.add_message(request,messages.SUCCESS, "Coffee successfully added to history")
        return redirect('user_coffee_detail',pk=user_coffee.pk)

    def create_user_coffee(self, coffee: Coffee, user: "User", opinion: Opinion) -> UserCoffee:
        user_coffee = UserCoffee(owner=user, coffee=coffee, opinion=opinion)
        user_coffee.save()
        return user_coffee

    @staticmethod
    def _update_average(coffee):
        opinions = Opinion.objects.filter(coffee=coffee)
        coffee = Coffee.objects.get(pk=coffee.pk)
        average_rating = opinions.aggregate(Avg('rating'))
        coffee.average = average_rating['rating__avg']
        coffee.reviewed_by += 1
        coffee.save()

class CoffeeDetail(View):
    def get(self, request: HttpRequest, pk, format=None) -> HttpResponse:
        coffee = Coffee.objects.get(pk=pk)
        coffee_opinions = self._get_opinions(coffee)

        context = {"coffee": coffee, "coffee_opinions": coffee_opinions}
        return render(request, "coffee_detail.html", context=context)

    def _get_opinions(self, coffee: Coffee) -> HttpResponse:
        try:
            coffee_opinions = Opinion.objects.filter(coffee=coffee)
        except Opinion.DoesNotExist:
            coffee_opinions = None
        return coffee_opinions


class CoffeeList(ListView):
    model = Coffee
    paginate_by = 20
    template_name = "coffee_list.html"
    ordering = ['name']
    order_mapping = {
        "name": "Alphabetical A-Z",
        "-name": "Alphabetical Z-A",
        "average": "Average ascending",
        "-average" : "Average descending",
        "reviewed_by": "Popularity ascending",
        "-reviewed_by" : "Popularity descending",
        "estimated_price": "Price ascending",
        "-estimated_price": "Price descending"
    }
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'name')
        return ordering

    def get_context_data(self, **kwargs):
        context = super(CoffeeList, self).get_context_data(**kwargs)
        ordering = self.request.GET.get('ordering', 'name')
        order_name = self.order_mapping[ordering]
        context['ordering'] = order_name
        return context

class TopUsersView(View):
    def get(self, request, format=None):
        top_users = UserCoffee.objects.values('owner').annotate(count=Count('owner')).order_by('-count')[:10]
        for user in top_users:
            user['username'] = self._add_username(user_id=user['owner'])
            user['top_rated_coffee'] = self._get_top_rated_coffee(user_id=user['owner'])
        context = {"opinions": top_users}
        return render(request, "top_users.html", context=context)

    def _add_username(self, user_id: int):
        return User.objects.get(pk=user_id).username

    def _get_top_rated_coffee(self,user_id: int):
        user_history = UserCoffee.objects.filter(owner=user_id)
        opinions_info = []
        for coffee in user_history:
            opinion = Opinion.objects.get(pk=coffee.opinion.id)
            opinions_info.append({
                "rating": opinion.rating,
                "coffee_name": opinion.coffee.name,
                "coffee_id": opinion.coffee.id
            })
        return max(opinions_info, key=lambda x: x['rating'])
