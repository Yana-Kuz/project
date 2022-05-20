from django.urls import include, path
from first import views
from django.conf import settings
from django.contrib.auth import logout
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("lti",views.lti, name='lti'),
    # url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},name='logout'),
    url(r'^admin/', admin.site.urls),
    path("lti_python",views.lti_python, name = 'lti_python'),
    path("add",views.add_tool, name = 'add_tool'),
    path("all",views.all_tool, name = 'all_tools')
]
