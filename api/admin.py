from django.contrib import admin

from api.models import appUser, MeditationSession, ExcerciseSession



class appUserAdmin(admin.ModelAdmin):
	fields = ['user', 'start_date', 'mediation_time', 'excercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at']

class MeditationSessionAdmin(admin.ModelAdmin):
	fields = ['meditation_id', 'user', 'percent_completed', 'created_at', 'updated_at']

class ExerciseSessionAdmin(admin.ModelAdmin):
	fields = ['Exercise_id', 'user', 'percent_completed', 'created_at', 'updated_at']


# Register your models here.
admin.site.register(appUser, appUserAdmin)
admin.site.register(MeditationSession, MeditationSessionAdmin)
admin.site.register(ExcerciseSession, ExerciseSessionAdmin)

