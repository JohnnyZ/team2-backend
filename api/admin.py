from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MeditationSession, ExerciseSession, Assessment, Response, MultiSelectResponse, ExerciseReminder, AssessmentPush, ExercisePush, MeditationPush

# Import Export
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin, ImportExportMixin

class ExerciseReminderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'notification_time', 'user_id_display', 'user')
	fields = ['user', 'notification_time']
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

class ExercisePushAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'exercise_id', 'user_id_display', 'user')
	fields = ['user', 'exercise_id']
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

class MeditationPushAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'user_id_display', 'user')
	fields = ['user']
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

class AssessmentPushAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ('id', 'assessment_id_display', 'next_send', 'is_momentary', 'user_id_display', 'user')
	fields = ['user', 'assessment', 'next_send', 'is_momentary']
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

	def assessment_id_display(self, obj):
		return obj.assessment_id
	assessment_id_display.short_description = 'Assessment ID'
	assessment_id_display.admin_order_field = 'assessment_id'

class MeditationSessionResource(resources.ModelResource):
	class Meta:
		model = MeditationSession

class MeditationSessionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'meditation_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['user', 'meditation_id', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']
	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

class ExerciseSessionResource(resources.ModelResource):
	class Meta:
		model = ExerciseSession

class ExerciseSessionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'exercise_id', 'user_id_display', 'user', 'created_at', 'updated_at')
	fields = ['user', 'exercise_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'


class AssessmentResource(resources.ModelResource):
	#user = Field(attribute='userprofile__user__username')
	class Meta:
		model = Assessment

class AssessmentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'user_id_display', 'user', 'start_time', 'complete_time', 'created_at', 'updated_at')
	fields = ['user', 'start_time', 'complete_time', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']
	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'
	user_id_display.admin_order_field = 'user_id'

	resource_class = AssessmentResource

class ResponseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'assessment_id_display', 'get_user', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at')
	fields = ['assessment', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['type', 'percent', 'question_id', 'emotion', 'assessment__user__username']

	def assessment_id_display(self, obj):
		return obj.assessment_id
	assessment_id_display.short_description = 'Assessment ID'
	assessment_id_display.admin_order_field = 'assessment_id'

	def get_user(self, obj):
		return obj.assessment.user.username
	get_user.short_description = 'User'
	get_user.admin_order_field = 'assessment__user__username'

	# Import_Export
	#resource_class = ResponseResource

class MultiSelectResponseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	list_display = ('id', 'response_id_display', 'response_question_id_display', 'selection_id')
	fields = ['response', 'selection_id']

	def response_id_display(self,obj):
		return obj.response_id
	response_id_display.short_description = 'Response ID'

	def response_question_id_display(self,obj):
		return obj.response.question_id
	response_question_id_display.short_description = 'Question ID'


class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserProfileAdmin(ImportExportActionModelAdmin, UserAdmin):
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
admin.site.register(ExerciseReminder, ExerciseReminderAdmin)
admin.site.register(ExercisePush, ExercisePushAdmin)
admin.site.register(AssessmentPush, AssessmentPushAdmin)
admin.site.register(MeditationPush, MeditationPushAdmin)

