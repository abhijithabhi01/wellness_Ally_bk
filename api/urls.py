
from django.urls import path
from .views import (UserCreateView,LoginView,HealthIssuesListView,HealthProfileList,
                    DietPlanList,ExerciseVideosList,ExerciseVideosDetail,SymptomTipList,SymptomTipDetail,
                    CategoryList,CategoryProductsList,ProductDetail,OrderCreateView,OrderDetail,CommunityChatCreateView,
                    CommunityChatListView,PersonalChatCreateAPIView,PersonalChatListView,AppointmentCreateView)
urlpatterns = [
 path('register/',UserCreateView.as_view(),name='register'),
 path('login/',LoginView.as_view(),name='login'),
 path('health_issue/list/',HealthIssuesListView.as_view(),name='issue-list'),
 path('health-profiles/<int:health_issue_id>/', HealthProfileList.as_view(), name='health-profile-list'),
 path('diet-plan/<int:health_profile_id>/', DietPlanList.as_view(), name='diet-plan-detail'),
 path('exercise-videos/<int:health_profile_id>/', ExerciseVideosList.as_view(), name='exercise-videos-list'),
 path('exercise-videos/detail/<int:exercise_video_id>/', ExerciseVideosDetail.as_view(), name='exercise-videos-detail'),
 path('symptom-tips/<int:health_profile_id>/', SymptomTipList.as_view(), name='symptom-tip-list'),
 path('symptom-tips/detail/<int:symtomtip_id>/', SymptomTipDetail.as_view(), name='symptom-tip-detail'),
 path('category/<int:health_profile_id>/', CategoryList.as_view(), name='category-list'),
 path('categories/<int:category_id>/products/', CategoryProductsList.as_view(), name='category-products-list'),
 path('products/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),

 path('order/create/',OrderCreateView.as_view(),name='order-create'),
 path('order/<int:order_id>/',OrderDetail.as_view(),name='order-detail'),

 path('community-chat/create/',CommunityChatCreateView.as_view(),name='cummunity chat'),
 path('community-chat/list/',CommunityChatListView.as_view(),name='cummunity-list'),
 path('personal-chat/create/',PersonalChatCreateAPIView.as_view(),name='personal-chat'),
 path('personal-chat/list/',PersonalChatListView.as_view(),name='list-personal-chat'),
 path('appointment/create/',AppointmentCreateView.as_view(),name='appoinment')


]