from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"baseleagues" : League.objects.filter(sport__startswith="Base"),
		"femleagues" : League.objects.filter(name__contains="Women"),
		"anyhockey" : League.objects.filter(sport__contains="Hockey"),
		"notfoot" : League.objects.exclude(sport="Football"),
		"conferences" : League.objects.filter(name__icontains="conference"),
		"atlantic" : League.objects.filter(name__icontains="atlantic"),
		"dalteams" : Team.objects.filter(location="Dallas"),
		"raptors" : Team.objects.filter(team_name="Raptors"),
		"cityteams" : Team.objects.filter(location__icontains="city"),
		"teamswitht" : Team.objects.filter(team_name__startswith="T"),
		"locationdesc" : Team.objects.order_by('location'),
		"nameasc" : Team.objects.order_by('-team_name'),
		"coopers" : Player.objects.filter(last_name="Cooper"),
		"joshuas" : Player.objects.filter(first_name="Joshua"),
		"coopersnotjoshua" : Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua"),
		"alexorwyatt" : Player.objects.filter(first_name="Alexander") | Player.objects.filter(first_name="Wyatt"),
		
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/index.html", context)

def index2(request):
	
	context = { 
		'atlsoccteams' : League.objects.get(name = "Atlantic Soccer Conference").teams.all(),
		'pbostonpenguin' : Player.objects.filter(curr_team__team_name__icontains="penguins"),
		'playerinbaseball': Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference"),
		'hockeyflores': Player.objects.filter(curr_team__league__name__icontains="atlantic amateur field hockey").filter(last_name="Flores"),
		'allfoot': Player.objects.filter(curr_team__league__name__icontains="soccer"),
		'sophiateams':Team.objects.filter(curr_players__first_name__icontains="sophia"),
		'sophialeagues': League.objects.filter(teams__curr_players__first_name__icontains="sophia"),
		'floresnotin':Player.objects.exclude(curr_team__team_name__icontains="roughriders").filter(last_name="Flores"),
		'samuel': Player.objects.get(first_name="Samuel",last_name="Evans").all_teams.all(),
		'gatos': Team.objects.get(team_name__icontains="cats").all_players.all(),
		'oldwichi' : Player.objects.exclude(curr_team__team_name__icontains="Vikings").filter(all_teams__team_name__icontains="vikings"),
		'jacob' : Team.objects.filter(all_players__first_name__icontains="jacob",all_players__last_name__icontains="gray").exclude(team_name__icontains="colts"),
		'joshua' : Player.objects.filter(all_teams__league__name__icontains="Atlantic Federation of Amateur Baseball Players").filter(first_name__icontains="joshua"),
		'12steams' : Team.objects.annotate(Count('curr_players')).annotate(Count('all_players')).filter(curr_players__count__gte=12).filter(all_players__count__gte=12).order_by('-all_players__count'),
		'allplayers' : Player.objects.annotate(Count('all_teams')).order_by('-all_teams__count')
		}

	return render(request, "leagues/index2.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")