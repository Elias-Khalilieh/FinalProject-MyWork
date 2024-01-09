
from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_home),
    path('success',views.display_home),
    path('signup', views.new_sign_up),
    path('signin', views.new_sign_in),
    path('logout',views.destroy_session),
    path('load_contact_us_page',views.display_contact),
    path('go_to_add',views.display_add),
    path('add_new_anime',views.create_anime),
    path('animes/<int:anid>',views.show_anime),
    path('addrev/<int:anid>',views.postrev)
]