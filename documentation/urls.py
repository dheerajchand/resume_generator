#!/usr/bin/env python3
"""
Documentation URL patterns
"""

from django.urls import path
from . import views

app_name = 'documentation'

urlpatterns = [
    path('', views.docs_index, name='index'),
    path('search/', views.docs_search, name='search'),
    path('<str:page_name>/', views.docs_page, name='page'),
]
