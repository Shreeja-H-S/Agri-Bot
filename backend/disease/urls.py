from django.urls import path
from .views import DiseasePredictView

urlpatterns = [
    path('predict/', DiseasePredictView.as_view(), name='disease-predict'),
]
