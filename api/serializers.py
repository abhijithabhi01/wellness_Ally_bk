
from rest_framework import serializers
from .models import User,HealthCondition,HealthIssues,HealthProfile,DietPlans,SymptomTips,ExerciseVideos,Category,Product

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'password', 'dob', 'email', 'gender', 'user_type', 'is_active','is_staff')
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)  # Use set_password to handle password hashing

        instance.save()
        return instance    
    

class HealthConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCondition
        fields = ['id', 'name', 'description']

class HealthIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIssues
        fields = ['id', 'issue', 'description', 'image']

class HealthProfileSerializer(serializers.ModelSerializer):
    condition = HealthConditionSerializer()
    issue = HealthIssuesSerializer()

    class Meta:
        model = HealthProfile
        fields = ['id', 'condition', 'issue', 'description']


class DietPlansSerializer(serializers.ModelSerializer):
    health_profile = HealthProfileSerializer()

    class Meta:
        model = DietPlans
        fields = '__all__'

class ExerciseVideosSerializer(serializers.ModelSerializer):
    health_profile = HealthProfileSerializer()

    class Meta:
        model = ExerciseVideos
        fields = '__all__'

class SymptomTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomTips
        fields = '__all__'        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'        

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ['category', 'category_name', 'name', 'description', 'image', 'price']        