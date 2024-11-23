from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# In this owner file, we define functionality for admin user and typical user
# Typical user see only edit things on what only he did created. Admin user see everything

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
	# If user is admin show him page, if user.request == user.owner (just user) show him page
	def get_queryset(self):
		qs = super(OwnerUpdateView, self).get_queryset()
		if self.request.user.is_staff:
			return qs
		else:	
			return qs.filter(user=self.request.user)

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
	# If user is admin show him page, if user.request == user.owner (just user) show him page
	def get_queryset(self):
		qs = super(OwnerDeleteView, self).get_queryset()
		if self.request.user.is_staff:
			return qs
		else:	
			return qs.filter(user=self.request.user)