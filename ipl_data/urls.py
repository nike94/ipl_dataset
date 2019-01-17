from django.urls import path
from . import views

urlpatterns = [
    # for jason objects
    path('index/', views.index, name='index'),
    path('matches-played/', views.matches_played, name='matches_played'),
    path('wins-per-season/', views.wins_per_season, name='wins_per_season'),
    path('extra-runs/', views.extra_runs, name='extra_runs'),
    path('top-economy/', views.top_economy, name='top_economy'),
    path('ipl-story/', views.ipl_story, name='ipl_story'),

    # for charts
    path('matches-played/chart', views.matches_played_chart, name='matches_played_chart'),
    path('wins-per-season/chart', views.wins_per_season_chart, name='wins_per_season_chart'),
    path('extra-runs/chart', views.extra_runs_chart, name='extra_runs_chart'),
    path('top-economy/chart', views.top_economy_chart, name='top_economy_chart'),
    path('ipl-story/chart', views.ipl_story_chart, name='ipl_story_chart'),
]
