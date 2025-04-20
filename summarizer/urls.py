from django.contrib import admin
from django.urls import path, include
from summarizer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('summarizer.urls')),
    path('download-summary/', download_summary, name='download_summary'),
]