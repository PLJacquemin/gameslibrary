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
    path('year_view/<year>', views.year_view_dt, name="year-view-dt"),
    path('games', views.all_games, name="games-list" ),
    path('add_game', views.add_game, name="add-game"),
    path('game_detail/<game_id>', views.game_detail, name='game-detail'),
    path('game_update/<game_id>', views.game_update, name='game-update'),
    path('game_delete/<game_id>', views.game_delete, name='game-delete'),
    path('search_games', views.search_game, name="search-game"),
    path('roulette', views.roulette, name="roulette"),
    path('game_chart/<year>', views.games_chart, name='game-chart'),
    path('time_chart/<year>', views.time_chart, name='time-chart'),
    path('genre_chart/<year>', views.genre_chart, name='genre-chart'),
    path('platform_chart/<year>', views.platform_chart, name='platform-chart'),
    path('platform_total', views.platform_total, name='platform-total'),
    path('time_genre_chart', views.time_genre_chart, name='time-genre-chart'),
    path('genre_total_chart', views.genre_total_chart, name='genre-total-chart'),
    path('db_steam', views.db_steam, name="db-steam"),
    path('db_psn', views.db_psn, name="db-psn"),
]