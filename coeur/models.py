#encoding=utf-8
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db import models
#
class Responsable(User):
    class Meta:
        proxy       = True
        ordering    = ['first_name']
    #Here you redefine the default behavior of
    #of the __unicode__ function
    def __unicode__(self):
        if self.get_full_name():
            return self.get_full_name()
        else :
            return self.username
        
    def profile(self):
        return self.get_profile()
    profile = property(profile)

    
    

class Location(models.Model):
    titre       = models.CharField("Emplacement", max_length=50)
    def __unicode__(self):
        return self.titre

    
class Enseignant(models.Model):
    nom         = models.CharField(max_length=40)
    prenom      = models.CharField(max_length=40)
    email       = models.EmailField()
    def __unicode__(self):
        return "%s %s" % (self.nom, self.prenom)

class Domaine(models.Model):
    titre       = models.CharField("domaine", max_length=50)
    order       = models.IntegerField("position dans la liste", null=True, blank=True)
    
    def __unicode__(self):
        return self.titre
    def nb_heures(self, promotion):
        total = 0
        for m in self.matiere_set.all().filter(promotion=promotion):
            total += m.nombre_heures
        return total

    def nb_credits(self, promotion):
        total = 0
        for m in self.matiere_set.all().filter(promotion=promotion):
            total += m.nombre_credits
        return total
    
    def nb_coef(self, promotion):
        total = 0
        for m in self.matiere_set.all().filter(promotion=promotion):
            total += m.nombre_coef
        return total
    
class Promotion(models.Model):
    titre       = models.CharField(max_length=10, primary_key=True)

    def __unicode__(self):
        return self.titre
    def nb_matieres(self):
        m = Matiere.objects.filter(promotion=self.pk).count()
        return m
#    def nb_intervenants(self):
#        return Enseignant.objects.filter(matiere__promotion = self.pk).count()
    def nb_seances(self):
        nb = 0;
        for m in self.matiere_set.all():
            nb += m.nombre_seances
        return nb
    def nb_heures(self):
        nb = 0
        for m in self.matiere_set.all():
            nb += m.nombre_heures
        return nb
    def nb_credits(self):
        nb = 0
        for m in self.matiere_set.all():
            nb += m.nombre_credits
        return nb
    
    def nb_coef(self):
        nb = 0
        for m in self.matiere_set.all():
            nb += m.nombre_coef
        return nb
    
    
class Specialite(models.Model):
    titre       = models.CharField(max_length=30)

    def __unicode__(self):
        return self.titre
   
class MatiereManager(models.Manager):
    def matiere_for_promotion(self, promo, domaine=None):
        
        qs = self.filter(promotion = promo).order_by("domaine")
        if domaine is not None:
            qs = qs.filter(domaine = domaine)
        return qs
    
class Matiere(models.Model):
    
    promotion   = models.ForeignKey(Promotion)
    specialite  = models.ForeignKey(Specialite, null=True, blank=True)
    
    domaine   = models.ForeignKey(Domaine, verbose_name="Domaine", null=True, blank=True)
    titre       = models.CharField(max_length=70)
    
    heures       = models.IntegerField("nombre d'heures de cours", null=True, blank=True)
#    td          = models.IntegerField("nombre de TD", null=True, blank=True)
#    tp          = models.IntegerField("nombre de TP", null=True, blank=True)
    coef        = models.IntegerField("Coefficient", null=True, blank=True)
    credit      = models.IntegerField("crédit ECTS", null=True, blank=True)
#    tp_note     = models.IntegerField("nombre de tp notés", null=True, blank=True)
#    partiel     = models.IntegerField("nombre de partiels", null=True, blank=True)
#    examen      = models.IntegerField("nombre d'examens", null=True, blank=True)
    
#    responsables= models.ManyToManyField(Responsable, through="Membership", blank=True, null=True)
    responsables= models.ManyToManyField(Responsable, blank=True, null=True)
    
    equipe_pedagogique  = models.ManyToManyField(Enseignant, blank=True, null=True)
    
    introduction        = RichTextField(blank=True)
    objectifs           = RichTextField(blank=True)
    competences         = RichTextField(verbose_name="compétences développées par l'enseignement", blank=True)
    certifications      = RichTextField(blank=True)
    programme           = RichTextField(verbose_name="programme du cours", blank=True)
    prerequis           = RichTextField(verbose_name="pré-requis", blank=True) # fusion de "relation"
    relation            = RichTextField(verbose_name="cours suivant, relation avec la matière", blank=True) #relation est maintenant "cours suivant"
    methodes            = RichTextField(verbose_name="méthodes et outils de travail", blank=True)
    mode_evaluation     = RichTextField(verbose_name="mode d'évaluation", blank=True)
    ressource_reference = RichTextField(verbose_name="ressources de référence", blank=True)
    
    commentaires        = models.TextField(blank=True)
    
    objects = MatiereManager()
    
    def __unicode__(self):
        return self.titre
    
    def _get_nombre_seances(self):
        return int(self.heures/1.75) if self.heures else 0
    nombre_seances = property(_get_nombre_seances)
    
    def _get_nombre_heures(self):
        return self.heures if self.heures else 0
    nombre_heures = property(_get_nombre_heures)
    
    def _get_nombre_credits(self):
        return self.credit if self.credit else 0
    nombre_credits = property(_get_nombre_credits)
    
    def _get_nombre_coef(self):
        return self.coef if self.coef else 0
    nombre_coef = property(_get_nombre_coef)
    
    def _get_responsables_to_string(self):
        str = ""
        if self.responsables.all():
#            print self.responsables.all()
            
            for i, r in enumerate(self.responsables.all()):
                str += ", " if i > 0 else ''
                if r.get_full_name():
                    str += r.get_full_name()
                else :
                    str += r.username()

        return str

    responsable = property(_get_responsables_to_string)
    
    def _get_locations(self):
        locations = []
        if self.responsables.all():
            
            for r in self.responsables.all():
                if r.get_profile():
                    if not r.get_profile().location in locations :
                        locations.append(r.get_profile().location)
        return locations
    locations = property(_get_locations)
    
    @models.permalink
    def get_absolute_url(self):
        return ('matiere', (), {
            'promo': self.promotion,
            'matiere': self.id,
            })
        
#class Membership(models.Model):
#    
#    matiere     = models.ForeignKey(Matiere)
#    user        = models.ForeignKey(Responsable)
#    
#    class Meta:
#        db_table = 'coeur_matiere_responsables'