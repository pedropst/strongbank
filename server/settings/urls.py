from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from strongbank.views import ClienteViewSet, ContaViewSet, DepositarViewSet, ExtratoViewset, SacarViewSet, TransferirViewSet, SaldoViewSet, UserCreate, UserDetail, UserList
# from strongbank.views import ClienteViewSet, ContaViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='Cliente')
router.register(r'contas', ContaViewSet, basename='Conta')
router.register(r'sacar', SacarViewSet, basename='Sacar')
router.register(r'depositar', DepositarViewSet, basename='Depositar')
router.register(r'transferir', TransferirViewSet, basename='Transferir')
router.register(r'saldo', SaldoViewSet, basename='Saldo')
router.register(r'extrato', ExtratoViewset, basename='Extrato')

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

