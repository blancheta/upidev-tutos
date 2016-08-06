from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from hero_slider import urls as hero_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hero-slider/', include(hero_urls)),
    url(r'^$', TemplateView.as_view(template_name='demo/slider.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
