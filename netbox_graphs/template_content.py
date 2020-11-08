from extras.plugins import PluginTemplateExtension

from .models import Graph


def button_template(template_context):
    show_graphs = Graph.objects.filter(
        type__model=template_context.context["object"].__class__.__name__.lower()
    ).exists()
    return template_context.render(
        "netbox_graphs/button.html",
        extra_context={
            "object_pk": template_context.context["object"].pk,
            "type": template_context.context["object"].__class__.__name__.lower(),
            "show_graphs": show_graphs,
        },
    )


class DeviceGraphButton(PluginTemplateExtension):
    model = "dcim.device"

    def buttons(self):
        return button_template(self)


class SiteGraphButton(PluginTemplateExtension):
    model = "dcim.site"

    def buttons(self):
        return button_template(self)


## Does not work needs fixing
class VirtualizationVMIntfGraphButton(PluginTemplateExtension):
    model = "virtualization.vminterface"

    def buttons(self):
        print("VM Interface")
        return button_template(self)


## Does not work needs fixing
class IntfGraphButton(PluginTemplateExtension):
    model = "dcim.interface"

    def left_page(self):
        print("DCIM Interface")
        return button_template(self)


class ProviderGraphButton(PluginTemplateExtension):
    model = "circuits.provider"

    def left_page(self):
        return button_template(self)


template_extensions = [
    DeviceGraphButton,
    SiteGraphButton,
    VirtualizationVMIntfGraphButton,
    IntfGraphButton,
    ProviderGraphButton,
]
