from datetime import date, datetime, time, timedelta
from random import randint

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.management.base import BaseCommand

from push_notifications.models import APNSDevice

from api.models import UserProfile, ExercisePush, AssessmentPush, ExerciseSession, Assessment, MeditationPush
from api.constants import END_HOUR, START_HOUR, MIN_ASSESSMENTS_PER_DAY, MAX_ASSESSMENTS_PER_DAY

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):

	@staticmethod
	def sendPush(msg):
		device = APNSDevice.objects.get(registration_id='a08423188a75a26d3bde67d9a7cfd7cf6b6370e9033d7dc829e2b0d5d1087950')
		device.send_message(msg)

	# Send push to given user and send them down the exercise that it will link to
	# Save this into the ExercisePush table
	@staticmethod
	def sendMeditationPush(user):
		device = APNSDevice.objects.get(registration_id=user.apns_device.registration_id)
		device.send_message("Time to Meditate", extra={})

		med_push = MeditationPush()
		med_push.user_id = user.user.id
		med_push.save()

	# Send push to given user and send them down the exercise that it will link to
	# Save this into the ExercisePush table
	@staticmethod
	def sendExercisePush(user, exercise_id):
		device = APNSDevice.objects.get(registration_id=user.apns_device.registration_id)
		device.send_message("Time for this weeks exercise", extra={"exercise_id": exercise_id})

		exercise_push = ExercisePush(exercise_id=exercise_id)
		exercise_push.user_id = user.user.id
		exercise_push.save()

	# Send push to given user and send down the assessment_id and if this is the morning/extended assessment
	# Save this into the AsessementPush table - schedule the next push
	@staticmethod
	def sendAssessmentPush(user, assessment_id, is_momentary):
		device = APNSDevice.objects.get(registration_id=user.apns_device.registration_id)
		device.send_message("Time for an assessment", extra={"assessment_id": assessment_id, "is_momentary":is_momentary})

		# Calculate the amount to incrememnt so it's within our range of desired number of assessments
		minutes_in_day = (END_HOUR - START_HOUR) * 60
		max_interval = minutes_in_day / (MIN_ASSESSMENTS_PER_DAY - 1)
		min_interval = minutes_in_day / (MAX_ASSESSMENTS_PER_DAY - 1)
		random_interval = randint(min_interval,max_interval)

		print("would set it to: ")
		print(datetime.now() + timedelta(minutes=random_interval)) # TODO put this into schedule

		assessment_push = AssessmentPush(next_send=datetime.now() + timedelta(minutes=random_interval))#datetime.now() + timedelta(minutes=15))
		assessment_push.user_id = user.user.id
		assessment_push.assessment_id = assessment_id
		assessment_push.is_momentary = is_momentary
		assessment_push.save()

	@staticmethod	
	def run_cron():
		for user in UserProfile.objects.exclude(apns_device=None):

			user_id = user.user.id

			dow = datetime.today().weekday()
			now = datetime.now()
			aware_now = timezone.make_aware(now, timezone.get_default_timezone())
			now_time = now.time()
			now_date = now.date()
			last_possible_send_time = time(hour=END_HOUR)
			first_possible_send_time = time(hour=START_HOUR)

			# used for querying for assessments sent today
			today_min = datetime.combine(date.today(), time.min)
			today_max = datetime.combine(date.today(), time.max)

			# last meditation push
			# meditation_pushes = MeditationPush.objects.filter(user__id=user_id).order_by("-sent")
			today_meditations = MeditationPush.objects.filter(user__id=user_id, sent__range=(today_min, today_max)).order_by("-sent")

			# get the last exercise push for user (order by sent descending)
			exercise_sessions = ExerciseSession.objects.filter(user__id=user_id).order_by("-created_at")
			exercise_pushes = ExercisePush.objects.filter(user__id=user_id).order_by("-sent")

			# all assessments sent to this user today
			today_assessments = AssessmentPush.objects.filter(user__id=user_id, sent__range=(today_min, today_max)).order_by("-sent")

			# check if eligable for exercise lesson
			# it's the day of week they specified
			# and it's past the time they want to receive the push
			if user.exercise_day_of_week == dow and	user.exercise_time < now_time:		

			    # check to see if this is their first exercise
				if exercise_sessions.exists():
					last_exercise_session = exercise_sessions[0]
					# if a push was sent in the past 1) make sure one wasn't sent today and 2) send push with last_push_exercise+1
					if exercise_pushes.exists():
						last_exercise_push = exercise_pushes[0]
						last_exercise_push_date = last_exercise_push.sent.date()

						# if they've received a push today, don't send another
						if now_date > last_exercise_push_date:
							# send the exercise push with the execrcise id to push
							Command.sendExercisePush(user=user, exercise_id=last_exercise_push.exercise_id + 1)
					# if no push has been sent, base the exercise off the last completed exercise session
					else:
						Command.sendExercisePush(user=user, exercise_id=last_exercise_session.exercise_id + 1)

				# they're eligble for first exercise push and haven't received one before
				elif not exercise_pushes.exists():
					Command.sendExercisePush(user=user, exercise_id=0)

			if not today_meditations.exists() and exercise_pushes.exists() and now_time > user.meditation_time:
				Command.sendMeditationPush(user=user)

			# if an assessment was sent today, see if they're eligable for another one
			if today_assessments.exists():
				last_assessment = today_assessments[0]
				
				# it's past the time of our next send
				# and before the last send time
				if aware_now > last_assessment.next_send and now_time < last_possible_send_time:	
					# create assessment and push it down with the id and is_momentary = true (since it's not the morning one)
					new_assessment = Assessment()
					new_assessment.user_id = user_id
					new_assessment.save()

					Command.sendAssessmentPush(user=user, assessment_id=new_assessment.id, is_momentary=True)

			# no assessment sent today - check if they're eligable for morning/extended assessment
			# TODO: this will send the morning one at the same time everyday (START_HOUR) - add variance?
			elif now_time > first_possible_send_time:
				# create assessment and push it down with the id and is_momentary = false (since it is the morning one)
				new_assessment = Assessment()
				new_assessment.user_id = user_id
				new_assessment.save()

				Command.sendAssessmentPush(user=user, assessment_id=new_assessment.id, is_momentary=False)



	def handle(self, *args, **options):
		#do action
		# self.sendPush("sup")
		self.run_cron()


