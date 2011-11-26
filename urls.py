from django.conf.urls.defaults import *
from django.contrib import admin
from programme import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',

    (r'^ckeditor/', include('ckeditor.urls')),   

    (r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    

)

if settings.DEBUG :
    urlpatterns +=patterns("",(r'^media_site/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_DIR+'/media_site/'}))
    
    
urlpatterns += patterns("",(r'', include('coeur.urls')))