from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'coeur.views',
    #url(r'^rtf$', 'export_all_rtf', name="export_all_rtf"),
    url(r'^en_pdf$', 'export_all', name='export_all'),
    url(r'^(?P<promo>\w+)/(?P<matiere>\d+)/export$', 'export', name='export'),
    url(r'^(?P<promo>\w+)/(?P<matiere>\d+)', 'matiere', name='matiere'),
    url(r'^(?P<promo>\w+)', 'programme', name="programme_promo"),

    url(r'', 'index', name="index"),
)