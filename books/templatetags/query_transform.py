from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """Is used for changing just some parameters in a get request when generating a link.
    Taken from the Stack Overflow anser https://stackoverflow.com/questions/46026268/how-to-preserve-get-parameters-during-pagination-in-django by addmoss."""

    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
