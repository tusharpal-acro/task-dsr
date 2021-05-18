"""digital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path,re_path
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView
from dsrs import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"dsrs", views.DSRViewSet)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="DSR Project",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),    
    path('dsrs/', views.DSRListAPIView.as_view()),
    path('dsrs/<id>', views.DSRRetrieveAPIView.as_view()),
    path('resource/percentile/<int:number>', views.RESOURCEView),
    path("list/", views.list),
    path("deleted/<id>", views.deleted),

]
