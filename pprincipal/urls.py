"""pprincipal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portafolio.views import (
    Inicio, perfilportafolio, CrearPortafolio, InfoPerfilDetalle,
    VerDetalleProyecto,signup, signin,signout,contacto,verIps

)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Inicio.as_view(), name="inicio"),
    path('portafolio/<usuario>', perfilportafolio.as_view(), name="perfil"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('signout/', signout, name="signout"),
    path('contacto/', contacto, name="contacto"),
    path('crearportafolio/', CrearPortafolio.as_view(), name="create"),
    path('about/', InfoPerfilDetalle.as_view(), name="aboutinfo"),
    path('proyecto/<id>', VerDetalleProyecto.as_view(), name="proyecto"),
    path('ipvisitantes/', verIps.as_view(), name="verips")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
