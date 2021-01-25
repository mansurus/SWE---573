from django.urls import path
from . import views

urlpatterns = [
    path('result', views.redditsearch, name="result"),
    path('vaccine', views.vaccineSub, name="vaccine"),
    path('search', views.searchKeyword, name="search"),
    path('wiki', views.wikiResult, name="wiki"),
    path('<str:id>/', views.posts, name="posts"),
    path('error', views.errorPage, name="error"),
    path('error2', views.errorWiki, name="error2"),
    # path('api/list', views.ListJson.as_view()),
    # path('api/read/<str:id>/', views.ListJsonById.as_view()),
    
]