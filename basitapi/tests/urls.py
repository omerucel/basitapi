from django.conf.urls import patterns, url

from basitapi.urlpatterns import format_suffix_patterns
from basitapi.tests.integration_tests.views_tests import SampleView, SampleErrorView, SampleSessionView

urlpatterns = patterns('',
    url(r'sample$', SampleView.as_view()),
    url(r'error$', SampleErrorView.as_view()),
    url(r'session$', SampleSessionView.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
