from django.urls import path
from .views import submit_cost, upload_file, get_costs

urlpatterns = [
    path('submit_cost/', submit_cost, name='submit_cost'),
    path('upload_file/', upload_file, name='upload_file'),
    path('get_costs/', get_costs, name='get_costs'),
]