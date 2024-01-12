from django.urls import path
from . import views 

urlpatterns = [
    path('product_form/<int:category_id>/', views.product_form, name='product_form'),
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('product/<int:product_id>/add_comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/update/', views.update_profile, name='update_profile'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('search/', views.search_products, name='search_products'),
    path('view_advertiser_profile/<str:username>/', views.view_advertiser_profile, name='view_advertiser_profile'),
    path('categories/<int:category_id>/',views.product_list, name='product_list'),

]


