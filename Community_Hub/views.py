from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
import random, string
from twilio_send_otp import *
from .models import User, Phone, Post, Volunteer, VolunteerMessage, Feedback, Contact
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
def home(request):
    username = request.session.get('username')
    try:
        posts = Post.objects.filter(status="verified").order_by('-updated_date')[:10]
    except Post.DoesNotExist:
        posts = None
    
    context = {
        'username' : username,
        'posts': posts,
    }
    return render(request, 'index.html', context)

def logout_page(request):
    request.session.flush()
    messages.success(request, "Logging out.... See you soon!")
    return redirect('Home Page')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def all_posts(request):
    username = request.session.get('username')
    try: 
        posts = Post.objects.filter(status="verified").order_by('-updated_date')
    except Post.DoesNotExist:
        posts = None
    
    print(posts)
    context = {
        'username': username,
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def create_post(request):
    username = request.session.get('username')
    return render(request, 'create_post.html', {'username' : username})

def about(request):
    username = request.session.get('username')
    return render(request, 'about.html', {'username' : username})

def feedback(request):
    username = request.session.get('username')
    return render(request, 'feedback.html', {'username' : username})

def contact(request):
    username = request.session.get('username')
    return render(request, 'contact.html', {'username' : username})

def profile(request, username):
    if username is None:
        username = request.session.get('username')
        if not username:
                messages.warning(request, 'Please login first to view your profile!')
                return redirect('Login Page')
    
    user = get_object_or_404(User, username=username)
    
    if not user:
        messages.warning(request, "User not found or or session expired. Please login again!")
        return redirect('Login Page')
    
    context = {
        'username' : username,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'profession': user.profession,
        'user_photo' : user.photo,
        'address': user.address,
    }
    
    posts = user.posts.filter(status="verified").order_by('-created_date')
    if not posts:
        return render(request, 'profile.html', context)
    
    context['posts'] = posts
    return render(request, 'profile.html', context)

registered = False

def register_phone_verify(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        phone = data.get("phone")
        registered = Phone.objects.filter(phone=phone).exists()
        user_registered = User.objects.filter(phone_number = phone).exists()
        if user_registered:
            return JsonResponse({"success":False, "message":"A user with this phone number already exists. Please use another phone number or got to login page to login!", "status": 400})
        if registered:
            result = send_otp(phone)
            return JsonResponse(result)
        else:
            Phone.objects.create(
                phone= phone
            )
            return JsonResponse({"success":False, "message":"Get your number registered on Twilio. Need Help? Go to the contact page and send us your details. Our developers will contact you!!", "status": 400})
            
def register_phone_verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        phone = data.get("phone")
        otp = data.get("otp")
        result = verify_otp(phone, otp)
        if result["success"]:
            return JsonResponse(result)
        else:
            return JsonResponse(result)
        
@ensure_csrf_cookie
def get_started_form(request):
    print(request.POST)
    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        phone_num = request.POST.get("phone_number")
        password = request.POST.get("password1")
        address = request.POST.get("user_address")
        profession = request.POST.get("user_proffession")
        image_file = request.FILES.get("user_photo")

        if not all([firstname, lastname, phone_num, password, address, profession, image_file]):
            messages.error(request, "Please fill in all fields!")
            return render(request, 'register.html')
        
        user_name = firstname.replace(" ", "").lower() + lastname.replace(" ", "").lower() + ''.join(random.choices(string.digits, k=3))

        try:
            if not Phone.objects.filter(phone=phone_num).exists():
                return render(request, 'register.html', {'error': 'Please reigister your number on Twilio.'})
            
            user = User.objects.create(
                first_name=firstname,
                last_name=lastname,
                username=user_name,
                password=make_password(password),
                phone_number=phone_num,
                address = address,
                profession = profession,
                photo = image_file     
            )
            request.session['username'] = user.username
            request.session['phone'] = user.phone_number
            messages.success(request, "Registration successful!")
            return redirect('Home Page')
        except IntegrityError:
            messages.error(request, "A user with this phone number already exists. Please use another phone number or got to login page to login!")
            return render(request, 'register.html')
    messages.error(request, "Form not submitted. Please try again")
    return render(request, 'register.html')

def login_user(request):
    if request.method == "POST":
        phone_num = request.POST.get("phone-number")
        password = request.POST.get("password")
        if not all([phone_num, password]):
            messages.error(request, "Please provide both phone number and password!")
            return redirect('Login Page')
        try:
            user = User.objects.get(phone_number=phone_num)
            if check_password(password, user.password):
                request.session['username'] = user.username
                request.session['phone'] = user.phone_number
                messages.success(request, "Login successful!")
                return redirect('Home Page')
            else:
                messages.error(request, "Incorrect password!")
                return redirect('Login Page')
        except User.DoesNotExist:
            messages.error(request, "Invalid phone number or password!")
            return redirect('Login Page')
    return redirect('Login Page')

def login_phone_verify(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        phone = data.get("phone")
        registered = User.objects.filter(phone_number=phone).exists()
        if not registered:
            return JsonResponse({"success": False, "message": "No user exists with this phone number! Please re-check!!"})
        request.session['phone'] = phone
        result = send_otp(phone)
        return JsonResponse(result)
    return redirect('Login Page')

def login_phone_verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        phone = request.session.get('phone')
        otp = data.get("otp")
        result = verify_otp(phone, otp)
        return JsonResponse(result)
    return redirect('Login Page')

def reset_password(request):
    if request.method == "POST":
        phone = request.session.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not all([password1, password2]):
            messages.error(request, "Please fill in all fields!")
            return redirect('Login Page')
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('Login Page')
        try:
            user = User.objects.get(phone_number=phone)
            user.password = make_password(password1)
            user.save()
            del request.session['phone']
            messages.success(request, "Password reset successful! Please login with your new password!")
            return redirect('Login Page')
        except User.DoesNotExist:
            messages.error(request, "User does not exist! Please register first!")
            return redirect('Register Page')
    return redirect('Login Page')

def create_post_submit(request):
    if request.method == "POST":
        user_name = request.session.get('username')
        title = request.POST.get('post_title')
        description = request.POST.get('post_description')
        date = request.POST.get('post_date')
        author_name = request.POST.get('author_name')
        phone_number = request.POST.get('author_phone')
        location = request.POST.get('post_location')
        category = request.POST.get('post_category')
        
        if not all([title, description, date, author_name, phone_number, location, category]):
            messages.error(request, "Please fill in all fields!!!")
            return redirect('Create Post Page')
        
        try:
            user= User.objects.get(username=user_name, phone_number=phone_number)
            post = Post.objects.create(
                author = user,
                title = title,
                description = description,
                event_date = date,
                author_name = author_name,
                author_phone_number = user,
                location = location,
                category = category
            )
            messages.success(request, "Post created successfully!! Will be visible after admin approval. Thank you for your patience.")
            Volunteers = Volunteer.objects.filter(address = location)
            post_id = post.id
            message_post = f"Post ID: {post_id}\nTitle: {title}\nDescription: {description}\nLocation: {location}\nDate: {date}\n Please login to your admin panel and verify the post."
            for volunteer in Volunteers:
                result = send_message(volunteer.phone_number, message_post)
                if result["success"]:
                    VolunteerMessage.objects.create(
                        volunteer = volunteer,
                        post = post,
                        message_sid = result["sid"]
                    )
            return redirect('All Posts Page')
        except User.DoesNotExist:
            messages.error(request, "User does not exist! Please provide correct details(phone number).")
            return redirect('Create Post Page')
        
#def sms_reply(request):
#    if request.method == "POST":
#        incoming_msg = request.POST.get('Body', '').strip().lower() 
#        from_number = request.POST.get('From', '')
#        print(f"Message from {from_number}: {incoming_msg}")
        
       # try:
      #      msg = VolunteerMessage.objects.filter(
     #           volunteer = Volunteer.objects.get(phone_number=from_number),
    #            status = "sent",         
   #         ).latest('id')
#          post = msg.post
#
           # if incoming_msg == "yes":
              #  post.status = "approved"
             #   post.save()
            #elif incoming_msg == "no":
           #     post.status = "rejected"
         #       post.save()
          #  msg.status = "replied"
        #    msg.save()                
       # except VolunteerMessage.DoesNotExist:
     #       print("No pending messages found for this volunteer.")
    #return HttpResponse("Message processed")

def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get('author_name')
        rating = request.POST.get('feedback_rating')
        feedback_text = request.POST.get('feedback_description')
        
        if not rating:
            messages.error(request, "Please provide a rating!")
            return redirect('Feedback Page')
        
        try:
            Feedback.objects.create(
                author_name = name,
                rating = rating,
                feedback = feedback_text
            )
            messages.success(request, "Thank you for your feedback!")
            return redirect('Home Page')
        except Exception as e:
            messages.error(request, "An error occured while submitting your feedback. Please try again.")
            return redirect('Feedback Page')
        
def submit_contact(request):
    if request.method == "POST":
        name = request.POST.get('author_name')
        phone = request.POST.get('author_phone')
        subject = request.POST.get('subject')
        description = request.POST.get('subject_description')
        
        if not all([name, phone, subject, description]):
            messages.error(request, "Please fill in all the fields!")
            return redirect('Contact Page')
        
        try:
            Contact.objects.create(
                name = name,
                phone_number = phone,
                subject = subject,
                description = description
            )
            messages.success(request, "Please wait while our team will contact you soon! Thank you for reaching to us!")
            return redirect('Home Page')
        except Exception as e:
            messages.error(request, "An error occured while submitting your contact details. Please try again!")
            return redirect('Contact Page')
    
def submit_filter_request(request):
    username = request.session.get('username')

    if request.method == "POST":
        print(request.POST)
        category = request.POST.get('category')
        location = request.POST.get('location')
        
        posts = Post.objects.all()
        if category and location:
            posts = posts.filter(category=category, location=location)
        elif category:
            posts = Post.objects.filter(category=category)
        elif location:
            posts = posts.filter(location=location)
        
        if not posts.exists():
            messages.error(request, "No posts found for the selected filters!")
        else:
            messages.success(request, 'Filtered posts fetched successfully!')
        
        context = {
            'username': username,
            'posts': posts,
        }
        return render(request, 'all_posts.html', context)
                    