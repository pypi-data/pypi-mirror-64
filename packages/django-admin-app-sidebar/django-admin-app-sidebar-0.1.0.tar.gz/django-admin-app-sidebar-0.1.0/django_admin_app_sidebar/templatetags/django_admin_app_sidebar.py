from django.template import Library
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from ..portlets import get_portlets

register = Library()

@register.simple_tag(takes_context=True)
def portlets_render(context):
    request = context.get("request", None)
    if not request:
        return ""
    if "opts" in context:
        opts = context["opts"]
        app_label = opts.app_label
        model_name = opts.model_name
    else:
        if "app_label" in context:
            app_label = context["app_label"]
        else:
            app_label = ""
        if "model_name" in context:
            model_name = context["model_name"]
        else:
            model_name = None
    url_name = request.resolver_match.url_name
    portlet_htmls = []
    extra_css_paths = []
    extra_js_paths = []
    portlets = get_portlets(app_label, model_name, url_name)
    for portlet in portlets:
        for css in (portlet["extra_css"] or []):
            if not css in extra_css_paths:
                extra_css_paths.append(css)
        for js in (portlet["extra_js"] or []):
            if not js in extra_js_paths:
                extra_js_paths(js)
        html = portlet["render"](context)
        portlet_htmls.append(html)
    return render_to_string("django-admin-app-sidebar/sidebar-portlets.html", {
        "portlets": portlet_htmls,
        "extra_css": extra_css_paths,
        "extra_js": extra_js_paths,
        "fix_changelist_problem": url_name.endswith("_changelist") and len(portlets),
        "fix_changeform_problem": (url_name.endswith("_change") or url_name.endswith("_add")) and len(portlets),
    })

@register.simple_tag
def sidebar_navigation_url(item, request):
    url = item["url"]
    url_args = item.get("url_args", [])
    url_kwargs = item.get("url_kwargs", {})
    if callable(url):
        return url(request, *url_args, **url_kwargs)
    else:
        try:
            url = reverse(item.url, args=url_args, kwargs=url_kwargs)
        except:
            return url

