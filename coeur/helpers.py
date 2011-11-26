
    
    
from django.core.context_processors import request
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from pyth.plugins.rtf15.writer import Rtf15Writer
from pyth.plugins.xhtml.reader import XHTMLReader


def create_rtf(matiere):
    
    httpResponse = render_to_response('coeur/matiere_rtf.html', {'matiere'      : matiere,
                                                     })
    filename = '/tmp/rtf/%s %s.rtf' % (matiere.promotion, matiere.titre)
    f = open(filename, 'w')
    doc = XHTMLReader.read(httpResponse.content, "")
    Rtf15Writer.write(doc , f)
    
    return filename
