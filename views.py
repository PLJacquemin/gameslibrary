# Import de fonctions de Django
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, Avg, Max, Min, FloatField, Q
from django.http import JsonResponse, HttpResponseRedirect

# Import d'autres librairies
from random import choice
from howlongtobeatpy import HowLongToBeat
import datetime

# Import des fonctions d'autres fichiers locaux
from .supp_functions import *
from .models import Video_game
from .get_libraries import get_steam_db, get_psn_db
from .forms import GameForm

# Liste des couleurs pour les graphiques

bkg_colors = [
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

####### Affichage de la page d'accueil

# Premier onglet d'accueil
def home(request):
    return render(request, "gl_home.html")

# Onglet sur les tableaux de bord de la page d'accueil
def dash_wiki(request):
    return render(request, "gl_dash_wiki.html")

# Onglet sur la base de données de la page d'accueil
def data_wiki(request):
    return render(request, "gl_data_wiki.html")

# Onglet "Work in Progress"
def wip(request):
    return render(request, "gl_wip.html")


######## Tableaux de bord

# Tableau annuel: affichage par défaut toujours sur l'année en cours

def year_view(request, year=datetime.date.today().year):

    # Contrôle pour éviter les cas où la longueur est plus longue que 4 si la base de données est mal alimentée
    if len(str(year))>4:
        pass

    # Préparation du bouton de sélection des dates
    dt_selection = []
    for dt in Video_game.objects.filter(completed=True).dates('date','year'):
        dt_selection.append(dt.year)
    dt_selection.reverse()

    # Formatage des dates pour le filtre de sélection
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    # Récupération de la liste des jeux terminés entre la date de début et de fin
    qset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True)

    # Alimentation des indicateurs
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


    return render(request, 'gl_year_view.html', 
                      { 'finished_year': finished_year, 'year': year,
                       'dt_selection': dt_selection,
                       'avg_year':avg_year, 'med_year':med_year, 'max_year':max_year, 'min_year':min_year,
                       'long_game':long_game, 'last_game': last_game, 'first_game': first_game, 'short_game': short_game,
                       'first_game_hours': first_game_hours, 'first_game_minutes': first_game_minutes, 
                       'last_game_hours': last_game_hours, 'last_game_minutes': last_game_minutes,
                       'best_platform': best_platform})

# Tableau de bord global

def global_view(request):

    # Alimentation des indicateurs

    # Indicateurs globaux
    qset = Video_game.objects.all()
    total = Video_game.objects.all().count()
    finished = Video_game.objects.filter(completed=True).count()
    played = Video_game.objects.filter(played=True, completed=False).count()
    untouched = total - finished - played
    progress_pl = round(played/total*100)
    progress_fi = round(finished/total*100)
    progress_un = 100 - progress_pl - progress_fi
    
    # Indicateurs par plateforme
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

    # Indicateurs par genre
    tot_genre = Video_game.objects.filter(~Q(genre="")).values('genre').annotate(total=Count('genre')).annotate(time=Sum('playtime_forever')).annotate(time_game=Sum('playtime_forever')/Count('genre'))

        # Meilleur genre de jeux
    best_genre=tot_genre.order_by('-total')[0]
    best_genre_hours=best_genre['time']//60
    best_genre_minutes=best_genre['time']%60

        # Genre le moins touché
    low_genre=tot_genre.order_by('total')[0]
    low_genre_hours=low_genre['time']//60
    low_genre_minutes=low_genre['time']%60

        # Le plus de temps passé
    long_genre=tot_genre.order_by('-time')[0]
    long_genre_hours=long_genre['time']//60
    long_genre_minutes=low_genre['time']%60

        # Le moins de temps passé
    short_genre=tot_genre.order_by('time')[0]
    short_genre_hours=short_genre['time']//60
    short_genre_minutes=short_genre['time']%60

        # Le plus de temps passé par jeu
    lpg_genre=tot_genre.order_by('-time_game')[0]
    lpg_genre_hours=lpg_genre['time_game']//60
    lpg_genre_minutes=lpg_genre['time_game']%60

        # Le moins de temps passé par jeu
    spg_genre=tot_genre.order_by('time_game')[0]
    spg_genre_hours=spg_genre['time_game']//60
    spg_genre_minutes=spg_genre['time_game']%60

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


######## Partie "Base de données"

# Affichage d'une liste de jeux, actuellement juste une liste de jeux affichée de manière "random"

def all_games(request):
    game_list = Video_game.objects.all()
    return render(request, 'gl_games_list.html', {'game_list': game_list.order_by('?')[:20]})

# Ajout d'un jeu

def add_game(request):
    submitted = False
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gameslibrary/add_game?submitted=True')
    else:
        form = GameForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'gl_add_game.html', {'form':form, 'submitted': submitted})

# Affichage des détails d'un jeu

def game_detail(request, game_id):
    game = Video_game.objects.get(pk=game_id)
    game_hltb = game.name.replace("- ", " ").replace(": ", " ").replace("™", "")

    # Récupération des données venant de How Long To Beat
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

# Mise à jour des jeux

def game_update(request, game_id):
    game = Video_game.objects.get(pk=game_id)
    form = GameForm(request.POST or None, instance=game)
    if form.is_valid():
        form.save()
        return redirect('GamesLibrary:game-detail', game_id=game_id)
    return render(request, 'gl_update_game.html',  {'game': game, 'form': form})

# Recherche dans la base de données
 
def search_game(request):
    if request.method == "POST":
        searched = request.POST['searched']
        games = Video_game.objects.filter(name__icontains=searched)
        return render(request, 'gl_search_games.html', {'searched':searched, 'games':games})
    else:
        return render(request, 'gl_search_games.html', {})

# Mode roulette: affiche les détails d'un jeu aléatoire

def roulette(request):
    pks = Video_game.objects.filter(completed=False).values_list('pk', flat=True)
    random_pk = choice(pks)
    game = Video_game.objects.get(pk=random_pk)
    return render(request, 'gl_roulette.html',  {'game': game})

# Suppression d'un jeu

def game_delete(request, game_id):
	game = Video_game.objects.get(pk=game_id)
	game.delete()
	return redirect('GamesLibrary:games-list')	

# Mise à jour de la base de données par récupération des données de steam

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

# Mise à jour de la base de données par récupération des données du PSN

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

######## Partie "Graphiques Annuels"

# Graphique annuel du nombre de jeux terminés par mois

def year_games_chart(request, year):
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

# Affichage du temps par mois et du temps cumulé

def year_time_chart(request, year):
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

# Affichage de la répartition des jeux par genre en "tarte"

def year_genre_pie(request, year):
    data = []
    genres = []
    bkgrnd = []
    colors = bkg_colors
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True).values('genre').annotate(total=Count('genre'))

    i = 0
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

# Affichage de la répartition des jeux par plateforme en "tarte"

def year_platform_pie(request, year):
    data = []
    platform = []
    bkgrnd = []
    colors = bkg_colors
    start_date=f'{year}-01-01'
    end_date=f'{year}-12-31'

    queryset = Video_game.objects.filter(date__gte=start_date, date__lte=end_date, completed=True).values('platform').annotate(total=Count('platform'))

    i = 0
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

######## Partie "Graphiques Annuels"

# Affichage de la répartition des jeux par plateforme en "tarte"

def global_platform_pie(request):
    data = []
    platform = []
    bkgrnd = []
    colors = bkg_colors
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

# Affichage du temps par genre et du temps par jeu et par genre

def time_genre_chart(request):
    labels = []
    data = []
    data_2 = []

    queryset = Video_game.objects.filter(~Q(genre="")).values('genre').annotate(time=Sum('playtime_forever')).annotate(time_game=Sum('playtime_forever')/Count('genre'))
    
    total_time=0
    for entry in queryset:
        labels.append(entry['genre'])
        data.append(round(entry['time_game']//60))
        data_2.append(round(entry['time']//60))

    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data_2
    })

# Affichage du nombre de jeux par genre en "tarte"

def global_genre_pie(request):
    data = []
    genres = []
    bkgrnd = []
    colors = bkg_colors
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