#encoding=utf-8
from coeur.models import Matiere, Location, Domaine, Promotion, \
    Specialite
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.encoding import iri_to_uri
from account.models import User_Profile


    


class MatiereAdmin(admin.ModelAdmin):
    list_display = ("titre", "promotion", "specialite", "responsable", "campus", "domaine", "nombre_seances", "nombre_heures", "credit", "coef")
    
    fieldsets = (
        (None, {
            'fields': (('promotion', 'specialite'), 'domaine', 'titre', ('credit', 'heures', 'coef'))
        }),
        
        ('equipe pédagogique', {
            'classes': (['wide', 'extrapretty']),
            'fields': ('responsables',)
        }),
        ('Description', {
            'classes': (['wide', 'extrapretty']),
            'fields': ('introduction', 'objectifs', 'competences', 'certifications', 'programme', 'prerequis', 'relation', 'methodes', 'mode_evaluation', 'ressource_reference', 'commentaires')
        }),
               
    )

    save_on_top = True
    
    filter_horizontal = ('responsables',)
    
    list_filter = ('promotion','domaine', 'responsables', )
    
    def campus(self, obj):
        return ", ".join(["%s" % a for a in obj.locations])
        

    def save_model(self, request, obj, form, change):

        # corrige le bug de ckeditor qui ajoute un <br /> par defaut
        if ' '.join(obj.introduction.split()) == "<br />":
            obj.introduction = ""
        if ' '.join(obj.programme.split()) == "<br />":
            obj.programme = ""
        if ' '.join(obj.methodes.split()) == "<br />":
            obj.methodes = ""
        if ' '.join(obj.ressource_reference.split()) == "<br />":
            obj.ressource_reference = ""
        obj.save()
        
#    def change_view(self, request, object_id, extra_context=None):
#        result = super(MatiereAdmin, self).change_view(request, object_id, extra_context)
#
#
#        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
#            result['Location'] = iri_to_uri(Matiere.objects.get(pk=object_id).get_absolute_url())
#        return result
        
admin.site.register(Matiere, MatiereAdmin)
admin.site.register((Location, Domaine, Promotion, Specialite,))
