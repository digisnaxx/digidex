from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from copwatch.models import Officer

register = template.Library()

@register.filter
def prepend_dollars(dollars):
    if dollars:
        dollars = round(float(dollars), 2)
        return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
    else:
        return ''


@register.filter
def get_vehicles(pk):
    officer = Officer.objects.filter(pk=pk).all()
    vehicles = officer.vehicle_set.all()
    return vehicles