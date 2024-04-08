from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User,HealthIssues,HealthCondition,HealthProfile,DietPlans,ExerciseVideos,SymptomTips,Category,Product,Order,CommunityChat,PersonalChat
from .serializers import (UserSerializer,HealthConditionSerializer,HealthIssuesSerializer,HealthProfileSerializer,DietPlansSerializer
                          ,ExerciseVideosSerializer,SymptomTipsSerializer,CategorySerializer,ProductSerializer,
                          OrderSerializer,CommunityChatSerializer,PersonalChatSerializer,AppointmentSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from rest_framework import generics
# Create your views here.

class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"registration success","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

current_user = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)

        if user.check_password(password):
            

            refresh = RefreshToken.for_user(user)

            response_data = {
                'status': 1,
                'data': {
                    'token': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'user': {
                        'id': user.id,
                        'full_name': user.full_name,
                        'phone': user.phone,
                        'dob': user.dob,
                        'email': user.email,
                        'gender': user.gender,
                        'user_type': user.user_type,
                        'is_active': user.is_active
                    }
                }
            }

          
            return Response(response_data)

        return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)

class HealthIssuesListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            health_issues = HealthIssues.objects.all()
            serializer = HealthIssuesSerializer(health_issues, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class HealthProfileList(APIView):
    def get(self, request, health_issue_id, *args, **kwargs):
        try:
            health_profiles = HealthProfile.objects.filter(issue=health_issue_id)
            serializer = HealthProfileSerializer(health_profiles, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except HealthProfile.DoesNotExist:
            return Response({'error': 'HealthIssue not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DietPlanList(APIView):
    def get(self, request, health_profile_id, *args, **kwargs):
        try:
            dietplans = DietPlans.objects.filter(health_profile=health_profile_id)
            serializer = DietPlansSerializer(dietplans, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except DietPlans.DoesNotExist:
            return Response({'error': 'dietplan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ExerciseVideosList(APIView):
    def get(self, request, health_profile_id, *args, **kwargs):
        try:
            exercise_video = ExerciseVideos.objects.filter(health_profile=health_profile_id)
            serializer = ExerciseVideosSerializer(exercise_video, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except ExerciseVideos.DoesNotExist:
            return Response({'error': 'ExerciseVideos not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
class ExerciseVideosDetail(APIView):
    def get(self, request, exercise_video_id, *args, **kwargs):
        try:
            exercise_video = ExerciseVideos.objects.get(id=exercise_video_id)
            serializer = ExerciseVideosSerializer(exercise_video)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except ExerciseVideos.DoesNotExist:
            return Response({'error': 'ExerciseVideos not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       

class SymptomTipList(APIView):
    def get(self, request, health_profile_id, *args, **kwargs):
        try:
            symtomtip = SymptomTips.objects.filter(health_profile=health_profile_id)
            serializer = SymptomTipsSerializer(symtomtip, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except SymptomTips.DoesNotExist:
            return Response({'error': 'SymptomTips not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SymptomTipDetail(APIView):
    def get(self, request, symtomtip_id, *args, **kwargs):
        try:
            symtomtip = SymptomTips.objects.filter(health_profile=symtomtip_id)
            serializer = SymptomTipsSerializer(symtomtip)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except SymptomTips.DoesNotExist:
            return Response({'error': 'SymptomTips not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryList(APIView):
    def get(self, request, health_profile_id, *args, **kwargs):
        try:
            category = Category.objects.filter(health_profile=health_profile_id)
            serializer = CategorySerializer(category, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryProductsList(APIView):
    def get(self, request, category_id, *args, **kwargs):
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)

            serializer = ProductSerializer(products, many=True)

            response_data = {
                'category': category.name,
                'products': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductDetail(APIView):
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Assuming you have a 'product_id' and 'quantity' field in the request data
        product_id = request.data.get('product_id')
        order_quantity = 5
        address = request.data.get('address')

        try:
            # Retrieve the product based on the provided product_id
            product = Product.objects.get(id=product_id)

            # Check if the product quantity is greater than 0
            if product.qty > 0:
                # Check if the order quantity is less than or equal to the product quantity
                if order_quantity <= product.qty:
                    # Create the order serializer with product and request data
                    serializer = OrderSerializer(data={'product': product.id, 'quantity': order_quantity, 'total_price': product.price * order_quantity,'address':address, **request.data})

                    if serializer.is_valid():
                        # Save the order
                        order_instance = serializer.save(user=request.user)

                        # Update the product quantity and set is_out_of_stock to True if needed
                        product.qty -= order_quantity
                        if product.qty == 0:
                            product.is_out_of_stock = True
                        product.save()

                        return Response({"status": 1, "message": "Order created successfully"}, status=status.HTTP_201_CREATED)

                    return Response({"status": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status": 0, "message": "Order quantity exceeds product quantity"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": 0, "message": "Product quantity is not sufficient"}, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            return Response({"status": 0, "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 0, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class CommunityChatCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            serializer = CommunityChatSerializer(data=request.data)

            if serializer.is_valid():        
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CommunityChatListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            community_chats = CommunityChat.objects.all().order_by('-created_at')
            serializer = CommunityChatSerializer(community_chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PersonalChatCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            serializer = PersonalChatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender = request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PersonalChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            personal_chats = PersonalChat.objects.filter(sender=request.user).order_by('-created_at')
            serializer = PersonalChatSerializer(personal_chats, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentCreateView(APIView):
    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)