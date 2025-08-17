from django import template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag(takes_context=True)
def render_post(context, post):
    # This is the key part.
    return render_to_string(
        'core/post_partial.html',
        {'post': post},
        request=context['request']
    )
@register.filter
def get_vote(votedby_dict, username):
    if isinstance(votedby_dict, dict):
        return votedby_dict.get(username)
    return None