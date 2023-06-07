from django.contrib.auth.decorators import login_required
from django.urls import path, include
from apps.views import *
from apps.models import User
from django.urls import include, path
from apps.serializers import router





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    path('', index, name="main"),
    path('login/', Login.as_view(), name='login'),
    path('singup/', SingUpView.as_view(), name='signup'),
    path('profile/', login_required(PorfileView.as_view()), name='profile'),
    path('edit/<int:pk>', login_required(UpdateProfileView.as_view()), name='edit'),
    path('about/', AboutPageView, name='about'),
    path('logout/', Logout.as_view(), name='logout'),
    path('cart/', Cart, name='cart'),
    path('chekout/', Checkout, name='checkout'),
    path('update_item/', UpdateItem, name='update_item'),
    path('apps/', include(router.urls)),
    path('redoc/', redoc, name='redoc'),
]
