import pdb
from django_fasttest import TestCase
from cards.models import Card, Oracle
from activity.models import Vote

class SimpleTest(TestCase):
    
    fixtures = ['new.json']
        
    def test_card_existence(self):
        try:
            Card.objects.get(name='Jace, the Mind Sculptor')
        except:
            self.fail("No record found for Jace!")
        else:
            pass
    def test_leaderboard_page_exists(self):
        response = self.client.get('/leaderboard/')
        return self.assertEqual(response.status_code,200)
    def test_voting_page_exists(self):
        response = self.client.get('/vote/')
        return self.assertEqual(response.status_code,200)
    def test_sorting_is_working(self):
        good_card = Card(name='Inaction Injunction',elo=9999,votes=1000)
        good_card.save()
        response = self.client.get('/leaderboard/')
        first_card = response.context['cards'][0]
        return self.assertEqual(first_card.name,'Inaction Injunction')
    def test_votes_raising_elo(self):
        old_rating = Card.objects.get(name='Isochron Scepter').elo
        self.client.post('/vote/', {'voted_for':'Isochron Scepter', 'voted_against':'Precursor Golem'})
        new_rating = Card.objects.get(name='Isochron Scepter').elo
        return self.assertGreater(new_rating, old_rating)
    def test_votes_lowering_elo(self):
        old_rating = Card.objects.get(name='Precursor Golem').elo
        self.client.post('/vote/', {'voted_for':'Isochron Scepter', 'voted_against':'Precursor Golem'})
        new_rating = Card.objects.get(name='Precursor Golem').elo
        return self.assertGreater(old_rating, new_rating)
    def test_404_firing_on_invalid_vote(self):
        response = self.client.post('/vote/', {'voted_for':'Spooky Wooky', 'voted_against':999})
        return self.assertEqual(response.status_code,404)
    def test_showing_vote_feedback(self):
        response = self.client.post('/vote/', {'voted_for':'Rakdos, Lord of Riots', 'voted_against':'Precursor Golem'}, follow=True)
        return self.assertContains(response,'You ')
    def test_oracle_single_set_working(self):
        millstone = Oracle.objects.get(name="Geralf's Mindcrusher")
        rules = millstone.rules
        return self.assertTrue(rules.find('library') > -1 )
    def test_leaderboard_showing_oracle(self):
        good_card = Card(name='Inaction Injunction',elo=9999,votes=1000)
        good_card.save()
        response = self.client.get('/leaderboard/')
        return self.assertContains(response, 'Detain')
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
        response = self.client.post('/vote/', {'voted_for':'Isochron Scepter', 'voted_against':'Precursor Golem'}, follow=True)
        response = self.client.post('/vote/', {'voted_for':'Rakdos, Lord of Riots', 'voted_against':'Austere Command'}, follow=True)
        return self.assertTrue(Vote.objects.all()[0].voted_for.name=='Rakdos, Lord of Riots')
    def test_votes_use_certainty(self):
        new_card = Card(name='Cobblebrute',elo='1000',votes=10)
        new_card.save()
        new_card = Card(name='Homicidal Seclusion',elo='1000',votes=0)
        new_card.save()
        new_card = Card(name='Rakdos Guildgate',elo='1000',votes=0)
        new_card.save()
        new_card = Card(name='Life from the Loam',elo='1000',votes=0)
        new_card.save()
        
        response = self.client.post('/vote/', {'voted_for':'Cobblebrute', 'voted_against':'Homicidal Seclusion'})
        response = self.client.post('/vote/', {'voted_for':'Rakdos Guildgate', 'voted_against':'Life from the Loam'})
        cobblebrute = Card.objects.get(name='Cobblebrute')
        rakdos_guildgate = Card.objects.get(name='Rakdos Guildgate')
        homicidal_seclusion = Card.objects.get(name='Homicidal Seclusion')
        life_from_the_loam = Card.objects.get(name='Life from the Loam')
        
        if (rakdos_guildgate.elo > cobblebrute.elo and cobblebrute.elo > 1000 and life_from_the_loam.elo == homicidal_seclusion.elo):
            pass
        else:
            self.fail("ELOs not moving properly: " + str(rakdos.elo) + " " + str(cobblebrute.elo)
                      + " " + str(life_from_the_loam.elo) + " " + str(homicidal_seclusion.elo))
    def test_votes_use_elo(self):
        bad_card = Card(name='Baddie',elo=1000,votes=1000)
        good_card = Card(name='Goodie',elo=1900,votes=1000)
        good_card.save()
        bad_card.save()
        response = self.client.post('/vote/', {'voted_for':'Goodie', 'voted_against':'Baddie'})
        return self.assertEqual(Card.objects.get(name='Goodie').elo,1902) #minimum elo gain
    def test_all_cards_have_images(self):
        from django.contrib.staticfiles import finders
        for card in Card.objects.all():        
            if finders.find("coolcards/images/cards/"+card.get_pic_name()) != None:
                pass
            else:
                self.fail(card.name + " has no picture.")
    def test_all_cards_have_oracle_definitions(self):
        for card in Card.objects.all():        
            try:
                card.get_oracle_data()
            except:
                self.fail(card.name + " has no oracle data.")
        