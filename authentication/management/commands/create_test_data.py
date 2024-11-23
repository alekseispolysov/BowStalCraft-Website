from django.core.management.base import BaseCommand
from authentication.models import User_Profile, Reputation_user
from mainapp.models import Post, CommentToPost, ContactEmail, SecurityEmailMessage
from forum.models import ForumPost, CommentToPost, Reputation_post
from django.contrib.auth.models import User
from django.conf import settings
from faker import Faker
import random
import os
import lorem
from datetime import date

posts_folder_path = os.path.join(settings.MEDIA_ROOT, 'user_default_images/Posts')
users_folder_path = os.path.join(settings.MEDIA_ROOT, 'user_default_images/Users')
post_images = os.listdir(posts_folder_path)
user_images = os.listdir(users_folder_path)

# ## Run command python manage.py create_test_data.py

# Variables
GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),	
		)
CATEGORY = (
		('Suggestions', 'Suggestions'),
		('Help', 'Help'),
		('Question','Question'),
		('Discussion', 'Discussion'),
		('Other', 'Other'),
	)

# Generating entire test database for testing purposes
class Command(BaseCommand):
	help = "Generate test data for the database"

	# when command is executed, this function is called
	def handle(self, *args, **kwargs):
		fake = Faker()
		today = date.today()
		# creating 10 users, 1 posts for each user and 1 comment for each user under his post
		for i in range(10):

			# choose random image
			random_user_image = random.choice(user_images)
			final_path = str(os.path.join("user_default_images/Users", random_user_image))

			# create user
			user = User.objects.create_user(
				username=fake.user_name(),
				email=fake.email(),
				first_name=fake.first_name(),
    			last_name=fake.last_name(),
				password="password123",
				)


			user.set_password("password123")
			# edit user profile (it is already created throw signals functionality)
			us_profile = user.user_profile
			us_profile.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
			us_profile.gender = random.choice([g[0] for g in GENDER])
			us_profile.profile_picture = final_path
			us_profile.reputation = random.randint(1, 500)
			us_profile.save()	
			user.save()

			# choose random image
			random_posts_image = random.choice(post_images)
			final_path = str(os.path.join("/media/user_default_images/Posts", random_posts_image))

			# create forum post object
			forum_post = ForumPost.objects.create(
				user=user,
				name=lorem.sentence(),
				topic=random.choice([c[0] for c in CATEGORY]),
				tags="RandomTagSimple",
				content=f"<img src={final_path}><br />{lorem.text()}",
				date_created=today,
				post_reputation=random.randint(1, 500),
				people_voted=0
				)

			# create comment to resent created post
			comment_to_post = CommentToPost.objects.create(
				user=user,
				post=forum_post,
				text=lorem.sentence(),
				date_created=today
				)

			# success message
			self.stdout.write(f"Successefuly created user, post and comment, iteration {i+1}: {user.username}, {user.user_profile.date_of_birth}, {user.user_profile.gender}, {user.user_profile.profile_picture}, {user.user_profile.reputation}")
		# creating super user and one post for him with topic important
		random_user_image = random.choice(user_images)
		final_path = str(os.path.join("user_default_images/Users", random_user_image))
		super_user = User.objects.create_superuser(
			username=fake.user_name(),
			email=fake.email(),
			first_name=fake.first_name(),
    		last_name=fake.last_name(),
			password="password123",
			)
		super_user.set_password("password123")

		# edit user profile (it is already created throw signals functionality)
		us_profile = super_user.user_profile
		us_profile.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
		us_profile.gender = random.choice([g[0] for g in GENDER])
		us_profile.profile_picture = final_path
		us_profile.reputation = random.randint(1, 500)
		us_profile.save()	
		super_user.save()

		# choose random image
		random_posts_image = random.choice(post_images)
		final_path = str(os.path.join("/media/user_default_images/Posts", random_posts_image))

		# create forum post object
		forum_post = ForumPost.objects.create(
			user=super_user,
			name="THIS IS ADMIN POST!",
			topic='Important',
			tags="ADMINPOST",
			content=f"<img src={final_path}><br />{lorem.text()}",
			date_created=today,
			post_reputation=random.randint(1000, 10000),
			people_voted=0
			)

		self.stdout.write(f"Successefuly created super user and forum post for him: {super_user.username}, {super_user.user_profile.date_of_birth}, {super_user.user_profile.gender}, {super_user.user_profile.profile_picture}, {super_user.user_profile.reputation}")

		# create 3 news
		for i in range(3):
			# choose image
			random_news_image = random.choice(post_images)
			final_path = str(os.path.join("user_default_images/Posts", random_news_image))
			
			# create news object
			newy = Post.objects.create(
				name="News: " + str(i+1),
				text=lorem.text(),
				date_created=today,
				preview_text="Basical preview text so you can deside, if you want read it or not",
				preview_picture=final_path,
				)

			# success message
			self.stdout.write(f"Successefuly news created, iteration {i+1}: {newy.name}, {newy.text[:10]}, {newy.date_created}, {newy.preview_text[:20]}, {newy.preview_picture}")



