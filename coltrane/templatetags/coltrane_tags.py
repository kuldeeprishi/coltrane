from django import template
#from coltrane.models import Entry, Link
from django.db.models import get_model



    
def do_latest_content(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content tag' takes exactly 4 arguments. Only {0} arguments supplied.".format(len(bits)))
    model_args = bits[1].split(".")
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("'get_latest_content' must be an 'application name'.'model name' string.")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: {0}".format(bits[1]))
    return LatestContentNode(model, bits[2], bits[4])

class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.model = model  
        self.num = num
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

register = template.Library()
register.tag('get_latest_content', do_latest_content)

# get_latest_content coltrane.links 5 as latest_linnks