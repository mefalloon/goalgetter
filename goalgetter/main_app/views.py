from django.shortcuts import render, redirect
from .models import Course, Assignment
from .forms import AssignmentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth import login 

# Add the following import
from django.http import HttpResponse

class CourseCreate(LoginRequiredMixin, CreateView):
  model = Course
  fields = ['name', 'subject']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the course
    return super().form_valid(form)


# class AssignmentUpdate(UpdateView):
#   model = Assignment
#   fields = ['name', 'date', 'category', 'todo']

# class AssignmentDelete(DeleteView):
#   model = Assignment
#   success_url = 'courses/<int:course_id>/'

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def courses_index(request):
  courses = Course.objects.filter(user=request.user)
  return render(request, 'courses/index.html', { 'courses': courses })

@login_required
def courses_detail(request, course_id):
  course = Course.objects.get(id=course_id)
  assignment_form = AssignmentForm()
  return render(request, 'courses/detail.html', {'course': course, 'assignment_form': assignment_form})

def add_assignment(request, course_id):
  form = AssignmentForm(request.POST)
  if form.is_valid():
    new_assignment = form.save(commit=False)
    new_assignment.course_id = course_id
    new_assignment.save()
  return redirect('detail', course_id=course_id) 

def delete_assignment(request, course_id, assignment_id):
  # Course.objects.get(id=course_id).assignments.remove(assignment_id)
  Assignment.objects.filter(id=assignment_id).delete()
  return redirect('detail', course_id=course_id)

def update_assignment(request, course_id, assignment_id):
  Assignment.objects.filter(id=assignment_id).update()
  return redirect('detail', course_id=course_id)


# I would definitely start with changing from delete to update
# Then grab your current assignment info into a variable and make changes to it as if you’re just writing in Python - that’s my assumption. Don’t forget to call .save() tho
# 12:39
# so like variable.name = new name then variable.save() before you render or redirect

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)