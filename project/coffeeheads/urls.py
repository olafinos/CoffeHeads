from .views import (
    HomeView,
    CoffeeList,
    UserCoffeeHistoryList,
    CoffeeDetail,
    UserCoffeeHistoryDetail,
    AddUserCoffee,
    TopUsersView
)
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("coffeeheads/", HomeView.as_view(), name="coffeeheads"),
    path("coffeeheads/coffee_list/", CoffeeList.as_view(), name="coffee_list"),
    path("coffeeheads/user/<int:pk>", UserCoffeeHistoryList.as_view(), name="user_coffee_list"),
    path("coffeeheads/coffee/<int:pk>", CoffeeDetail.as_view(), name="coffee_detail"),
    path(
        "coffeeheads/my_coffee/<int:pk>", UserCoffeeHistoryDetail.as_view(), name="user_coffee_detail"
    ),
    path(
        "coffeeheads/coffee/<int:pk>/add_to_history", AddUserCoffee.as_view(), name="add_user_coffee"
    ),
    path("coffeeheads/top_users", TopUsersView.as_view(),name="top_users_list")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
