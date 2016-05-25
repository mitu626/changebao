from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','ebuy.views.index'),
    url(r'^register/$','ebuy.views.register'),
    url(r'^login/$','ebuy.views.login'),
    url(r'^user/index/$','ebuy.views.userIndex',name="userIndex"),
    url(r'^createItemIndex/$','ebuy.views.createItem'),
    url(r'^itemIndex/$','ebuy.views.itemIndex'),
    url(r'^secretIndex/$','ebuy.views.secretIndex'),
    url(r"^searchIndex/$",'ebuy.views.searchIndex'),
    url(r"^search/$",'ebuy.views.search'),
    url(r"commentCreate/$",'ebuy.views.commentCreate'),
    url(r'^readme/$','ebuy.views.readme'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^(?P<name>\D+)/$','ebuy.views.temp')
    # Examples:
    # url(r'^$', 'changebao.views.home', name='home'),
    # url(r'^changebao/', include('changebao.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)+static("/media/",document_root=settings.MEDIA_ROOT)
