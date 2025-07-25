from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),

    ########## catalog##########3
    path('catalog/', views.catalog, name='catalog'),
    path('model/create/', views.model_create, name='model_create'),
    path('model/<str:model_id>/update/', views.model_update, name='model_update'),
    path('model/<str:model_id>/delete/', views.model_delete, name='model_delete'),
    path('model_add_stone/<str:model_id>', views.model_add_stone, name='model_add_stone'),
    path('model_delete_stone/<str:model_id>/<str:stone_full_name>', views.model_delete_stone, name='model_delete_stone'),
    path('model/<str:model_id>/model_add_2_lot/', views.model_add_2_lot, name='model_add_2_lot'),
    ############ lot ############
    path('lot/', views.lot_list, name='lot_list'),
    path('lot/create/', views.lot_create, name='lot_create'),
    path('lot/<str:lot_id>/update/', views.lot_update, name='lot_update'),
    path('lot/<str:lot_id>/delete/', views.lot_delete, name='lot_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
