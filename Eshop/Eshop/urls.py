from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings


from MainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home),
    path('shop/<str:cn>/',views.Shop),
    path('product/<int:num>/',views.ProductDetails),
    path('cart/',views.CartDetails),
    path('checkout/',views.CheckoutForm),
    path('login/',views.Login),
    path('signup/',views.SignUp),
    path('addproduct/',views.AddProduct),
    path('adminpage/',views.AdminPage),
    path('logout/',views.logout),
    path('cartdelete/<str:num>/', views.CartDelete),
    path('delete/<str:num>/',views.DeleteProduct),
    path('edit/<int:num>',views.editProduct),
    path('orderplace/',views.OrderPlaced),
    path('pastorder/', views.PastOrders),
    path('Previousorders/', views.PastOrders2),
    path('orderadmin/', views.OrderAdmin),
    path('dispatchedorder/<str:num>/', views.DispatchedOrder),

    #    path('handlerequest/',my.handlerequest,name='HandleRequest'),
 #   path('payment/', include(('payment.urls','payment'),namespace='payment')),
 #   path('paypal/',include('paypal.standard.ipn.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #pip install django-paypal
]
urlpatterns=urlpatterns+staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)