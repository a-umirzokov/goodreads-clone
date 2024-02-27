# from django.urls import path
#
# from api.views import BookReviewAPIView, BookReviewListAPIView
from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet

app_name = 'api'

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')
urlpatterns = router.urls
# urlpatterns = [
#     path('reviews/<int:id>/', BookReviewAPIView.as_view(), name='review-detail'),
#     path('reviews/', BookReviewListAPIView.as_view(), name='review-list'),
# ]
