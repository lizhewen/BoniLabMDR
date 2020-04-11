from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('bsp-plot/', views.plot_bsp, name='bsp-plot'),
    path('geno-plot/', views.plot_geno, name='geno-plot'),
    path('auc-plot/', views.plot_auc, name='auc-plot'),
    path('auc-plot/<yearChosen>/', views.plot_auc, name='auc-plot'),
    path('multi-bsp-plot/', views.multi_plot_bsp, name='multi-bsp-plot'),
    path('multi-geno-plot/', views.multi_plot_geno, name='multi-geno-plot'),
    path('multi-cyc-plot/', views.multi_plot_cyc, name='multi-cyc-plot'),
]