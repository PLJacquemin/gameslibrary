from django.shortcuts import render, redirect
from .models import Video_game
from django.views import generic
from .forms import GameForm
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Avg, Max, Min, FloatField, Q
from django.http import JsonResponse
from random import choice
from .get_steam import get_steam_db, get_psn_db
from howlongtobeatpy import HowLongToBeat
import datetime
from decimal import *

def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count == 0:
        return 0
    elif count % 2 == 1:
        return values[int(round(count/2))]
    else:
        return sum(values[count/2-1:count/2+1])/Decimal(2.0)
    
def time_calculation(minutes):
    days = minutes // 1440    
    years =  days // 365
    leftover_days = days % 365
    leftover_minutes = minutes % 1440
    hours = leftover_minutes // 60
    left_minutes = leftover_minutes % 60
    time_calculated={'years': years, 'days': leftover_days, 'hours': hours, 'minutes': left_minutes}
    return time_calculated

def home(request):
    return render(request, "gl_home.html")

def dash_wiki(request):
    return render(request, "gl_dash_wiki.html")

def data_wiki(request):
    return render(request, "gl_data_wiki.html")

def wip(request):
    return render(request, "gl_wip.html")

def year_view(request):
    dt_selection = []
    for dt in Video_game.objects.dates('date','year'):
        dt_selection.append(dt.year)
    dt_selection.reverse()
    year=datetime.date.today().year
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'
    qset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True)
    finished_year = qset.count()
    avg_year = round(qset.aggregate(average=Avg('playtime_forever', output_field=FloatField())/60)['average'],2)
    max_year = round(qset.aggregate(maxi=Max('playtime_forever', output_field=FloatField()))['maxi']/60,2)
    med_year = round(median_value(qset, 'playtime_forever')/60,2)
    long_game = qset.order_by('-playtime_forever')[0]
    short_game = qset.order_by('playtime_forever')[0]
    last_game = qset.order_by('-date')[0]
    first_game = qset.order_by('date')[0]
    first_game_hours = first_game.playtime_forever // 60
    first_game_minutes = first_game.playtime_forever % 60
    last_game_hours = last_game.playtime_forever // 60
    last_game_minutes = last_game.playtime_forever % 60
    min_year = round(qset.aggregate(mini=Min('playtime_forever', output_field=FloatField()))['mini']/60,2)
    best_platform = qset.values('platform').annotate(total=Count('platform')).order_by("-total")[0]
    #print(best_platform)

    #print(avg_year, med_year, max_year, min_year)
    return render(request, 'gl_year_view.html', 
                      { 'finished_year': finished_year, 'year': year,
                       'dt_selection': dt_selection,
                       'avg_year':avg_year, 'med_year':med_year, 'max_year':max_year, 'min_year':min_year,
                       'long_game':long_game, 'last_game': last_game, 'first_game': first_game, 'short_game': short_game,
                       'first_game_hours': first_game_hours, 'first_game_minutes': first_game_minutes, 
                       'last_game_hours': last_game_hours, 'last_game_minutes': last_game_minutes,
                       'best_platform': best_platform})


def year_view_dt(request, year):
    if len(year)>4:
        pass
    dt_selection = []
    for dt in Video_game.objects.filter(completed=True).dates('date','year'):
        dt_selection.append(dt.year)
    dt_selection.reverse()
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    qset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True)
    finished_year = qset.count()

    avg_year = round(qset.aggregate(average=Avg('playtime_forever', output_field=FloatField())/60)['average'],2)
    med_year = round(median_value(qset, 'playtime_forever')/60,2)
    max_year = round(qset.aggregate(maxi=Max('playtime_forever', output_field=FloatField()))['maxi']/60,2)
    long_game = qset.order_by('-playtime_forever')[0]
    short_game = qset.order_by('playtime_forever')[0]
    last_game = qset.order_by('-date')[0]
    first_game = qset.order_by('date')[0]
    first_game_hours = first_game.playtime_forever // 60
    first_game_minutes = first_game.playtime_forever % 60
    last_game_hours = last_game.playtime_forever // 60
    last_game_minutes = last_game.playtime_forever % 60
    min_year = round(qset.aggregate(mini=Min('playtime_forever', output_field=FloatField()))['mini']/60,2)
    best_platform = qset.values('platform').annotate(total=Count('platform')).order_by("-total")[0]
    #print(best_platform)

    return render(request, 'gl_year_view.html', 
                      { 'finished_year': finished_year, 'year': year,
                       'dt_selection': dt_selection,
                       'avg_year':avg_year, 'med_year':med_year, 'max_year':max_year, 'min_year':min_year,
                       'long_game':long_game, 'last_game': last_game, 'first_game': first_game, 'short_game': short_game,
                       'first_game_hours': first_game_hours, 'first_game_minutes': first_game_minutes, 
                       'last_game_hours': last_game_hours, 'last_game_minutes': last_game_minutes,
                       'best_platform': best_platform})


def global_view(request):
    qset = Video_game.objects.all()
    total = Video_game.objects.all().count()
    finished = Video_game.objects.filter(completed=True).count()
    played = Video_game.objects.filter(played=True, completed=False).count()
    untouched = total - finished - played
    progress_pl = round(played/total*100)
    progress_fi = round(finished/total*100)
    progress_un = 100 - progress_pl - progress_fi
    tot_genre = Video_game.objects.filter(~Q(genre="")).values('genre').annotate(total=Count('genre')).annotate(time=Sum('playtime_forever')).annotate(time_game=Sum('playtime_forever')/Count('genre'))

    best_genre=tot_genre.order_by('-total')[0]
    best_genre_hours=best_genre['time']//60
    best_genre_minutes=best_genre['time']%60

    low_genre=tot_genre.order_by('total')[0]
    low_genre_hours=low_genre['time']//60
    low_genre_minutes=low_genre['time']%60

    long_genre=tot_genre.order_by('-time')[0]
    long_genre_hours=long_genre['time']//60
    long_genre_minutes=low_genre['time']%60

    short_genre=tot_genre.order_by('time')[0]
    short_genre_hours=short_genre['time']//60
    short_genre_minutes=short_genre['time']%60

    lpg_genre=tot_genre.order_by('-time_game')[0]
    lpg_genre_hours=lpg_genre['time_game']//60
    lpg_genre_minutes=lpg_genre['time_game']%60

    spg_genre=tot_genre.order_by('time_game')[0]
    spg_genre_hours=spg_genre['time_game']//60
    spg_genre_minutes=spg_genre['time_game']%60

    best_platform = qset.values('platform').annotate(total=Count('platform')).order_by("-total")[0]
    worst_platform = qset.values('platform').annotate(total=Count('platform')).order_by("total")[0]
    number_platform = len(qset.values('platform').annotate(total=Count('platform')))
    spent_time = qset.values('platform').annotate(time=Sum('playtime_forever'))
    most_time = spent_time.order_by("-time")[0]["time"]
    less_time = spent_time.order_by("time")[0]["time"]
    total_time = 0
    for time in spent_time:
        total_time += time["time"]
    total_time_cal = time_calculation(total_time)
    most_time_cal = time_calculation(most_time)
    less_time_cal = time_calculation(less_time)

    return render(request, 'gl_global_view.html', 
                  {'total': total,'finished': finished, 'played': played, 
                   'progress_pl': progress_pl, 'progress_fi': progress_fi, 'progress_un': progress_un,
                   'untouched':untouched, 'best_platform':best_platform, 'worst_platform': worst_platform, 
                   'number_platform': number_platform, 'total_time_cal': total_time_cal, 'most_time_cal':most_time_cal,
                   'less_time_cal': less_time_cal, 'number_genre':len(tot_genre),
                   'best_genre':best_genre, 'best_genre_hours':best_genre_hours, 'best_genre_minutes':best_genre_minutes,
                   'low_genre':low_genre, 'low_genre_hours':low_genre_hours, 'low_genre_minutes':low_genre_minutes,
                   'long_genre':long_genre, 'long_genre_hours':long_genre_hours, 'long_genre_minutes':long_genre_minutes,
                   'short_genre':short_genre, 'short_genre_hours':short_genre_hours, 'short_genre_minutes':short_genre_minutes,
                   'lpg_genre':lpg_genre, 'lpg_genre_hours':lpg_genre_hours, 'lpg_genre_minutes':lpg_genre_minutes,
                   'spg_genre':spg_genre, 'spg_genre_hours':spg_genre_hours, 'spg_genre_minutes':spg_genre_minutes,})

def all_games(request):
    game_list = Video_game.objects.all()
    return render(request, 'gl_games_list.html', {'game_list': game_list.order_by('?')[:20]})

def add_game(request):
    submitted = False
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_game?submitted=True')
    else:
        form = GameForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'gl_add_game.html', {'form':form, 'submitted': submitted})

def game_detail(request, game_id):
    game = Video_game.objects.get(pk=game_id)
    game_hltb = game.name.replace("- ", " ").replace(": ", " ").replace("™", "")
    results = HowLongToBeat().search(game_hltb, similarity_case_sensitive=False)
    if results:
        hltb_main=f'{results[0].main_story} H'
        hltb_extra=f'{results[0].main_extra} H'
        hltb_complete=f'{results[0].completionist} H'
    else:
        hltb_main='- H'
        hltb_extra='- H'
        hltb_complete='- H'
    g_hours=game.playtime_forever//60
    g_minutes=game.playtime_forever%60
    return render(request, 'gl_games_detail.html',  {'game': game, 'hltb_main': hltb_main, 'hltb_extra': hltb_extra, 'hltb_complete': hltb_complete
                                                 , 'g_hours': g_hours, 'g_minutes': g_minutes})

def game_update(request, game_id):
    game = Video_game.objects.get(pk=game_id)
    form = GameForm(request.POST or None, instance=game)
    if form.is_valid():
        form.save()
        return redirect('GamesLibrary:game-detail', game_id=game_id)
    return render(request, 'gl_update_game.html',  {'game': game, 'form': form})
 
def search_game(request):
    if request.method == "POST":
        searched = request.POST['searched']
        games = Video_game.objects.filter(name__icontains=searched)
        return render(request, 'gl_search_games.html', {'searched':searched, 'games':games})
    else:
        return render(request, 'gl_search_games.html', {})
    
def roulette(request):
    pks = Video_game.objects.filter(completed=False).values_list('pk', flat=True)
    random_pk = choice(pks)
    game = Video_game.objects.get(pk=random_pk)
    return render(request, 'gl_roulette.html',  {'game': game})

def game_delete(request, game_id):
	game = Video_game.objects.get(pk=game_id)
	game.delete()
	return redirect('GamesLibrary:games-list')		

def games_chart(request, year):
    labels = []
    data = []
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date,completed=True).annotate(month=TruncMonth('date')).values('month').annotate(total=Count('appid')).order_by('month')
    for entry in queryset:
        labels.append(f"{entry['month'].year}-{entry['month'].month:02d}")
        data.append(entry['total'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def time_chart(request, year):
    labels = []
    data = []
    data_2 = []
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True).annotate(month=TruncMonth('date')).values('month').annotate(time=Sum('playtime_forever')/60).order_by('month')
    total_time=0
    for entry in queryset:
        labels.append(f"{entry['month'].year}-{entry['month'].month:02d}")
        total_time+=entry['time']
        data.append(total_time)
        data_2.append(entry['time'])

    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data_2
    })

def genre_chart(request, year):
    data = []
    genres = []
    bkgrnd = []
    colors = [
      'rgba(10, 99, 132, 1.0)',
      'rgba(20, 159, 64, 1.0)',
      'rgba(30, 205, 86, 1.0)',
      'rgba(40, 192, 192, 1.0)',
      'rgba(50, 162, 235, 1.0)',
      'rgba(60, 102, 255, 1.0)',
      'rgba(70, 203, 207, 1.0)',
      'rgba(80, 180, 12, 1.0)',
      'rgba(90, 203, 207, 1.0)',
      'rgba(100, 203, 207, 1.0)',
      'rgba(110, 203, 207, 1.0)',
      'rgba(120, 203, 207, 1.0)',
      'rgba(130, 203, 207, 1.0)',
      'rgba(140, 203, 207, 1.0)',
      'rgba(150, 203, 207, 1.0)',
      'rgba(160, 203, 207, 1.0)',
      'rgba(170, 203, 207, 1.0)',
      'rgba(180, 203, 207, 1.0)',
      'rgba(190, 203, 207, 1.0)',
      'rgba(200, 203, 207, 1.0)',
      'rgba(210, 203, 207, 1.0)',
      'rgba(220, 203, 207, 1.0)',
    ]
    i = 0
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True).values('genre').annotate(total=Count('genre'))
    for entry in queryset:
        data.append(entry['total'])
        genres.append(entry['genre'])
        bkgrnd.append(colors[i])
        i+=1

    return JsonResponse(data={
        'labels': genres,
        'data': data,
        'bkgrnd': bkgrnd
    })

def platform_chart(request, year):
    data = []
    platform = []
    bkgrnd = []
    colors = [
      'rgba(10, 99, 132, 1.0)',
      'rgba(20, 159, 64, 1.0)',
      'rgba(30, 205, 86, 1.0)',
      'rgba(40, 192, 192, 1.0)',
      'rgba(50, 162, 235, 1.0)',
      'rgba(60, 102, 255, 1.0)',
      'rgba(70, 203, 207, 1.0)',
      'rgba(80, 180, 12, 1.0)',
      'rgba(90, 203, 207, 1.0)',
      'rgba(100, 203, 207, 1.0)',
      'rgba(110, 203, 207, 1.0)',
      'rgba(120, 203, 207, 1.0)',
      'rgba(130, 203, 207, 1.0)',
      'rgba(140, 203, 207, 1.0)',
      'rgba(150, 203, 207, 1.0)',
      'rgba(160, 203, 207, 1.0)',
      'rgba(170, 203, 207, 1.0)',
      'rgba(180, 203, 207, 1.0)',
      'rgba(190, 203, 207, 1.0)',
      'rgba(200, 203, 207, 1.0)',
      'rgba(210, 203, 207, 1.0)',
      'rgba(220, 203, 207, 1.0)',
    ]
    i = 0
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True).values('platform').annotate(total=Count('platform'))
    for entry in queryset:
        data.append(entry['total'])
        platform.append(entry['platform'])
        bkgrnd.append(colors[i])
        i+=1

    return JsonResponse(data={
        'labels': platform,
        'data': data,
        'bkgrnd': bkgrnd
    })

def platform_total(request):
    data = []
    platform = []
    bkgrnd = []
    colors = [
      'rgba(10, 99, 132, 1.0)',
      'rgba(20, 159, 64, 1.0)',
      'rgba(30, 205, 86, 1.0)',
      'rgba(40, 192, 192, 1.0)',
      'rgba(50, 162, 235, 1.0)',
      'rgba(60, 102, 255, 1.0)',
      'rgba(70, 203, 207, 1.0)',
      'rgba(80, 180, 12, 1.0)',
      'rgba(90, 203, 207, 1.0)',
      'rgba(100, 203, 207, 1.0)',
      'rgba(110, 203, 207, 1.0)',
      'rgba(120, 203, 207, 1.0)',
      'rgba(130, 203, 207, 1.0)',
      'rgba(140, 203, 207, 1.0)',
      'rgba(150, 203, 207, 1.0)',
      'rgba(160, 203, 207, 1.0)',
      'rgba(170, 203, 207, 1.0)',
      'rgba(180, 203, 207, 1.0)',
      'rgba(190, 203, 207, 1.0)',
      'rgba(200, 203, 207, 1.0)',
      'rgba(210, 203, 207, 1.0)',
      'rgba(220, 203, 207, 1.0)',
    ]
    i = 0

    queryset = Video_game.objects.values('platform').annotate(total=Count('platform'))
    for entry in queryset:
        data.append(entry['total'])
        platform.append(entry['platform'])
        bkgrnd.append(colors[i])
        i+=1

    return JsonResponse(data={
        'labels': platform,
        'data': data,
        'bkgrnd': bkgrnd
    })

def db_steam(request):
    submitted = False
    error = False
    if request.method == "POST" and 'run_script' in request.POST:
            steam_id = request.POST.get("steam_id", "")
            api_key = request.POST.get("api_key", "")
            if steam_id and api_key:
                print('API key entered and Steam ID')
                get_steam_db(apikey=api_key, steamid=steam_id)
                return HttpResponseRedirect('/gameslibrary/db_steam?submitted=True')
            else:
                print('Not keys')
                return HttpResponseRedirect('/gameslibrary/db_steam?error=True')
    else:
        if 'submitted' in request.GET:
            submitted = True
        elif 'error' in request.GET:
            error = True
    
    return render(request, 'gl_database.html', {'submitted': submitted, 'error': error})

def db_psn(request):
    submitted = False
    error = False
    if request.method == "POST" and 'run_script' in request.POST:
            token_psn = request.POST.get("token_psn", "")
            if token_psn:
                print('PSN token entered')
                get_psn_db(token=token_psn)
                return HttpResponseRedirect('/gameslibrary/db_psn?submitted=True')
            else:
                print('Not keys')
                return HttpResponseRedirect('/gameslibrary/db_psn?error=True')
    else:
        if 'submitted' in request.GET:
            submitted = True
        elif 'error' in request.GET:
            error = True
    
    return render(request, 'gl_database_psn.html', {'submitted': submitted, 'error': error})


def time_genre_chart(request):
    labels = []
    data = []
    data_2 = []

    queryset = Video_game.objects.filter(~Q(genre="")).values('genre').annotate(time=Sum('playtime_forever')).annotate(time_game=Sum('playtime_forever')/Count('genre'))
    total_time=0
    for entry in queryset:
        labels.append(entry['genre'])
        data.append(round(entry['time_game']/60))
        data_2.append(round(entry['time']/60))

    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data_2
    })

def genre_total_chart(request):
    data = []
    genres = []
    bkgrnd = []
    colors = [
      'rgba(10, 99, 132, 1.0)',
      'rgba(20, 159, 64, 1.0)',
      'rgba(30, 205, 86, 1.0)',
      'rgba(40, 192, 192, 1.0)',
      'rgba(50, 162, 235, 1.0)',
      'rgba(60, 102, 255, 1.0)',
      'rgba(70, 203, 207, 1.0)',
      'rgba(80, 180, 12, 1.0)',
      'rgba(90, 203, 207, 1.0)',
      'rgba(100, 203, 207, 1.0)',
      'rgba(110, 203, 207, 1.0)',
      'rgba(120, 203, 207, 1.0)',
      'rgba(130, 203, 207, 1.0)',
      'rgba(140, 203, 207, 1.0)',
      'rgba(150, 203, 207, 1.0)',
      'rgba(160, 203, 207, 1.0)',
      'rgba(170, 203, 207, 1.0)',
      'rgba(180, 203, 207, 1.0)',
      'rgba(190, 203, 207, 1.0)',
      'rgba(200, 203, 207, 1.0)',
      'rgba(210, 203, 207, 1.0)',
      'rgba(220, 203, 207, 1.0)',
    ]
    i = 0

    queryset = Video_game.objects.filter(~Q(genre="")).values('genre').annotate(total=Count('genre'))
    for entry in queryset:
        data.append(entry['total'])
        genres.append(entry['genre'])
        bkgrnd.append(colors[i])
        i+=1

    return JsonResponse(data={
        'labels': genres,
        'data': data,
        'bkgrnd': bkgrnd
    })