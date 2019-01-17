from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Matches, Deliveries
from collections import OrderedDict
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.db.models import Count, Sum, ExpressionWrapper, FloatField, IntegerField, F, Q

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Home page
def index(request):
    template_name = "ipl_data/index.html"
    context = {}
    return render(request, template_name, context)


# print json of number of matches played per year
@cache_page(CACHE_TTL)
def matches_played(request):
    queryset = Matches.objects.values('season').annotate(count=Count('season')).order_by('season')
    seasons = list(queryset)
    context = {}
    for season in seasons:
        context[season['season']] = season['count']

    return JsonResponse(context, safe=False)


# print json of number of matches won by each team per season
@cache_page(CACHE_TTL)
def wins_per_season(request):
    queryset = Matches.objects.values('season', 'winner').annotate(Count('winner')).order_by('season')
    results = list(queryset)
    context = {}
    year = 0
    for match in results:
        if year == int(match['season']):
            context[match['season']][match['winner']] = int(match['winner__count'])
        else:
            year = int(match['season'])
            context[match['season']] = {match['winner']: int(match['winner__count'])}

    return JsonResponse(context, safe=False)


# print json of extra runs given in the year 2016 by each team
@cache_page(CACHE_TTL)
def extra_runs(request):
    queryset = Deliveries.objects.values('bowling_team').annotate(Sum('extra_runs')).filter(match__season='2016')
    extra_runs = list(queryset)
    context = {}

    for team in extra_runs:
        context[team['bowling_team']] = team['extra_runs__sum']

    return JsonResponse(context, safe=False)


# print json of top ten economical bowler in the year 2015
def top_economy(request):
    queryset = Deliveries.objects.filter(match__season='2015') \
            .values('bowler') \
            .annotate(t_runs=Sum('total_runs', output_field=FloatField()), l_runs=Sum('legbye_runs', output_field=FloatField()), b_runs=Sum('bye_runs', output_field=FloatField()), c_runs=Count('total_runs', filter=Q(noball_runs=0) & Q(wide_runs=0))).annotate(eco=ExpressionWrapper(
             (F('t_runs')-F('l_runs')-F('b_runs'))/(F('c_runs')/6),
             output_field=FloatField())).order_by('eco')[:10]

    context = OrderedDict()
    top_economy = list(queryset)

    for bowler in top_economy:
        context[bowler['bowler']] = round(bowler['eco'], 2)

    return JsonResponse(context, safe=False)


# print json object of top 10 runs scored or wikcet taken in the provided year
def ipl_story(request):
    if request.method == 'POST':
        performer = request.POST.get('performer', None)
        season = request.POST.get('year', None)

        if performer == 'batsman':
            queryset = Deliveries.objects.filter(match__season=int(season)).values('batsman').annotate(runs=Sum('batsman_runs')).order_by('-runs')[:10]
        else:
            queryset = Deliveries.objects.filter(match__season=int(season)).values('bowler').annotate(wiks=(Count('player_dismissed', output_field=IntegerField())-Count('player_dismissed', output_field=IntegerField(), filter=Q(player_dismissed='')))).order_by('-wiks')[:10]
        context = {
            "performance": list(queryset)
        }

        return JsonResponse(context, safe=False)
    else:
        return render(request, 'ipl_data/info_form.html')


# display chart of number of matches played per year
def matches_played_chart(request):
    template_name = "ipl_data/matches_played.html"
    queryset = Matches.objects.values('season').annotate(count=Count('season')).order_by('season')
    context = {
        "matches_played": queryset
    }

    return render(request, template_name, context)


# display chart of number of matches won by each team per season
def wins_per_season_chart(request):
    template_name = "ipl_data/wons_per_season_chart.html"
    queryset = Matches.objects.values('season', 'winner').annotate(Count('winner')).order_by('season', 'winner')
    wins = list(queryset)
    teams = set()
    season = set()

    for team in wins:
        if team['winner']:
            season.add(team['season'])
            teams.add(team['winner'])

    matches_won_per_season = {}

    year = 0
    for win in wins:
        if win['winner']:
            if year != win['season']:
                if len(matches_won_per_season) != 0:
                    for team in teams:
                        if team not in teams_played:
                            if team in matches_won_per_season.keys():
                                matches_won_per_season[team].append(0)
                            else:
                                matches_won_per_season[team] = [0]
                year = win['season']
                teams_played = set()
            else:
                teams_played.add(win['winner'])

            if win['winner'] not in matches_won_per_season.keys():
                matches_won_per_season[win['winner']] = []
            teams_played.add(win['winner'])
            matches_won_per_season[win['winner']].append(int(win['winner__count']))

    teams = list(teams)
    teams.sort()

    season = list(season)
    season.sort()


    context = {
        'teams': teams,
        'season': season,
        'matches_won': matches_won_per_season
    }
    return render(request, template_name, context)


# display chart of extra runs given in the year 2016 by each team
def extra_runs_chart(request):
    template_name = 'ipl_data/extra_runs_chart.html'
    queryset = Deliveries.objects.values('bowling_team').annotate(Sum('extra_runs')).filter(match__season='2016')
    context = {
        'extra_runs': queryset
    }

    return render(request, template_name, context)


# display chart of top ten economical bowler in the year 2015
def top_economy_chart(request):
    template_name = 'ipl_data/top_economy.html'
    queryset = Deliveries.objects.filter(match__season='2015') \
            .values('bowler') \
            .annotate(t_runs=Sum('total_runs', output_field=FloatField()), l_runs=Sum('legbye_runs', output_field=FloatField()), b_runs=Sum('bye_runs', output_field=FloatField()), c_runs=Count('total_runs', filter=Q(noball_runs=0) & Q(wide_runs=0))).annotate(eco=ExpressionWrapper(
             (F('t_runs')-F('l_runs')-F('b_runs'))/(F('c_runs')/6),
             output_field=FloatField())).order_by('eco')[:10]

    top_eco = OrderedDict()
    top_economy = list(queryset)

    for bowler in top_economy:
        top_eco[bowler['bowler']] = round(bowler['eco'], 2)

    bowlers = list(top_eco.keys())
    eco = list(top_eco.values())
    context = {
        'bowlers': bowlers,
        'eco': eco
    }
    return render(request, template_name, context)


# display chart of top 10 runs scored or wikcet taken in the provided year
def ipl_story_chart(request):
    if request.method == 'POST':
        template_name = 'ipl_data/ipl_story_chart.html'
        performer = request.POST.get('performer', None)
        season = request.POST.get('year', None)

        if performer == 'batsman':
            queryset = Deliveries.objects.filter(match__season=int(season)).values('batsman').annotate(performence=Sum('batsman_runs')).order_by('-performence')[:10]
            yaxis = "Runs"
        else:
            queryset = Deliveries.objects.filter(match__season=int(season)).values('bowler').annotate(performence=(Count('player_dismissed', output_field=IntegerField())-Count('player_dismissed', output_field=IntegerField(), filter=Q(player_dismissed='')))).order_by('-performence')[:10]
            yaxis = "Wickets"

        player_performence = list(queryset)

        player_name = []
        performence = []
        for player in player_performence:
            player_name.append(player[performer])
            performence.append(player['performence'])

        context = {
            "player_name": player_name,
            "performences": performence,
            "performer": performer,
            "season": season,
            "yaxis": yaxis
        }

        return render(request, template_name, context)
    else:
        return render(request, 'ipl_data/info_form.html')
