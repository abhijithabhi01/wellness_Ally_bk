
from django.urls import path
from .views import UserCreateView,LoginView,HealthIssuesListView,HealthProfileList
urlpatterns = [
 path('register/',UserCreateView.as_view(),name='register'),
 path('login/',LoginView.as_view(),name='login'),
 path('health_issue/list/',HealthIssuesListView.as_view(),name='issue-list'),
 path('health-profiles/<int:health_issue_id>/', HealthProfileList.as_view(), name='health-profile-list'),

]
