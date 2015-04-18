from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MeditationSession, ExerciseSession, Assessment, Response, MultiSelectResponse

class MeditationSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'meditation_id', 'user_id_display', 'user', 'percent_completed', 'created_at', 'updated_at')
	fields = ['user', 'meditation_id', 'percent_completed', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']
	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ExerciseSessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'exercise_id', 'user_id_display', 'user', 'created_at', 'updated_at')
	fields = ['user', 'exercise_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']

	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'


class AssessmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_id_display', 'user', 'start_time', 'complete_time', 'created_at', 'updated_at')
	fields = ['user', 'start_time', 'complete_time', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['user__username']
	def user_id_display(self, obj):
		return obj.user_id
	user_id_display.short_description = 'User ID'

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('id', 'assessment_id_display', 'get_user', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at')
	fields = ['assessment', 'type', 'boolean', 'number', 'emotion', 'percent', 'question_id', 'created_at', 'updated_at']
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ['type', 'percent', 'question_id', 'emotion', 'assessment__user__username']

	def assessment_id_display(self, obj):
		return obj.assessment_id
	assessment_id_display.short_description = 'Assessment ID'

	def get_user(self, obj):

		return obj.assessment.user.username 
	get_user.short_description = 'User'

class MultiSelectResponseAdmin(admin.ModelAdmin):
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


# from django.contrib.auth import get_user_model
# from django.utils.translation import ugettext_lazy as _
# from push_notifications.models import APNSDevice, GCMDevice, get_expired_tokens

# User = get_user_model()
# class DeviceAdmin(admin.ModelAdmin):
# 	list_display = ("__unicode__", "device_id", "user", "active", "date_created")
# 	search_fields = ("name", "device_id", "user__%s" % (User.USERNAME_FIELD))
# 	list_filter = ("active", )
# 	actions = ("send_message", "send_bulk_message", "prune_devices", "enable", "disable")

# 	def send_message(self, request, queryset):
# 		ret = []
# 		errors = []
# 		r = ""
# 		for device in queryset:
# 			try:
# 				r = device.send_message("Test single notification")
# 			except Exception as e:
# 				errors.append(str(e))
# 			if r:
# 				ret.append(r)
# 		if errors:
# 			self.message_user(request, _("Some messages could not be processed: %r" % ("\n".join(errors))))
# 		if ret:
# 			self.message_user(request, _("All messages were sent: %s" % ("\n".join(ret))))
# 	send_message.short_description = _("Send test message")

# 	def send_bulk_message(self, request, queryset):
# 		r = queryset.send_message("Test bulk notification")
# 		self.message_user(request, _("All messages were sent: %s" % (r)))
# 	send_bulk_message.short_description = _("Send test message in bulk")

# 	def enable(self, request, queryset):
# 		queryset.update(active=True)
# 	enable.short_description = _("Enable selected devices")

# 	def disable(self, request, queryset):
# 		queryset.update(active=False)
# 	disable.short_description = _("Disable selected devices")

# 	def prune_devices(self, request, queryset):
# 		# Note that when get_expired_tokens() is called, Apple's
# 		# feedback service resets, so, calling it again won't return
# 		# the device again (unless a message is sent to it again).  So,
# 		# if the user doesn't select all the devices for pruning, we
# 		# could very easily leave an expired device as active.  Maybe
# 		#  this is just a bad API.
# 		expired = get_expired_tokens()
# 		devices = queryset.filter(registration_id__in=expired)
# 		for d in devices:
# 			d.active = False
# 			d.save()


# admin.site.register(APNSDevice, DeviceAdmin)
# admin.site.register(GCMDevice, DeviceAdmin)


## Register models ##

# Add UserProfile to user 
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(MeditationSession, MeditationSessionAdmin)
admin.site.register(ExerciseSession, ExerciseSessionAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(MultiSelectResponse, MultiSelectResponseAdmin)

