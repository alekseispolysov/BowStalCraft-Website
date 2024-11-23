from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import DetailView

from itertools import chain

from . models import *
from . forms import *
from . owner import *
from . filters import *

# This view file contains functionality for all our forum app

# protect delete and update views
class ForumIndexPage(generic.ListView):
	template_name = 'forum/forum_index.html'
	paginate_by = 20
	model = ForumPost
	def get_queryset(self):
		posts = ForumPost.objects.all()
		# filter all usernames
		queryset = super(ForumIndexPage, self).get_queryset()

		self.myFilter = ForumFilter(self.request.GET, queryset=posts)
		queryset = self.myFilter.qs 
		#  [::-1] = to reverse the queryset
		return queryset[::-1]

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['myFilter'] = self.myFilter
		ctx['importantObjects'] = ForumPost.objects.all().filter(topic__icontains="Important")
		return ctx


# creating the new post
class CreateForumPost(LoginRequiredMixin, CreateView):
	template_name = 'forum/forum_create_post.html'
	model = ForumPost
	form_class = ForumPostForm
	success_url = reverse_lazy('forum:forum-index-page')

	def form_valid(self, form):
		form.instance.user = self.request.user
		# you can define in witch order you calling the super method
		return super().form_valid(form)

# updating the new post
class UpdateForumPost(OwnerUpdateView):
	template_name = 'forum/forum_update_post.html'
	model = ForumPost
	form_class = ForumPostForm
	success_url = reverse_lazy('forum:forum-index-page')

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs) # run data from generic view first, then append here something else
		# going into super class
		return ctx

# deleting post
class DeleteForumPost(OwnerDeleteView):
	template_name = 'forum/forum_delete_post.html'
	model = ForumPost
	success_url = reverse_lazy('forum:forum-index-page')

# detail view of the post
class DetailForumPage(View):
	def getqueryrelation(self, request, post):
		# function that is taking everything that repeating in it. It is checking if user has a query relation with post. If he liked or disliked that post
		# also it checks, if user is authenticated
		if request.user.is_authenticated:
			query_relation = Reputation_post.objects.filter(user=request.user).filter(post=post).first()
			if query_relation is None:
				relation_value = 0
			else:
				relation_value = query_relation.reputation
		else:
			relation_value = None

		return relation_value

	def get(self, request, pk):

		post = get_object_or_404(ForumPost, id=pk)
		comments = CommentToPost.objects.all().filter(post_id=pk)
		form = CommentToPostForm
		ctx = {
		'post':post,
		'form':form,
		'comments':comments,
		'relation_value': self.getqueryrelation(request, post),
		}

		return render(request, 'forum/forum_detail_post.html', ctx)
	# creating comment functionality
	def post(self, request, pk):
		if request.user.is_authenticated:
			form = CommentToPostForm(request.POST)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.user = request.user
				obj.post = get_object_or_404(ForumPost, pk=pk)
				obj.save()
				return redirect('forum:forum-detail-page', pk)
			else:
				return render(request, 'forum/forum_detail_post.html', ctx)
		else:
			ctx = {
			'post':post,
			'form':form,
			'comments':comments,
			'relation_value': self.getqueryrelation(request),
			}
			return render(request, 'forum/forum_detail_post.html', ctx)

# Ajax is here, because we need to set reputation for each post dynamicly
# the logic for reputation holded by ajax
class DetailForumPostPageAjax(LoginRequiredMixin, View):
	def post(self, request, pk):
		# here I need to check if user is already has opinion with post_reputation

		cur_user = User.objects.get(pk=request.POST["user_id"])
		post = ForumPost.objects.get(pk=request.POST["post_id"])
		user_action = request.POST["user_action"]
		# after when I got everything, I need to check if the user_profile has relation with ForumPostObject, called opinion_posts

		if user_action == 'dislike':
			reputation_temp = 1
		else:
			reputation_temp = -1
		query_relation = Reputation_post.objects.filter(user=cur_user).filter(post=post).first()
		counter = 0

		# check functionality for like and dislike buttons. Logic here are ment to check if user clicked same button two times and other scenarios

		if query_relation == None:
			if user_action == 'like':
				reputation_temp = 1
			elif user_action == 'dislike':
				reputation_temp = -1
			else:
				reputation_temp = 0
			new_relation = Reputation_post(user=cur_user, post=post, reputation=reputation_temp)
			post.people_voted += 1
			
			post.post_reputation += new_relation.reputation
			post.save()
			new_relation.save()
			query_relation = new_relation
		else:
			# so if reputation is greater then 0 we will check if
			if query_relation.reputation > 0:
				# it is like pressed, if so, undo the reputation and lover the people, that have been before
				if user_action == 'like':
					query_relation.reputation += -1
					counter = -1
					post.people_voted += -1
				# if it is dislike, we dont undo the people, but we changing the reputation
				elif user_action == 'dislike':
					query_relation.reputation += -2
					counter = -2
				else:
				# else we do nothing
					pass
			# else if the reputation is negative (means the dislike have been pressed before)
			elif query_relation.reputation < 0:
				# we will check, if it is a like, if so we won't change the count of people, inseted change reputation
				if user_action == 'like':
					query_relation.reputation += 2
					counter += 2
				# if dislike have been pressed the second time, we will undo dislike and lower the people
				elif user_action == 'dislike':
					query_relation.reputation += 1
					post.people_voted += -1
					counter +=1
				# else we do nothing
				else:
					pass
			# if the relation exist and it is 0 and something have been pressed we will change reputation and do nothing with people, because they are counted up
			else:
				if user_action == 'like':
					query_relation.reputation = 1
					counter += 1
					post.people_voted += 1
				elif user_action == 'dislike':
					query_relation.reputation = -1
					post.people_voted += 1
					counter -= 1
				else:
					pass			
			post.post_reputation += counter
			post.save()
			query_relation.save()
		

		# Create json object, that we sending back

		# I need to send something to dermine, which button should I show

		data = {
		"people_voted": post.people_voted,
		"reputation" : post.post_reputation,
		# send the value of query_relation.reputation
		"current_relation_reputation": query_relation.reputation
		}
		return JsonResponse(data)


# new advanced search
class fullSearch(View):
	# generate page with get method
	def get(self, request):
		return render(request, 'forum/fullsearch.html')

	def post(self, request):

		# getting everything from POST dictionary
		iD = request.POST['iD']
		name = request.POST['name']
		author = request.POST['author']
		topic = request.POST['topic']
		tags = request.POST['tags']

		# logic for parsing tags by comma

		tags_individual = tags.split(',')

		tags_url = ''
		for i in range(len(tags_individual)):
			tags_url += f'&tags={tags_individual[i]}'


		rating = request.POST['rating']
		lessrating = request.POST['lessrating']
		greatrating = request.POST['greatrating']


		contains = request.POST['contains']
		date_after = request.POST['date_after']
		date_before = request.POST['date_before']

		# construct url
		url = f'/forum/?id={iD}&name={name}&user__username={author}&topic={topic}{tags_url}&greatrating={greatrating}&rating={rating}&lessrating={lessrating}&text={contains}&start_date={date_after}&end_date={date_before}'
		# redirect
		return redirect(url)

		pass

# delete, edit comment functionality
# people protection functionality

class EditCommentToPost(OwnerUpdateView):
	template_name = 'forum/comment_edit_page.html'
	model = CommentToPost
	form_class = CommentToPostForm
	success_url = reverse_lazy('forum:forum-index-page')

class DeleteCommentToPost(OwnerDeleteView):
	template_name = 'forum/comment_delete_page.html'
	model = CommentToPost
	success_url = reverse_lazy('forum:forum-index-page')




