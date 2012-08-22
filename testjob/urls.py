from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from testapp import views

id_pattern = '([_\-a-zA-Z0-9]{1,50})'
model_name_pattern = '([_a-zA-Z0-9]{1,50})'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^testapp/$', views.lst),
    url(r'table_ajax/%(id_pattern)s/$' % locals(), views.table_ajax),
    url(r'table_update_ajax/%(id_pattern)s/$' % locals(), views.table_update_ajax),
    url(r'table_struct_ajax/', views.table_struct_ajax),
    url(r'table_add_ajax/%(model_name_pattern)s/' % locals(), views.table_add_ajax),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
