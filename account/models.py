from django.contrib.auth.models import User
from django.db import models
from programme.coeur.models import Location

class User_Profile(models.Model):
    user        = models.OneToOneField(User)
    fonction    = models.CharField("titre/fonction", max_length=40)
    telephone   = models.IntegerField(max_length=10, null=True, blank=True)
    location    = models.ForeignKey(Location)
    
    def __unicode__(self):
        return self.user.get_full_name()