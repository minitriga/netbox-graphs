from django import forms
from django.contrib import admin

from .models import Graph

#
# Graphs
#


class GraphForm(forms.ModelForm):
    class Meta:
        model = Graph
        exclude = ()
        help_texts = {
            "template_language": '<a href="https://jinja.palletsprojects.com">Jinja2</a> is strongly recommended for '
            "new graphs."
        }
        widgets = {
            "source": forms.Textarea,
            "link": forms.Textarea,
        }


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Graph", {"fields": ("type", "name", "weight")}),
        ("Templates", {"fields": ("template_language", "source", "link"), "classes": ("monospace",)}),
    )
    form = GraphForm
    list_display = [
        "name",
        "type",
        "weight",
        "template_language",
        "source",
    ]
    list_filter = [
        "type",
        "template_language",
    ]
