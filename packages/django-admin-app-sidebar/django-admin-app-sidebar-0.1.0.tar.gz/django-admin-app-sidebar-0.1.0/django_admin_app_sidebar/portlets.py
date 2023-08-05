from django.template.loader import render_to_string
from django.urls import reverse

portlets = []

def register_portlet(render, order=0, app_label=None, model_name=None,
        show_in_app=False,
        show_in_app_index=False,
        show_in_model_site=True,
        show_in_model_changelist=False,
        show_in_model_change=False,
        show_in_model_add=False,
        show_in_model_history=False,
        extra_css=None,
        extra_js=None):
    portlets.append({
        "render": render,
        "order": order,
        "app_label": app_label,
        "model_name": model_name,
        "show_in_app": show_in_app,
        "show_in_app_index": show_in_app_index,
        "show_in_model_site": show_in_model_site,
        "show_in_model_changelist": show_in_model_changelist,
        "show_in_model_change": show_in_model_change,
        "show_in_model_add": show_in_model_add,
        "show_in_model_history": show_in_model_history,
        "extra_css": extra_css,
        "extra_js": extra_js,
    })

def get_portlets(app_label, model_name, url_name):
    results = []
    for portlet in portlets:
        show_flag = False
        if portlet["app_label"] is None or portlet["app_label"] == app_label:
            if portlet["show_in_app"]:
                show_flag = True
            else:
                if portlet["show_in_app_index"] and url_name == "app_list":
                    show_flag = True
                else:
                    if portlet["model_name"] is None or portlet["model_name"] == model_name:
                        if portlet["show_in_model_site"]:
                            show_flag = True
                        else:
                            if (portlet["show_in_model_changelist"] and url_name == "{}_{}_changelist".format(app_label, model_name)):
                                show_flag = True
                            if (portlet["show_in_model_change"] and url_name == "{}_{}_change".format(app_label, model_name)):
                                show_flag = True
                            if (portlet["show_in_model_add"] and url_name == "{}_{}_add".format(app_label, model_name)):
                                show_flag = True
                            if (portlet["show_in_model_history"] and url_name == "{}_{}_history".format(app_label, model_name)):
                                show_flag = True
        if show_flag:
            results.append(portlet)
    results.sort(key=lambda e: e["order"])
    return results


class Portlet(object):

    def __call__(self, context=None):
        raise NotImplementedError("Please implement portlet's __call__ method...")


class SidebarNavigation(Portlet):

    def __init__(self, title, navigation):
        self.title = title
        self.navigation = navigation

    def __call__(self, context=None):
        return render_to_string("django-admin-app-sidebar/sidebar-navigation.html", {
            "title": self.title,
            "navigation": self.navigation,
            "request": context["request"],
        })
