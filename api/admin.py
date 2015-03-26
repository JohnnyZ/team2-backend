from django.contrib import admin

from api.models import appUser, MeditationSession, ExerciseSession



class appUserAdmin(admin.ModelAdmin):
	
	list_display = ('user_id_display', 'user', 'start_date', 'mediation_time', 'exercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at')
	fields = ['user', 'start_date', 'mediation_time', 'exercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class MeditationSessionAdmin(admin.ModelAdmin):
	list_display = ('meditation_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['meditation_id', 'user', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ExerciseSessionAdmin(admin.ModelAdmin):
	list_display = ('exercise_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['exercise_id', 'user', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'


# Register your models here.
admin.site.register(appUser, appUserAdmin)
admin.site.register(MeditationSession, MeditationSessionAdmin)
admin.site.register(ExerciseSession, ExerciseSessionAdmin)

