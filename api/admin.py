from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from api.models import appUser, MeditationSession, ExerciseSession

"""
class appUserAdmin(admin.ModelAdmin):
	list_display = ('user_id_display', 'user', 'start_date', 'mediation_time', 'exercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at')
	fields = ['user', 'start_date', 'mediation_time', 'exercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
"""

class MeditationSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'meditation_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['meditation_id', 'user', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ExerciseSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'exercise_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['exercise_id', 'user', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'


class appUserInline(admin.StackedInline):
    model = appUser

class appUserAdmin(UserAdmin):
    inlines = [ appUserInline, ]
    list_display = ('start_date', 'mediation_time', 'exercise_day_of_week',
			'exercise_time', 'created_at', 'updated_at')

## Register models ##

#admin.site.register(appUser, appUserAdmin)
# Add appUser to user 
admin.site.unregister(User)
admin.site.register(User, appUserAdmin)
admin.site.register(MeditationSession, MeditationSessionAdmin)
admin.site.register(ExerciseSession, ExerciseSessionAdmin)

