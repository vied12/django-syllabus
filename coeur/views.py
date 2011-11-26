#encoding=utf-8

from coeur.models import Matiere, Promotion, Domaine
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
import cStringIO as StringIO
import cgi
import ho.pisa as pisa
import time
import zipfile

@login_required
def index(request):
    
#    from django.core.mail import send_mail
#    send_mail('Subject here', 'Here is the message.', 'from@example.com', ['vied12@gmail.com'], fail_silently=False)
    
    promotions  = Promotion.objects.all().order_by("titre")
    

    
    return render_to_response('coeur/index.html', {'promotions' : promotions }, context_instance=RequestContext(request))

def export_all_rtf(request):
    import os
    
    
    erreurs = []
    fichiers = []
    for matiere in Matiere.objects.all():
        print "%s %s" %(matiere.promotion, matiere.titre)
        try :
            fn = helpers.create_rtf(matiere)
            fichiers.append(fn)
            
            
        except :
            print "~~  ERREUR %s %s" %(matiere.promotion, matiere.titre)
            erreurs.append(matiere)
    
    print "compression de ", fichiers
    zip = zipfile.ZipFile('/tmp/toto.zip', 'w', zipfile.ZIP_STORED)
    for f in fichiers:
        zip.write(f, os.path.basename(f))
        

    zip.close

    return render_to_response('coeur/exportation_rtf.html', {"erreurs" : erreurs}, context_instance=RequestContext(request))

@login_required
def programme(request, promo):
    
    promo = get_object_or_404(Promotion, pk=promo)
    domaines  = Domaine.objects.all().order_by("order")
    add_url     = urlresolvers.reverse('admin:coeur_matiere_add')
    
    res = []

    for cat in domaines : 
        dict = {cat : {"matieres" :Matiere.objects.matiere_for_promotion(promo, cat), "total_heures" :cat.nb_heures(promo), "total_credits" : cat.nb_credits(promo), "total_coef" : cat.nb_coef(promo)} }

        res.append(dict)

    return render_to_response('coeur/programme.html', {'promo' : promo, 
                                                       'programme'  : res, 
                                                       'domaines' : domaines,
                                                       'add_url'    : add_url,
                                                       }, context_instance=RequestContext(request))

@login_required
def matiere(request, promo, matiere):
    matiere     = get_object_or_404(Matiere, pk=matiere)
    change_url  = urlresolvers.reverse('admin:coeur_matiere_change', args=(matiere.id,))
    add_url     = urlresolvers.reverse('admin:coeur_matiere_add')
    
    return render_to_response('coeur/matiere.html', {'matiere'      : matiere, 
                                                     'change_url'   : change_url, 
                                                     'add_url'      : add_url,
                                                     }, context_instance=RequestContext(request))
    
@login_required 
def export(request, promo, matiere):

    matiere = Matiere.objects.get(pk=matiere)
    result =  write_pdf('coeur/matiere_pdf.html',{
        'pagesize' : 'A4',
        'matiere' : matiere,
        'site':Site.objects.get(pk=1),
         })
    response = http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    import unicodedata
    titre = unicodedata.normalize('NFKD', matiere.titre).encode('ascii','ignore')
    response['Content-Disposition'] = "attachment; filename=\"%s - %s.pdf\"" % (matiere.promotion, titre)
    return response
    
@login_required 
def export_all(request):
    zip_path = '/tmp/syllabus.zip'
    zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED)
    
    for matiere in Matiere.objects.all():

        result = write_pdf('coeur/matiere_pdf.html',{
            'pagesize' : 'A4',
            'matiere' : matiere,
            'site':Site.objects.get(pk=1),
             })
        
        import unicodedata
        titre = unicodedata.normalize('NFKD', matiere.titre).encode('ascii','ignore')
        titre = titre.replace("/", "-")
        titre = titre.replace("\\", "-")
        print titre
        file = open("/tmp/syllabus/%s - %s.pdf" % (matiere.promotion, titre), "w")
        file.write(result.getvalue())
        file.close()
        zip.write("/tmp/syllabus/%s - %s.pdf" % (matiere.promotion, titre))
    
    zip.close()
    zip_file = open(zip_path, 'r')
    response = http.HttpResponse(zip_file.read(), mimetype='application/zip')
    
    response['Content-Disposition'] = "attachment; filename=syllabus.zip"
    return response
        
        


def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result, encoding="UTF-8")
    if not pdf.err:
        return result
    return http.HttpResponse('Gremlin\'s ate your pdf! %s' % cgi.escape(html))