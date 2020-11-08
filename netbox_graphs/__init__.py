__version__ = "0.0.1"

from extras.plugins import PluginConfig


class GraphsConfig(PluginConfig):
    """Plugin configuration for the netbox_graphs plugin."""

    name = "netbox_graphs"
    verbose_name = "Netbox Graphs"
    version = __version__
    author = "Alex Gittings"
    description = "A plugin for NetBox Graphs."
    base_url = "graphs"
    required_settings = []
    min_version = "2.8.1"
    default_settings = {}
    caching_config = {}


config = GraphsConfig  # pylint:disable=invalid-name
