from django.conf.urls import patterns, url

from basitapi.urlpatterns import format_suffix_patterns
from basitapi.tests.integration_tests import views_tests

urlpatterns = patterns('',
    url(r'sample$', views_tests.SampleView.as_view()),
    url(r'error$', views_tests.SampleErrorView.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)
