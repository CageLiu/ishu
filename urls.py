from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from idushu.apps.dushu import views as dv
#from idushu.apps.forum import views as fv

urlpatterns = patterns('',
        (r'^$',dv.index),
        (r'^index/$',dv.index),
        (r'^login/$',dv.login),
        (r'^logout/$',dv.logout),
        (r'^reg/$',dv.register),
        (r'^addposts/$',dv.assign_method,{'view':dv.addposts}),
        (r'^addbook/$',dv.assign_method,{'view':dv.addbook}),
        (r'^addreply/$',dv.assign_method,{'view':dv.addreply}),
        (r'^check/(?P<models>\w+)/(?P<fields>\w+)/$',dv.checking),
        (r'^confirmail/$',dv.confirmail),
        (r'^(?P<action>edit)/(?P<models>\w+)/(?P<args>\d+)/$',dv.viewitem),
        (r'^(?P<models>\w+)/$',dv.viewitem),
        (r'^(?P<models>\w+)/(?P<args>\d+)/$',dv.viewitem),
        #(r'^logout/$',dv.logout),
        #(r'^login/$',dv.login,{'view':dv.login}),
        #(r'^$',dv.index,{'view':dv.login}),
)
