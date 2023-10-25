"""
URL configuration for qnd41app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,re_path,include
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from baton.autodiscover import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail import urls as wagtaildocs_urls

urlpatterns = i18n_patterns (

    path('analytics/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('rosetta/', include('rosetta.urls')),

    re_path(r'^businessmedia/', include(wagtailadmin_urls),name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),

  )  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
