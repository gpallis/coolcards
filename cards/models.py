from django.db import models
import xml.etree.ElementTree as ET

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=200)
    elo = models.IntegerField(default=1000)
    votes = models.IntegerField(default=0)
    pic_url = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["-elo"]
    
class Oracle(models.Model):
    #Oracle entries for cards.
    name = models.CharField(max_length = 200)
    type = models.CharField(max_length = 200)
    rules = models.CharField(max_length = 2500, null=True)
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
        oracle_entry = Oracle(name=card.find('name').text,type=card.find('type').text,rules=card.find('rules').text)
        oracle_entry.save()
        
def getCardData(name,datatype):
    tree = ET.parse("/myRootFiles/cardlist_truncated.xml")
    root = tree.getroot()
    
    card = root.find("./cards/card/[name='" + name + "']")
    return card.find(datatype).text