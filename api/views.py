from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User,HealthIssues,HealthCondition,HealthProfile,DietPlans,ExerciseVideos,SymptomTips,Category,Product
from .serializers import UserSerializer,HealthConditionSerializer,HealthIssuesSerializer,HealthProfileSerializer,DietPlansSerializer,ExerciseVideosSerializer,SymptomTipsSerializer,CategorySerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
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