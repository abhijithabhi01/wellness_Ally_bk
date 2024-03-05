from django.contrib import admin
from .models import User,HealthIssues,HealthCondition,HealthProfile,ExerciseVideos,DietPlans,Category,Product,SymptomTips
# Register your models here.
admin.site.register(User)
admin.site.register(HealthProfile)
admin.site.register(HealthCondition)
admin.site.register(HealthIssues)
admin.site.register(ExerciseVideos)
admin.site.register(DietPlans)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SymptomTips)