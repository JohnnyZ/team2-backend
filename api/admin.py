from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MeditationSession, ExerciseSession, Assessment, Response, MultiSelectResponse

class MeditationSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'meditation_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['user', 'meditation_id', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ExerciseSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'exercise_id', 'user_id_display', 'user', 'created_at', 'updated_at')
	fields = ['user', 'exercise_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'


class AssessmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_id_display', 'user', 'start_time', 'complete_time', 'created_at', 'updated_at')
	fields = ['user', 'start_time', 'complete_time', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user']
	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('id', 'assessment_id_display', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at')
	fields = ['assessment', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['type', 'percent', 'question_id', 'emotion']

	def assessment_id_display(self, obj):
		return obj.assessment_id
	assessment_id_display.short_description = 'Assessment ID'

class MultiSelectResponseAdmin(admin.ModelAdmin):
	list_display = ('id', 'response_id_display', 'response', 'selection_id')
	fields = ['response', 'selection_id']

	def response_id_display(self,obj):
		return obj.response_id
	response_id_display.short_description = 'Response ID'


class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserProfileAdmin(UserAdmin):
	inlines = [ UserProfileInline, ]
	list_display = ('id', 'username', 'first_name', 'last_name', 'start_date', 'meditation_time', 'exercise_day_of_week', 
					'exercise_time', 'created_at', 'updated_at', )
	readonly_fields = ('created_at', 'updated_at')

	def start_date(self, obj):
		try:
			start_date = obj.profile.start_date
			return start_date
		except:
			return ""
	start_date.short_description = 'Start Date'

	def meditation_time(self, obj):
		try:
			meditation_time = obj.profile.meditation_time
			return meditation_time
		except:
			return ""
	meditation_time.short_description = 'Med Time'

	def exercise_day_of_week(self, obj):
		try:
			exercise_day_of_week = obj.profile.exercise_day_of_week
			return exercise_day_of_week
		except:
			return ""
	exercise_day_of_week.short_description = 'Exercise Day'

	def exercise_time(self, obj):
		try:
			exercise_time = obj.profile.exercise_time
			return exercise_time
		except:
			return ""
	exercise_time.short_description = 'Exercise Time'

	def created_at(self, obj):
		try:
			created_at = obj.profile.created_at
			return created_at
		except:
			return ""
	created_at.short_description = 'Created at'

	def updated_at(self, obj):
		try:
			updated_at = obj.profile.updated_at
			return updated_at
		except:
			return ""
	updated_at.short_description = 'Updated at'


## Register models ##

# Add UserProfile to user 
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(MeditationSession, MeditationSessionAdmin)
admin.site.register(ExerciseSession, ExerciseSessionAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(MultiSelectResponse, MultiSelectResponseAdmin)

