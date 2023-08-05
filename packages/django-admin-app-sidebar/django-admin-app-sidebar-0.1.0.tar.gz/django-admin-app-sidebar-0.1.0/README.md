# django-admin-app-sidebar

A django application that add portlets in right sidebar at app level.


## Install

```shell
pip install django-admin-app-sidebar
```

## Usage

**pro/settings.py**

**Note:**

- We used template override in django_admin_app_sidebar, so we MUST include django_admin_app_sidebar in INSTALLED_APPS.
- The app django_static_fontawesome is optional choice. If you are using icon in sidebar portlet you may need it.

```python
INSTALLED_APPS = [
    ...
    'django_static_fontawesome', # Optional, and install by yourself
    'django_admin_app_sidebar',
    ...
]
```

**app/__init__.py**

**Note:**

- We are going to set an example portlet in AppConfig.ready

```python
default_app_config = "django_admin_app_sidebar_example.apps.DjangoAdminAppSidebarExampleConfig"
```

**app/apps.py**

**Note:**

- By default, django_admin_app_sidebar provides an simple navigation portlet. Just init a navigation instance, and register it as a portlet.
- Navigation item config
    - `title`: required. the navigation link title.
    - `url`: required. the navigation link url.
    - `icon`: optional. icon class just before link title.
    - `target`: optional. link target, target=_blank means open in new window or tab.
    - `depth`: optional. depth=2 will add 20px indent to the link item. And depth=3 will add 40px.
    - if item=="-", then display a seperator.

```python
from django.apps import AppConfig
from django_admin_app_sidebar.portlets import register_portlet
from django_admin_app_sidebar.portlets import SidebarNavigation
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

class DjangoAdminAppSidebarExampleConfig(AppConfig):
    name = 'django_admin_app_sidebar_example'

    def ready(self):
        navigation = SidebarNavigation("Navigation", [{
            "title": "Home",
            "url": "/admin/",
            "icon": "fas fa-home",
        },"-",{
            "title": "Example Index",
            "url": reverse_lazy("admin:app_list", kwargs={"app_label": self.name}),
            "icon": "fas fa-building",
        },{
            "title": "Category Manager",
            "url": reverse_lazy("admin:{0}_{1}_changelist".format(self.name, "category")),
            "icon": "fas fa-tree",
            "depth": 2,
        },{
            "title": "Book Manager",
            "url": reverse_lazy("admin:{0}_{1}_changelist".format(self.name, "book")),
            "icon": "fas fa-file",
            "depth": 2,
        }])
        register_portlet(navigation, app_label=self.name, extra_css=[
            "fontawesome/css/all.min.css",
        ])
```

## Exported APIs

- django_admin_app_sidebar.portlets.Portlet

    It is a portlet base class. You can use any callable function instead of Portlet, simply take a context parameter and return rendered html string.

- django_admin_app_sidebar.portlets.SidebarNavigation

    A simple navigation portlet.

- django_admin_app_sidebar.portlets.register_portlet

    Register a portlet to the system.

## Detail of django_admin_app_sidebar.portlets.register_portlet 

```python
def register_portlet(render, order=0, app_label=None, model_name=None,
        show_in_app=True,
        show_in_app_index=False,
        show_in_model_site=False,
        show_in_model_changelist=False,
        show_in_model_change=False,
        show_in_model_add=False,
        show_in_model_history=False,
        extra_css=None,
        extra_js=None):
        ...
```

**Parameters:**

- `render`: required, it is a Portlet instance or a equivalent callable function.
- `order`: portlet display order
- `app_label`: in which application views the portlet will be displayed
    - if None, the portlet will be displayed in all application.
- `model_name`: in which model related view the portlet will be diplayed
    - if None, the portlet will be displayed in all views of the application
- `show_in_app`: default to True. show the portlet in all views under the application.
- `show_in_app_index`: default to False. show the portlet in app index view. app_label is required.
- `show_in_model_site`: default to False. show the portlet in all views related to the model
- `show_in_model_changelist`: default to False. show the portlet in changelist view.
- `show_in_model_change`: default to False. show the portlet in change view.
- `show_in_model_add`: default to False. show the portlet in add view.
- `show_in_model_history`: default to False. show the portlet in history view. **Not implemented yet**


## Releases

### v0.1.0 @todo

- First release.