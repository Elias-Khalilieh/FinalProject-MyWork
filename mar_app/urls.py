
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
    path('addrev/<int:anid>',views.postrev),
    path('review/delete/<int:reviewid>/<int:oneanimeid>',views.deleteonerev),
    path('anime/<int:anid>/edit',views.show_edit),
    path('anime/<int:anid>/delete',views.delthisan),
    path('editanime/<int:oneanimeid>',views.edit_anime),
    path('anime/<int:anid>/unfavorite',views.unfavorite_this),
    path('anime/<int:anid>/favorite',views.favorite_this),
    path('load_shop',views.display_shop)
]