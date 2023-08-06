from django.urls import path, include

app_name = "gdaps.core"
# automatically include Django-REST-Framework's URLs
urlpatterns = []
# FIXME: rest_framework namespace can't be chained?
# urlpatterns = [path("", include("rest_framework.urls"))]
