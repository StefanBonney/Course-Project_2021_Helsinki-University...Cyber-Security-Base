from django.urls import path
#from django.contrib.auth.decorators import login_required


from . import views

app_name = 'CoinMiner'
urlpatterns = [
    # ex: /CoinMiner/
    path('', views.index, name='index'),
    # ex: /CoinMiner/5/
    path('<int:coin_id>/', views.detail, name='detail'),
    # ex: /CoinMiner/5/30/results/
    path('<int:coin_id>/<str:message>/results/', views.results, name='results'),
    # ex: /CoinMiner/5/mine/
    path('<int:coin_id>/mine/', views.mine, name='mine'),
    # ex: /CoinMiner/5/error/
    path('error/', views.error, name='error'),
    # ex: /CoinMiner/5/add/
    path('add/', views.add, name='add'),
]