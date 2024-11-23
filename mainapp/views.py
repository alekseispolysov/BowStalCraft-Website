from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import generic
from django.views import View
from django.http import Http404

from . models import *
from . forms import *
from . filters import *

# This file contains all logic for our news feed and mainapp
# Views file

# detail view of the post
class PostDetailPage(View):
	def get(self, request, pk):

		post = get_object_or_404(Post, id=pk)
		comments = CommentToPost.objects.all().filter(post_id=pk)
		form = CommentToPostForm
		ctx = {
		'post':post,
		'form':form,
		'comments':comments,
		}
		return render(request, 'mainapp/post_detail.html', ctx)
	def post(self, request, pk):
		if request.user.is_authenticated:
			form = CommentToPostForm(request.POST)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.user = request.user
				obj.post = get_object_or_404(Post, pk=pk)
				obj.save()
				return redirect('mainapp:post-detail', pk)
			else:
				return render(request, 'mainapp/post_detail.html', ctx)
		else:
			ctx = {
			'post':post,
			'form':form,
			'comments':comments,
			}
			return render(request, 'mainapp/post_detail.html', ctx)

# home page
class HomePage(View):
	def get(self, request):
		return render(request, 'mainapp/home_page.html')

# newspage
class NewsPage(generic.ListView):
	template_name = 'mainapp/home.html'
	paginate_by = 5
	model = Post

	def get_queryset(self):
		self.news_count = Post.objects.all().count()
		queryset = super(NewsPage, self).get_queryset()
		# reverse queryset
		return queryset[::-1]

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['news_count'] = self.news_count
		return ctx

# All news page
class NewsAllPage(generic.ListView):
	template_name = 'mainapp/news_all.html'
	model = Post
	def get_queryset(self):
		news = Post.objects.all()
		# filter all usernames
		queryset = super(NewsAllPage, self).get_queryset()


		self.myFilter = newsFilter(self.request.GET, queryset=news)
		
		queryset = self.myFilter.qs 
		return queryset

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['myFilter'] = self.myFilter
		return ctx


# about page
class AboutPage(View):
	def get(self, request):
		return render(request, 'mainapp/about_page.html')

# support us page
class SupportUs(View):
	def get(self, request):
		return render(request, 'mainapp/support_us_page.html')

# download page
class DownloadPage(View):
	def get(self, request):
		return render(request, 'mainapp/download_page.html')



# footer contact form + contact form in contact form view
class ContactPage(FormView):
	def get(self, request):
		form = ContactEmailsForm()
		ctx = {
		'form':form,
		}
		return render(request, 'mainapp/contact_page.html', ctx)
	def post(self, request):
		form = ContactEmailsForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('mainapp:confirm-contact-page')
		else:
			ctx = {
			'form':form,
			}
			return render(request, 'mainapp/contact_page.html', ctx)
		# save email to the database


# if the user sended their mail correct, they would be redirected to the confirmed view
class ConfirmPage(View):
	def get(self, request):
		return render(request, 'mainapp/contact_confirm_page.html')



# view of the security page
class SecurityContactPage(FormView):
	def get(self, request):
		form = SecutiryMainForm()
		ctx = {
		'form':form,
		}
		return render(request, 'mainapp/security_bug_send.html', ctx)
	def post(self, request):
		form = SecutiryMainForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('mainapp:secutiry-report-success')
		else:
			ctx = {
			'form':form,
			}
			return render(request, 'mainapp/security_bug_send.html', ctx)

# success security page view
class SuccessSecurityPage(View):
	def get(self, request):
		return render(request, 'mainapp/security_success.html')

def page_not_found(request, exception):
	response = render_to_response('404.html',context_instance=RequestContext(request))
	response.status_code = 404
	return response
