from django.contrib import admin
from django.conf.urls import include,url
from django.views.generic import RedirectView
from django.conf import settings
# from pupil import views
from pupil import views
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login'), name='login-redirect'),
    url(r'^admin/', admin.site.urls),
    # url(r'^mask/',include('mask.urls')),
    url(r'^pupil/',include('pupil.urls')),
    # url(r'^register/$',views.UserFormView.as_view(),name='register'),
    url(r'^ht/', include('health_check.urls')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^register/$',views.RegisterPage.as_view(),name = 'register'),
    url(r'^login/$',views.LoginPage.as_view(),name = 'login')
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    