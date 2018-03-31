from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.home),       
    url(r'^login$', views.login),       
    url(r'^signup$', views.register),       
    url(r'^logout$', views.logoff),   
    url(r'^cBill$', views.seebill),     
    url(r'^addBill$', views.addingBill),   
    url(r'^cTask$', views.seetask),   
    url(r'^paidRemove/(?P<id>\d+)$', views.paidRemove),   
    url(r'^addTask$', views.addingTask),   
    url(r'^donate$', views.seefund),   
    url(r'^addFund$', views.addingFund),   
    url(r'^disp/(?P<id>\d+)$', views.disp),   
    url(r'^accept/(?P<id>\d+)$', views.acceptTask),   

    # url(r'^addFav/(?P<id>\d+)$', views.addingFav),   
    # url(r'^disp/(?P<id>\d+)$', views.disp),   
        
    # url(r'^wish_items/create$', views.additem),     
    # url(r'^dispList/(?P<id>\d+)$', views.disp),   
    # url(r'^delete/(?P<id>\d+)$', views.delete),   
        
    # url(r'^(?P<id>\d+)$', views.show),
    # url(r'^new$', views.new),
    # url(r'^create$', views.create),
    # url(r'^(?P<id>\d+)/edit$', views.edit),
    # url(r'^(?P<id>\d+)/update$', views.update),
    # url(r'^(?P<id>\d+)/destroy$', views.destroy),
    # # url(r'^(?P[0-9]{4})$', views.show),
    # url(r'^(?P<num>[0-9]+)$', views.show),     

]

