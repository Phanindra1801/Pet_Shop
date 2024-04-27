from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("login",views.login,name="login"),
    path("",views.home,name="home"),
    path("dogs",views.dogs,name="dogs"),
    path("cats",views.cats,name="cats"),
    path("birds",views.birds,name="birds"),
    path("fishes",views.fishes,name="fishes"),
    path("rabbits",views.rabbits,name="rabbits"),
    path("gunniepigs",views.gunniepigs,name="gunniepigs"),
    path("shelters",views.shelters,name="shelters"),
    path("medicines",views.medicines,name="medicines"),
    path("signup",views.signup,name="signup"),
    path("checkuserlogin",views.checkuserlogin,name="checkuserlogin"),
    path("logout",views.logout,name="logout"),
    path("temp",views.temp,name="temp"),
    path("owner",views.ownerpage,name="owner"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("rescue",views.rescue,name="rescue"),
    path("deleteuser/<int:uid>",views.deleteuser,name="deleteuser"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("userlogout",views.userlogout,name="userlogout"),
    path("viewproductsinowner", views.viewproductsinowner, name="viewproductsinowner"),
    path("deleteproduct/<int:uid>",views.deleteproduct,name="deleteproduct"),
    path("forgotpassword",views.forgotpassword,name="forgotpassword"),
    path("changepassword",views.changepassword,name="changepassword"),



    path("category/<str:id>",views.getcategory,name="getcategory"),
    path('addcartfun',views.add_cart,name="addcartfun"),
    path('cart/',views.get_cart,name="getcart"),
    path("deletecartproduct/<int:uid>",views.deletecartproduct,name="deletecartproduct"),
    path("clearcartafterpayment",views.clearcartafterpayment,name="clearcartafterpayment"),
    path('update_cart/', views.update_cart, name='update_cart'),

    path("payment", views.payment, name="payment"),
    path("payment-status", views.payment_status, name="payment-status"),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)