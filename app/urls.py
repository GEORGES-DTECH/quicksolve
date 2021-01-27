
from django.contrib import admin
from django.urls import path, include

from transactions.views import TransactionHomeView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('root/', admin.site.urls, name='manager'),
    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('', include('pwa.urls')),
    path('transactions/', include('transactions.urls')),
    path('registration', include('registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/',include(debug_toolbar.urls))
    ] + urlpatterns




