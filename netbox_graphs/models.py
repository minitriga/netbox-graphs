from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from extras.choices import TemplateLanguageChoices
from extras.registry import registry
from extras.utils import FeatureQuery
from utilities.querysets import RestrictedQuerySet
from utilities.utils import render_jinja2

#
# Graphs
#

SUPPORTED_MODELS = {
    "dcim": ["interface", "device", "site"],
    "circuits": ["provider"],
    "virtualization": ["vminterface"],
}

registry["model_features"]["netbox_graphs"] = SUPPORTED_MODELS


class Graph(models.Model):
    type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s",
        limit_choices_to=FeatureQuery("netbox_graphs"),
    )

    weight = models.PositiveSmallIntegerField(default=1000)
    name = models.CharField(max_length=100, verbose_name="Name")
    template_language = models.CharField(
        max_length=50, choices=TemplateLanguageChoices, default=TemplateLanguageChoices.LANGUAGE_JINJA2
    )
    source = models.CharField(max_length=500, verbose_name="Source URL")
    link = models.URLField(blank=True, verbose_name="Link URL")

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("type", "weight", "name", "pk")  # (type, weight, name) may be non-unique

    def __str__(self):
        return self.name

    def embed_url(self, obj):
        context = {"obj": obj}

        if self.template_language == TemplateLanguageChoices.LANGUAGE_DJANGO:
            template = Template(self.source)
            return template.render(Context(context))

        elif self.template_language == TemplateLanguageChoices.LANGUAGE_JINJA2:
            return render_jinja2(self.source, context)

    def embed_link(self, obj):
        if self.link is None:
            return ""

        context = {"obj": obj}

        if self.template_language == TemplateLanguageChoices.LANGUAGE_DJANGO:
            template = Template(self.link)
            return template.render(Context(context))

        elif self.template_language == TemplateLanguageChoices.LANGUAGE_JINJA2:
            return render_jinja2(self.link, context)
