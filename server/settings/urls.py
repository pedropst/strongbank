from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from strongbank.views import ClienteViewset, ContaViewset, DepositarViewset, ExtratoViewset, SacarViewset, TransferirViewset, SaldoViewset, UserCreate, UserDetail, UserList, CartaoViewset, FaturaViewset, PagarCreditoViewset, PagarDebitoViewset
# from strongbank.views import ClienteViewset, ContaViewset

router = routers.DefaultRouter()
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
    path('users/', UserList.as_view()),
    path('usercreate/', UserCreate.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]

