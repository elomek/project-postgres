from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from django.shortcuts import render






def home_page_view(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
def reviews_list(request):
    if request.method == 'GET': 
        queryset = Review.objects.all().order_by('-id')[:5]
        serializer = ReviewSerializer(queryset, many = True)   #many yani majmooei az reviws ha ast python -> json
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data =request.data)    # json -> python
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('everything is OK')




 
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request,id):
    #review = Review.objects.get(pk=id)
    review = get_object_or_404(Review, pk=id)
    
    if request.method == 'GET' :
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)