from django.urls import path

from . import views

urlpatterns = [
  path("", views.index_views, name="index"),
  path("accounts/login/", views.login_views, name="login"),
  path("logout", views.logout_views, name="logout"),
  path("register", views.register_views, name="register"),
  path("search", views.search_views, name="search"),
  path("profile/<int:user_id>/", views.profile_views, name="profile"),
  path("all-anime-watchlist/<int:user_id>/", views.watchlist_views, name="all_anime_watchlist"),
  path("currently-watching/<int:user_id>", views.watchlist_views,{'status': 'currently_watching'}, name="currently_watching"),
  path("completed/<int:user_id>", views.watchlist_views, {'status': 'completed'}, name="completed"),
  path("on-hold/<int:user_id>", views.watchlist_views, {'status': 'on_hold'}, name="on_hold"),
  path("dropped/<int:user_id>", views.watchlist_views, {'status': 'dropped'}, name="dropped"),
  path("plan-to-watch/<int:user_id>", views.watchlist_views, {'status': 'plan_to_watch'}, name="plan_to_watch"),
  path("change-status/<int:user_id>/", views.change_status_views, name="change_status"),
  path("every-anime", views.every_anime_views, name="every_anime"),
  path("add-anime/<int:user_id>/", views.add_anime_views, name="add_anime"),
  path("get-anime/<int:anime_id>/", views.get_anime_views, name="get_anime"),
  path("remove-anime/<str:anime_title>", views.remove_anime_views, name="remove_anime"),
  path("fetch-anime/<int:user_id>/", views.fetch_anime_views, name="fetch_anime"),
  path("add-recommended-anime", views.populate_views, {'category': 'recommendations', 'top': False}, name="add_recommended_animes"),
  path("add-top-airing-animes", views.populate_views, {'category': 'airing', 'top': True}, name="top_airing_animes"),
  path("add-top-upcoming-animes", views.populate_views, {'category': 'upcoming', 'top': True}, name="top_upcoming_animes"),
  path("add-top-tv-animes", views.populate_views, {'category': 'tv', 'top': True}, name="top_upcoming_tv_animes"),
  path("add-top-movie-animes", views.populate_views, {'category': 'movie', 'top': True}, name="top_movie_animes"),
  path("add-top-ova-animes", views.populate_views, {'category': 'ova', 'top': True}, name="top_ova_animes"),
  path("add-top-ona-animes", views.populate_views, {'category': 'ona', 'top': True}, name="top_ona_animes"),
  path("add-top-anime-special", views.populate_views, {'category': 'special', 'top': True}, name="top_anime_specials"),
  path("add-most-popular-animes", views.populate_views, {'category': 'bypopularity', 'top': True}, name="most_popular_animes"),
  path("add-most-favorite-animes", views.populate_views, {'category': 'favorite', 'top': True}, name="most_favorite_animes"),
]