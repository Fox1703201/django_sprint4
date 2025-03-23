from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class RulesPageView(TemplateView):
    template_name = "pages/rules.html"


def error_403csrf(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


def error_404(request, exception):
    return render(request, "pages/404.html", status=404)


def error_405(request, exception):
    return render(request, "pages/405.html", status=405)


def error_500(request):
    return render(request, "pages/500.html", status=500)
