from django.conf.urls import url
from rest_framework import urlpatterns
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

# determinar las direcciones en base a URL
# r'^   /$' --> definicion de ruta
urlpatterns=[
    url(r'^api/mascotas/$',views.MascotasViewSet.as_view()),
    url(r'^api/mascotas_crear/$',views.MascotasCreateViewSet.as_view()),
    url(r'^api/mascota/(?P<nombre>.+)/$',views.MascotaBuscarViewSet.as_view()),
    url(r'^api/categoria/(?P<categoria>.+)/$',views.MascotaCategoriaViewSet.as_view()),
]
# determinar que los simbolos de la ruta se implementen 
# como tal (parte de la misma ruta)
urlpatterns = format_suffix_patterns(urlpatterns)