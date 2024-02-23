from rest_framework import serializers
from .models import User, Content, Category


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'pincode']
        extra_kwargs = {
            'password': {'write_only': True},
            # 'email': {'validators': []},  # Disable default email validation
        }
    def validate_password(self, value):
        # Add custom password validation
        # Example: Minimum 8 characters, 1 uppercase, 1 lowercase
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return value
    def create(self, validated_data):
        # Override create method to set password properly
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        validated_data.pop('password')
        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'document', 'categories', 'author', 'created_at', 'updated_at']
    def validate_document(self, value):
        # Custom validation to check if the uploaded file is a PDF
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("File must be in PDF format.")
        return value
