"""
URL configuration for monotext project.

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
from django.contrib import admin
from django.urls import path, re_path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import RedirectView

import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('monotext/', include('posts.urls')),
    path('', RedirectView.as_view(url='monotext/', permanent=True)),
]

# Serving the static files in django (Works only when DEBUG=True and not for production use)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve the favicon
urlpatterns += [
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(settings.BASE_DIR, 'monotext/static/favicon'),
    }
    ),
]
