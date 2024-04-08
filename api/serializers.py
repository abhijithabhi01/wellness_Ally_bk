
from rest_framework import serializers
from .models import User,HealthCondition,HealthIssues,HealthProfile,DietPlans,SymptomTips,ExerciseVideos,Category,Product,CommunityChat,PersonalChat,Appointment,Order

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
        fields = ['id', 'condition', 'issue', 'description','image']

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
        fields = ["id",'category', 'category_name', 'name', 'description', 'image', 'price']        

class CommunityChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityChat
        fields = ['id', 'user', 'message', 'created_at']        

class PersonalChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer()  # Use the UserSerializer to represent the sender
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = PersonalChat
        fields = ['id', 'sender', 'message', 'replay', 'created_at']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer()  # Use the UserSerializer to represent the patient
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_time', 'title', 'created_at', 'payed']

    def validate_appointment_time(self, value):
        conflicting_appointments = Appointment.objects.filter(
            appointment_time=value
        ).exclude(pk=self.instance.pk if self.instance else None)

        if conflicting_appointments.exists():
            raise serializers.ValidationError("Appointment time slot is not available.")

        return value        
    
class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'updated_at', 'total_price', 'product','address','quantity',] 

class CommunityChatSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = CommunityChat
        fields = ['id', 'user', 'user_data', 'message', 'created_at']
        read_only_fields = ['user'] 

    def get_user_data(self, obj):
        # Here you can define what additional user data you want to include
        user = obj.user
        user_data = {
            'id': user.id,
            'full_name': user.full_name,
            # Add more fields as needed
        }
        return user_data

class PersonalChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalChat
        fields = ['id', 'sender', 'message', 'replay', 'created_at']
        read_only_fields = ['sender']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender'] = instance.sender.full_name  
        return representation

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_time', 'title', 'created_at', 'paid']
        read_only_fields = ['created_at']

    def validate(self, data):
        appointment_time = data.get('appointment_time')
        # Check if there is any appointment at the same time
        conflicting_appointments = Appointment.objects.filter(appointment_time=appointment_time)
        if self.instance:
            conflicting_appointments = conflicting_appointments.exclude(pk=self.instance.pk)
        if conflicting_appointments.exists():
            raise serializers.ValidationError("Appointment time slot is not available.")
        return data
