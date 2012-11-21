from django.db import models
from cards.models import Card

# Create your models here.
class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voter = models.CharField(max_length=2000)
    voted_for = models.ForeignKey(Card, related_name = 'card_voted_for_set')
    voted_against = models.ForeignKey(Card, related_name = 'card_voted_against_set')
    class Meta:
        ordering = ['-timestamp']
    def __unicode__(self):
        return self.voter + ' chose ' + self.voted_for.name + " over " + self.voted_against.name