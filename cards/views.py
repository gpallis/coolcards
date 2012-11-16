# Create your views here.
from cards.models import Card
import random
import pdb
from django.shortcuts import render, get_object_or_404

def vote(request):
    
    
    if voted(request):
        #We have a vote!
        handle_voting(request)
    
    vote_feedback = get_feedback(request)
        
    cards = random.sample(Card.objects.all(),2)
    return render(request,'vote.html',{'firstcard':cards[0], 'secondcard':cards[1], 'vote_feedback':vote_feedback})
    
def voted(request):
    try:
        request.POST['voted_for']
        request.POST['voted_against']
    except (KeyError):
        return False
    else:
        return True

def get_feedback(request): 
    if voted(request):
        winner = get_object_or_404(Card, name=request.POST['voted_for'])
        winner_position = get_position(winner)
        return ('You chose ' + winner.name + ', which now ranks at number ' + winner_position + '.')
    else:
        return ''
    
def get_position(wanted_card):
    #Return 1-indexed rank of a given card.
    
    card_list = Card.objects.all() #There's no need to order it by anything special, as Card has descending-elo ordering defined in its Meta.
    for tuple_pair in enumerate(card_list):
        #enumerate returns a list that goes [ (0, Jace), (1, Bitterblossom), etc]
        if tuple_pair[1] == wanted_card:
            rank = tuple_pair[0]
            return str(rank + 1)
    
def handle_voting(request):
    winner = get_object_or_404(Card, name=request.POST['voted_for'])
    loser = get_object_or_404(Card, name=request.POST['voted_against'])
    
    winner.elo += 12
    winner.votes += 1
    loser.elo -= 12
    loser.votes += 1
    winner.save()
    loser.save()