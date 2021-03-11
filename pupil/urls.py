from django.conf.urls import url,include
from pupil import views



app_name = 'pupil'

urlpatterns = [

    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^new/$',views.NewVisual.as_view(), name = 'newvisual'),
    url(r'^history/',views.history.as_view(),name='history'),
    url(r'^visual/(?P<pk>[0-9]+)/delete/$',views.DeleteVisual.as_view(), name = 'deletevisual'),
    url(r'^visual/(?P<pk>[0-9]+)/convert/$',views.ConvertVisual.as_view(),name = 'convertvisual'),
    url(r'^download/',views.download.as_view(),name='download'),

]
