from cards.models import Card
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.
def leaderboard(request):
    cards_ordered_list = Card.objects.all().order_by('elo').reverse()
    return render(request,'leaderboard.html', {'cards':cards_ordered_list})