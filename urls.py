from django.conf.urls.defaults import *
from wordcloud.views import *
import os
from django.views.generic.simple import direct_to_template

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    (r'^search/$', search_page),
    (r'^cloud/$', direct_to_template,
     {'template': 'canvas_cloud.html'}),
    (r'^tag/([^\s]+)/$', tag_page),
    (r'^profile/$', profile_page),


    # Session Management
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,
         {'template': 'registration/register_success.html'}),

    # Account Management
    (r'^save/$', corpus_save),
    (r'^settings/$', profile_settings_page),
    (r'^settings/saved/$', direct_to_template,
        {'template': 'settings_saved.html'}),

    # Site Media
    (r'site_media/(?P<path>.*)$','django.views.static.serve',
         {'document_root': site_media}),

    # Examples:
    # url(r'^$', 'django_wordcloud.views.home', name='home'),
    # url(r'^django_wordcloud/', include('django_wordcloud.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
