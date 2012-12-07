# Create your views here.
from cards.models import Card
from activity.models import Vote
import random
import math
import pdb
from django.shortcuts import render, get_object_or_404

def vote(request):
    if voted(request):
        #We have a vote!
        handle_voting(request)
    
    vote_feedback = get_feedback(request)
        
    card_population = get_card_population()
    cards = random.sample(card_population,2)
    return render(request,'vote.html',{'firstcard':cards[0], 'secondcard':cards[1], 'vote_feedback':vote_feedback})

def get_card_population():
    #returns a subset of the cards from with to extract a fairish match.
    SLICE_SIZE = 3 #number of cards in the slice.
    total_cards = Card.objects.count()
    lowest_rank_of_possible_slice_leader = total_cards - SLICE_SIZE
    chosen_slice_leader = random.randint(0,lowest_rank_of_possible_slice_leader)
    return Card.objects.all()[chosen_slice_leader:chosen_slice_leader+SLICE_SIZE]

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
    
def calculate_elo_move(winner,loser):
    base_bonus = 12 #what you get for winning an even match.
    winner_rank_advantage = float(winner.elo - loser.elo) #did the winner get a head start? 
    winner_win_probability = 0.5 + (winner_rank_advantage/800)# 100% win chance at 400 overdog, 0% win chance at 400 underdog.
    
    winner_win_probability = min(winner_win_probability,0.9) #because one can't be that sure, it's not chess, people might be trolling.
    winner_win_probability = max(winner_win_probability,0.1) #because one can't be that sure, it's not chess, people might be trolling.
    
    elo_move = 24 * (1 - winner_win_probability) #+12 in a 50-50, +2.4 for a stomp, +21.6 for a huge upset.
    return elo_move

def uncertainty_factor(card):
    #what do we multiply elo change by because of our ignorance?
    #maximum 5 at zero votes and 1 at anything above 49
    naive_modifier = (50 - card.votes)/10.0
    return max(naive_modifier,1) #cards with over 49 votes should move at normal speed 

def handle_voting(request):
    winner = get_object_or_404(Card, name=request.POST['voted_for'])
    loser = get_object_or_404(Card, name=request.POST['voted_against'])
    
    elo_move = calculate_elo_move(winner,loser)
    #Note that while elo_move and the uncertainty factor may be floats, the actual field is an integer.
    
    winner.elo += (elo_move*uncertainty_factor(winner))
    winner.votes += 1
    loser.elo -= (elo_move*uncertainty_factor(loser))
    loser.votes += 1
    winner.save()
    loser.save()
    
    #now, log the vote
    vote_data = Vote(voter=request.META['HTTP_X_FORWARDED_FOR'],voted_for=winner,voted_against=loser)
    vote_data.save()