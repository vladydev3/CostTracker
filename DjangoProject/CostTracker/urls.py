from django.urls import path, re_path
from .views import SubmitCostView, UploadFileView, GetCostsView, home, register
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Cost Tracker API",
      default_version='v1',
      description="API documentation for Cost Tracker",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('submit_cost/', SubmitCostView.as_view(), name='submit_cost'),
    path('upload_file/', UploadFileView.as_view(), name='upload_file'),
    path('get_costs/', GetCostsView.as_view(), name='get_costs'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]