from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
     path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('admin/webpage/catalog/', views.admin_catalog, name='admin_catalog'),
    path('catalog_custom/', views.catalog_custom, name='catalog_custom'),
    path('catalog/', views.catalog_list, name='catalog_list'),
    path('catalog/create/', views.catalog_create, name='catalog_create'),
    path('catalog/<str:model_id>/update/', views.catalog_update, name='catalog_update'),
    path('catalog/<str:model_id>/delete/', views.catalog_delete, name='catalog_delete'),

    # path('delete_record/<str:model_id>/<str:reference_name>', views.delete_record, name='delete_record'),
    # path('test_form/<str:model_id>/<str:stone_full_name>', views.test_form, name='test_form'),
    # # path('test/', views.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
