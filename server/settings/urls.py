from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from strongbank.views.cartao_viewset import CartaoViewset, PagarCreditoViewset, PagarDebitoViewset
from strongbank.views.cliente_viewset import ClienteViewset
from strongbank.views.conta_viewset import ContaViewset, DepositarViewset, ExtratoViewset, SacarViewset, TransferirViewset, SaldoViewset
from strongbank.views.fatura_viewset import FaturaViewset
from strongbank.views.login_viewset import LoginViewset
from strongbank.views.user_viewset import UserViewset


router = routers.DefaultRouter()
router.register(r'login', LoginViewset, basename='Login')
router.register(r'user', UserViewset, basename='User')
router.register(r'cliente', ClienteViewset, basename='Cliente')
router.register(r'conta', ContaViewset, basename='Conta')
router.register(r'sacar', SacarViewset, basename='Sacar')
router.register(r'depositar', DepositarViewset, basename='Depositar')
router.register(r'transferir', TransferirViewset, basename='Transferir')
router.register(r'saldo', SaldoViewset, basename='Saldo')
router.register(r'extrato', ExtratoViewset, basename='Extrato')
router.register(r'cartao', CartaoViewset, basename='Cartao')
router.register(r'fatura', FaturaViewset, basename='Fatura')
router.register(r'pagarcredito', PagarCreditoViewset, basename='PagarCredito')
router.register(r'pagardebito', PagarDebitoViewset, basename='PagarDebito')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('users/', UserList.as_view()),
    # path('usercreate/', UserCreate.as_view()),
    # path('users/<int:pk>/', UserDetail.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]

