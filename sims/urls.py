from django.conf.urls import url
from .views import *

urlpatterns = [

    # url(r'^index$', index, name='index'),

    #url(r'^register$', register, name='register'),
    url(r'^login$', loginpage, name='login'),
    url(r'^logout$', logout_user, name='logout'),

    url(r'^$', dashboard, name='dashboard'),

    url(r'^new_sim/(?P<pk>\d+)$', new_sim, name='new_sim'),
    url(r'^new_sim$', new_sim, name='new_sim'),

    url(r'^update_sim/(?P<pk>\d+)$', update_sim, name='update_sim'),
    url(r'^update_sim$', update_sim, name='update_sim'),

    url(r'^delete_sim$', delete_sim, name='delete_sim'),
    url(r'^delete_sim/(?P<pk>\d+)$', delete_sim, name='delete_sim'),

    url(r'^issues$', issues, name='issues'),

    url(r'^sims$', sims, name='sims'),

    url(r'^carriers/(?P<pk>\d+)$', carriers, name='carriers'),

    url(r'^new_carrier$', new_carrier, name='new_carrier'),

    url(r'^update_carrier/(?P<pk>\d+)$', update_carrier, name='update_carrier'),
    url(r'^delete_carrier/(?P<pk>\d+)$', delete_carrier, name='delete_carrier'),

    url(r'^upload$', upload_vsim_mgmt, name='upload'),
    url(r'^upload_single_vsim$', upload_single_vsim_mgmt, name='upload_single_vsim'),
    url(r'^upload_package$', upload_package, name='upload_package'),

    url(r'^analytics$', analytics, name='analytics'),
    url(r'^plmn_sets$', plmn_sets, name='plmn_sets'),


]