from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #path('admin/', include('admin_adminlte.urls')),    
    path('', include('fazenda.urls')),
    # path('admin/', admin.site.urls),
    path('fertilizantes/', include('fertilizantes.urls')),
    path('usuarios/', include('usuarios.urls')),
    
]
