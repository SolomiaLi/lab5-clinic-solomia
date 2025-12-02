from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Шлях до адмінки (якщо використовуєш)
    path('admin/', admin.site.urls),

    # 1. API (всі посилання починаються з api/)
    # Переконайся, що старий файл clinic/urls.py з API-класами існує
    path('api/', include('clinic.urls')),

    # 2. HTML Сайт (доступний по прямих посиланнях, наприклад /patients/)
    path('', include('clinic.html_urls')),
]