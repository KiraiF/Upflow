from django import template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag(takes_context=True)
def render_comment(context, comment):
    return render_to_string(
        'core/comment_partial.html',
        {'comment': comment},
        request=context['request']
    )