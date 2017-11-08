import os

from mako.template import Template

template = Template(open(
    os.path.join(os.path.dirname(__file__), "tmpl.mako")
).read())
