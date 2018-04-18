"""myAtom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cuisine.views import home, react, IndexView
import debug_toolbar


urlpatterns = [
    path('', home, name='home'),
    path('react/<int:page>', react, name='react'),
    path('index', IndexView.as_view(), name='index'),
    path('activity/', include('activity.urls')),
    path('accounts/', include('accounts.urls')),
    path('cuisine/', include('cuisine.urls')),
    path('admin/', admin.site.urls),
    path('debug/',include(debug_toolbar.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
