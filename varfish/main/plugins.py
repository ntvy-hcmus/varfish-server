from projectroles.plugins import ProjectAppPluginPoint
from .urls import urlpatterns

class ProjectAppPlugin(ProjectAppPluginPoint):
    """Plugin for registering app with Projectroles"""
    name = 'VarFish'
    title = 'VarFish'
    urls = urlpatterns
    # ...

    icon = 'ship'

    entry_point_url_id = 'main:main'

    description = 'VarFish'

    #: Required permission for accessing the app
    app_permission = 'varfish.main.view_data'

    #: Enable or disable general search from project title bar
    search_enable = False

    #: List of search object types for the app
    search_types = []

    #: Search results template
    search_template = None

    #: App card template for the project details page
    details_template = 'main/temp.html'

    #: App card title for the project details page
    details_title = 'VarFish App Overview'

    #: Position in plugin ordering
    plugin_ordering = 100

