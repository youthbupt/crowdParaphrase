from django.conf.urls import patterns, include, url
from django.contrib import admin
from userViews import *
from HITModel.views import *
import sys

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdParaphrase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^buildDatabaseFromFile/?$', InsertFromFile),
    url(r'^labelPage/?$', getLabelPage),
    url(r'^$', getHomePage),
    url(r'^userLogout/?$', userLogout),
    url(r'^userLogin/?$', userLogin),
    url(r'^checkLogin/?$', checkLogin),
    url(r'^removeParaphrase/?$', cleanParaphraseDatabase)
    # url(r'^admin/', include(admin.site.urls)),
)
