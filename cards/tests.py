import pdb
from django.test import TestCase
from cards.models import Card, Oracle

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
    def test_leaderboard_includes_ultimate_price(self):
        response = self.client.get('/leaderboard/')
        return self.assertContains(response,'Ultimate')
    def test_sorting_is_working(self):
        response = self.client.get('/leaderboard/')
        first_card = response.context['cards'][0]
        return self.assertEqual(first_card.name,'Nicol Bolas, Planeswalker')
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
        