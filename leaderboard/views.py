from cards.models import Card
from django.core.paginator import Paginator,InvalidPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def leaderboard(request):
    PAGE_LENGTH = 5 #for purposes of infinite scroll
    cards_ordered_list = Card.objects.all() #they are already ordered because of their class meta ordering property.
    
    p = Paginator(cards_ordered_list,PAGE_LENGTH)
    
    try:
        current_page = request.GET['p']
    except:
        #none specified, show 1st page
        current_page = 1
        return render(request,'leaderboard.html', {'cards':p.page(current_page)})

    #we're still here, so it must have been a desired-page request   
    try:
        #we have a page, and it's not the last one
        next_page = p.page(int(current_page) + 1)
        return render(request,'leaderboard_table.html', {'cards':next_page})     
    except:
        #there's no such page - must be the last one
        return HttpResponse('false') #the JS expects this and knows what to do with it.
    
def endless(request):
    babble = ('1')
    try:
        babble = str(request.GET['bubble'])
    except:
        #Shouldn't happen in test example.
        pass
        
    return render(request,'endless.html',{'babble':babble*20000, 'next_page':str(int(babble)+1)})