# from rest_framework import status
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from rest_framework.views import APIView
from books.models import BookReview
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.serializers import BookReviewSerializer
from rest_framework import viewsets


class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')
    lookup_field = 'id'

# class BookReviewAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(book_review)
#         return Response(data=serializer.data)
#
#     def delete(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         book_review.delete()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BookReviewListAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request):
#         reviews = BookReview.objects.all().order_by('-created_at')
#
#         paginator = PageNumberPagination()
#         page_obj = paginator.paginate_queryset(reviews, request)
#         serializer = BookReviewSerializer(page_obj, many=True)
#
#         return paginator.get_paginated_response(serializer.data)
#
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
