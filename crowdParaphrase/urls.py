from django.conf.urls import patterns, include, url
from django.contrib import admin
from userViews import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdParaphrase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^buildDatabaseFromFile/', HITModel.views.InsertFromFile),
    url(r'^labelPage/?$', getLabelPage),
    url(r'^$', getHomePage),
    url(r'^userLogout/?$', userLogout),
    url(r'^userLogin/?$', userLogin),
    url(r'^checkLogin/?$', checkLogin),
    url(r'^/removeParaphrase?$', HITModel.views.cleanParaphraseDatabase),
    # url(r'^admin/', include(admin.site.urls)),
)
