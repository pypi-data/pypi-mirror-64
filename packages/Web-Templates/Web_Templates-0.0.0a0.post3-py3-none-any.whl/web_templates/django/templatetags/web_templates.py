from django import template
# from django.template.defaultfilters import stringfilter
from collections import OrderedDict
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.html import html_safe

register = template.Library()


# @register.filter(name = 'route')
# def breadcrumb(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

@register.inclusion_tag("web-templates/breadcrumb.html",takes_context=True)
def breadcrumbs(context, index = None) :
    """Generates a breadcrumb from request.path for the current context

    :param context: The Django template context
    :param index: Label for the root link
    :return: The links comprising the bread crumb
    """
    # route = OrderedDict()
    links = []
    parts = context['request'].path_info.rstrip("/").split("/") if index else context['request'].path_info.strip("/").split("/")
    for cntr, item in enumerate(parts[:-1]) :
        path = "/".join(parts[:cntr+1]) # "/" + "/".join(parts[:index]) if index != len(parts) - 1 else None
        try :
            match = resolve("/{path}/".format(path) if path else "/")
        except :
            match = None
        # route[item if path else index] = None if match is None else (reverse(match.view_name, args=match.args, kwargs=match.kwargs)) # , urlconf=None, current_app=None
        if match is None :
            links.append(format_html('<span>{}</span>', item if path else index))
        else :
            links.append(format_html('<a href="{}">{}</a>',
               reverse(match.view_name, args=match.args, kwargs=match.kwargs),
               item if path else index))
    return {"route" : links} # "route": route,
# Use the following when using route
# {% for part, path in route.items %}
# {% if path is None %}
# <span>{{ part }}</span>
# {% else %}
# <a href="{{ path|safe }}}">{{ part }}</a>
# {% endif %}
# {% endfor %}

