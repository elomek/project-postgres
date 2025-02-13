from rest_framework import serializers
from .models import Review, Division, Department, ProductClass

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class ProductClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClass
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()  # نمایش اطلاعات کامل Division
    department = DepartmentSerializer()
    product_class = ProductClassSerializer()

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'rating', 'date_time', 'division', 'department', 'product_class']

    



