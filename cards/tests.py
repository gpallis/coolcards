import pdb
from django_fasttest import TestCase
from cards.models import Card, Oracle
from activity.models import Vote

class SimpleTest(TestCase):
    
    fixtures = ['new.json']
        
    def test_card_creation(self):
        try:
            Card.objects.get(name='Launch Party')
        except:
            self.fail("No record found for Launch Party!")
        else:
            pass
    def test_leaderboard_page_exists(self):
        response = self.client.get('/leaderboard/')
        return self.assertEqual(response.status_code,200)
    def test_voting_page_exists(self):
        response = self.client.get('/vote/')
        return self.assertEqual(response.status_code,200)
    def test_sorting_is_working(self):
        self.client.post('/vote/', {'voted_for':'Ultimate Price', 'voted_against':'Launch Party'})
        response = self.client.get('/leaderboard/')
        first_card = response.context['cards'][0]
        return self.assertEqual(first_card.name,'Ultimate Price')
    def test_votes_raising_elo(self):
        old_rating = Card.objects.get(name='Ultimate Price').elo
        self.client.post('/vote/', {'voted_for':'Ultimate Price', 'voted_against':'Launch Party'})
        new_rating = Card.objects.get(name='Ultimate Price').elo
        return self.assertGreater(new_rating, old_rating)
    def test_votes_lowering_elo(self):
        old_rating = Card.objects.get(name='Launch Party').elo
        self.client.post('/vote/', {'voted_for':'Ultimate Price', 'voted_against':'Launch Party'})
        new_rating = Card.objects.get(name='Launch Party').elo
        return self.assertGreater(old_rating, new_rating)
    def test_404_firing_on_invalid_vote(self):
        response = self.client.post('/vote/', {'voted_for':'Spooky Wooky', 'voted_against':999})
        return self.assertEqual(response.status_code,404)
    def test_showing_vote_feedback(self):
        response = self.client.post('/vote/', {'voted_for':'Rakdos, Lord of Riots', 'voted_against':'Launch Party'}, follow=True)
        return self.assertContains(response,'You ')
    def test_oracle_single_set_working(self):
        abrupt_decay = Oracle.objects.get(name='Abrupt Decay')
        rules = abrupt_decay.rules
        return self.assertTrue(rules.find('target') > -1 )
    def test_leaderboard_showing_oracle(self):
        self.client.post('/vote/', {'voted_for':'Ultimate Price', 'voted_against':'Launch Party'})
        response = self.client.get('/leaderboard/')
        return self.assertContains(response, 'monocolored')
    def test_leaderboard_showing_types(self):
        response = self.client.get('/leaderboard/')
        return self.assertContains(response, 'Legendary Creature')
    def test_leaderboard_showing_pt(self):
        response = self.client.get('/leaderboard/')
        return self.assertContains(response, '[6/6]')
    def test_new_card(self):
        new_card = Card(name='Cobblebrute',elo='9999',votes=5)
        new_card.save()
        response = self.client.get('/leaderboard/')
        return self.assertContains(response, '[5/2]')
    def test_vote_logging(self):
        #vote
        response = self.client.post('/vote/', {'voted_for':'Ultimate Price', 'voted_against':'Launch Party'}, follow=True)
        response = self.client.post('/vote/', {'voted_for':'Rakdos, Lord of Riots', 'voted_against':'Nicol Bolas, Planeswalker'}, follow=True)
        return self.assertTrue(Vote.objects.all()[0].voted_for.name=='Rakdos, Lord of Riots')
    def test_votes_use_certainty(self):
        new_card = Card(name='Cobblebrute',elo='1000',votes=10)
        new_card.save()
        response = self.client.post('/vote/', {'voted_for':'Cobblebrute', 'voted_against':'Hydrosurge'})
        response = self.client.post('/vote/', {'voted_for':'Rakdos, Lord of Riots', 'voted_against':'Launch Party'})
        cobblebrute = Card.objects.get(name='Cobblebrute')
        rakdos = Card.objects.get(name='Rakdos, Lord of Riots')
        hydrosurge = Card.objects.get(name='Hydrosurge')
        launch_party = Card.objects.get(name='Launch Party')
        ultimate_price = Card.objects.get(name='Ultimate Price')
        
        if (rakdos.elo > cobblebrute.elo and cobblebrute.elo > ultimate_price.elo and launch_party.elo == hydrosurge.elo):
            pass
        else:
            self.fail("ELOs not moving properly: " + str(rakdos.elo) + " " + str(cobblebrute.elo) +" " + str(ultimate_price.elo)
                      + " " + str(launch_party.elo) + " " + str(hydrosurge.elo))
    def test_votes_use_elo(self):
        bad_card = Card(name='Baddie',elo=1000,votes=1000)
        good_card = Card(name='Goodie',elo=1900,votes=1000)
        good_card.save()
        bad_card.save()
        response = self.client.post('/vote/', {'voted_for':'Goodie', 'voted_against':'Baddie'})
        return self.assertEqual(Card.objects.get(name='Goodie').elo,1902) #minimum elo gain
        
        
        
        