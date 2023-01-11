from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('login',views.login),
    path('signup',views.signup),
    path('ShowCakes/<id>',views.ShowCakes),
    path('ViewDetails/<id>',views.ViewDetails),
    path('signout',views.signout),
    path('addToCart',views.addToCart),
    path('ShowAllCartItems',views.ShowAllCartItems),
    path('MakePayment',views.MakePayment),
    path('removeItem',views.removeItem),
]
