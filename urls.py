from django.urls import path
from . import views

app_name = 'GamesLibrary'
urlpatterns = [
    path('', views.home, name="home"),
    path('dash_wiki', views.dash_wiki, name="dash-wiki"),
    path('data_wiki', views.data_wiki, name="data-wiki"),
    path('wip', views.wip, name="wip"),
    path('global_view', views.global_view, name="global-view"),
    path('year_view', views.year_view, name="year-view"),
    path('year_view/<year>', views.year_view, name="year-view-dt"),
    path('games', views.all_games, name="games-list" ),
    path('add_game', views.add_game, name="add-game"),
    path('game_detail/<game_id>', views.game_detail, name='game-detail'),
    path('game_update/<game_id>', views.game_update, name='game-update'),
    path('game_delete/<game_id>', views.game_delete, name='game-delete'),
    path('search_games', views.search_game, name="search-game"),
    path('roulette', views.roulette, name="roulette"),
    path('game_chart/<year>', views.year_games_chart, name='game-chart'),
    path('time_chart/<year>', views.year_time_chart, name='time-chart'),
    path('genre_pie/<year>', views.year_genre_pie, name='genre-pie'),
    path('platform_pie/<year>', views.year_platform_pie, name='platform-pie'),
    path('global_platform_pie', views.global_platform_pie, name='global-platform-pie'),
    path('time_genre_chart', views.time_genre_chart, name='time-genre-chart'),
    path('global_genre_pie', views.global_genre_pie, name='global-genre-pie'),
    path('global_owned_pie', views.global_owned_pie, name='global-owned-pie'),
    path('stars_chart/<year>', views.year_stars_chart, name='stars-chart'),
    path('release_chart/<year>', views.year_release_chart, name='release-chart'),
    path('publisher_pie/<year>', views.year_publisher_pie, name='publisher-pie'),
    path('db_steam', views.db_steam, name="db-steam"),
    path('db_psn', views.db_psn, name="db-psn"),
]