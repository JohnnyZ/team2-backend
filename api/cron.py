from datetime import date, datetime, time, timedelta
from random import randint

from django.contrib.auth.models import User
from django.utils import timezone

from .models import UserProfile, ExercisePush, AssessmentPush, ExerciseSession, Assessment
from .constants import END_HOUR, START_HOUR, MIN_ASSESSMENTS_PER_DAY, MAX_ASSESSMENTS_PER_DAY

import logging
logger = logging.getLogger(__name__)

def create_user(num, ex_dow, ex_time, med_time):
	user = User(
		username="test"+num, 
		email="test"+num+"@email.com", 
		first_name="first", 
		last_name="last")
	user.save()

	user_id = user.id

	profile = UserProfile(
		birthday="2015-03-30", 
		gender="0", 
		exercise_time=ex_time,
		exercise_day_of_week=ex_dow, # Sunday
		meditation_time=med_time)

	profile.user_id = user_id
	profile.save()

def createnewusers():
	create_user("7", 3, "13:00:00", "10:00:00")
	create_user("8", 3, "14:30:00", "10:00:00")
	create_user("9", 4, "22:00:00", "10:00:00")

def createExerciseSessions():
	session = ExerciseSession(exercise_id=1, created_at="2015-04-11T00:27:19.185783")
	session.user_id = 7
	session.save()

	push = ExercisePush(exercise_id=1, sent="2015-04-9T00:27:19.185783")
	push.user_id = 7
	push.save()




# Send push to given user and send them down the exercise that it will link to
# Save this into the ExercisePush table
def sendExercisePush(user, exercise_id):
	# TODO: send push
	device = APNSDevice.objects.get(registration_id=user.apns_device.apns_token)
	device.send_message("Time for this weeks exercise", extra={"exercise_id": exercise_id})

	exercise_push = ExercisePush(exercise_id=exercise_id)
	exercise_push.user_id = user.user.id
	exercise_push.save()

# Send push to given user and send down the assessment_id and if this is the morning/extended assessment
# Save this into the AsessementPush table - schedule the next push
def sendAssessmentPush(user, assessment_id, is_extended):
	# TODO: send push
	device = APNSDevice.objects.get(registration_id=user.apns_device.apns_token)
	device.send_message("Time for an assessment", extra={"assessment_id": exercise_id, "is_extended":is_extended})

	# Calculate the amount to incrememnt so it's within our range of desired number of assessments
	minutes_in_day = (END_HOUR - START_HOUR) * 60
	max_interval = minutes_in_day / (MIN_ASSESSMENTS_PER_DAY - 1)
	min_interval = minutes_in_day / (MAX_ASSESSMENTS_PER_DAY - 1)
	random_interval = randint(min_interval,max_interval)

	print("would set it to: ")
	print(datetime.now() + timedelta(minutes=random_interval)) # TODO put this into schedule

	assessment_push = AssessmentPush(next_send=datetime.now() + timedelta(minutes=15))
	assessment_push.user_id = user.user.id
	assessment_push.save()


def run_cron():
	all_users = UserProfile.objects.all()
	for user in all_users:

		user_id = user.user.id

		dow = datetime.today().weekday()
		now = datetime.now()
		aware_now = timezone.make_aware(now, timezone.get_default_timezone())
		now_time = now.time()
		now_date = now.date()
		last_possible_send_time = time(hour=END_HOUR)
		first_possible_send_time = time(hour=START_HOUR)

		# get the last exercise push for user (order by sent descending)
		exercise_sessions = ExerciseSession.objects.filter(user__id=user_id).order_by("-created_at")
		exercise_pushes = ExercisePush.objects.filter(user__id=user_id).order_by("-sent")

		# used for querying for assessments sent today
		today_min = datetime.combine(date.today(), time.min)
		today_max = datetime.combine(date.today(), time.max)
		# all assessments sent to this user today
		today_assessments = AssessmentPush.objects.filter(user__id=user_id, sent__range=(today_min, today_max)).order_by("-sent")

		# check if eligable for exercise lesson
		# it's the day of week they specified
		# and it's past the time they want to receive the push
		if user.exercise_day_of_week == dow and	user.exercise_time < now_time:		

		    # check to see if this is their first exercise
			if exercise_sessions.exists():
				last_exercise_session = exercise_sessions[0]
				last_exercise_push = exercise_pushes[0]
				last_exercise_push_date = last_exercise_push.sent.date()

				# if they've received a push today, don't send another
				if now_date > last_exercise_push_date:
					# send the exercise push with the execrcise id to push
					sendExercisePush(user=user, exercise_id=last_exercise_session.exercise_id + 1)

			# they're eligble for first exercise push and haven't received one before
			elif not exercise_pushes.exists():
				sendExercisePush(user=user, exercise_id=0)

		# if an assessment was sent today, see if they're eligable for another one
		elif today_assessments.exists():
			last_assessment = today_assessments[0]
			
			# it's past the time of our next send
			# and before the last send time
			if aware_now > last_assessment.next_send and now_time < last_possible_send_time:	
				# create assessment and push it down with the id and is_extended = false (since it's not the morning one)
				new_assessment = Assessment()
				new_assessment.user_id = user_id
				new_assessment.save()

				sendAssessmentPush(user=user, assessment_id=new_assessment.id, is_extended=False)

		# no assessment sent today - check if they're eligable for morning/extended assessment
		# TODO: this will send the morning one at the same time everyday (START_HOUR) - add variance?
		elif now_time > first_possible_send_time:
			# create assessment and push it down with the id and is_extended = true (since it is the morning one)
			new_assessment = Assessment()
			new_assessment.user_id = user_id
			new_assessment.save()

			sendAssessmentPush(user=user, assessment_id=new_assessment.id, is_extended=True)

