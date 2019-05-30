from django.urls import path, include

app_name = 'api'

urlpatterns = [
  path('v1/', include(('api.v1.urls', 'backend.api'), namespace='v1')),
]
