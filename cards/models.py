from django.db import models
from django.conf import settings
import xml.etree.ElementTree as ET
import re

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=200)
    elo = models.IntegerField(default=1000)
    votes = models.IntegerField(default=0)
    pic_url = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["-elo","name"]
    def get_pic_name(self):
        lowercase = self.name.lower()
        hyphenated = re.sub(' ','-',lowercase)
        final = re.sub('[,\']','',hyphenated)
        return final + ".jpg"
    def get_oracle_data(self):
        return Oracle.objects.get(name=self.name)
    def get_html_bio(self):
        #ugly, but required as linebreaks aren't replicated in the html otherwise
        rules = self.get_oracle_data().rules
        if not rules:
            rules = '' #to handle rule-less cards
        
        type = self.get_oracle_data().type
        
        finalText = '<p class="card-rules">' + type + self.get_pt_string() + '</p>'
        ruleslines = rules.split("\n")
        for line in ruleslines:
            finalText += '<p class="card-rules">' + line + '</p>'
        finalText = re.sub(
            '{(.)}', ('<img src="' + settings.STATIC_URL + 'coolcards/images/symbols/-' + r'\1' + '-.png" style="vertical-align:-2">'),
            finalText)
        return finalText
    def get_pt_string(self):
        my_oracle = self.get_oracle_data()
        if my_oracle.power and my_oracle.toughness:
            return ' [' + str(my_oracle.power) + '/' + str(my_oracle.toughness) + ']'
        else:
            return ''
    
class Oracle(models.Model):
    #Oracle entries for cards.
    name = models.CharField(max_length = 200)
    type = models.CharField(max_length = 200)
    rules = models.CharField(max_length = 2500, null=True)
    power = models.CharField(max_length = 20, null=True) #char not int used to forestall '0.5, *, *+1, etc
    toughness = models.CharField(max_length = 20, null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
    
def saveAllOracles():
    print "hello!"
    tree = ET.parse("/myRootFiles/cardlist_truncated.xml")
    root = tree.getroot()
    
    cards = root.findall('cards/card')
    
    for card in cards:
        oracle_entry = Oracle(
            name=card.find('name').text,
            type=card.find('type').text,
            rules=card.find('rules').text,
            power=card.find('power').text,
            toughness=card.find('toughness').text,
        )
        try:
            Oracle.objects.get(name=oracle_entry.name)
        except:
            oracle_entry.save()