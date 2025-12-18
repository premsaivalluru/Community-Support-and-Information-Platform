from django.contrib import admin
from .models import User, Phone, Volunteer, Post, Feedback, Contact, VolunteerMessage, PostVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'created_date', 'updated_date')
    search_fields=('first_name', 'phone_number')


@admin.register(Phone)
class UserPhone(admin.ModelAdmin):
    list_display = ('phone','created_at')
    search_fields = ('phone', 'created_at')


@admin.register(Volunteer)
class UserVolunteer(admin.ModelAdmin):
    list_display = ('user', 'address','profession','created_date', 'updated_date')
    search_fields = ('user__username', 'user__phone_number')


@admin.register(Feedback)
class UserFeedback(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'created_date')
    search_fields = ('author_name', 'rating')

@admin.register(Contact)
class UserContact(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_date')
    search_fields = ('name', 'subject', 'phone_number')

@admin.register(VolunteerMessage)
class VolunteerReply(admin.ModelAdmin):
    list_display = ('volunteer__user__username', 'post__title', 'created_date', 'updated_date')
    search_fields = ('volunteer_username', 'post_title')

    def volunteer_username(self, obj):
        return obj.volunteer.user.username
    volunteer_username.short_description = "Volunteer Username"

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = "Post Title"

@admin.register(PostVerification)
class PostVerificationAdmin(admin.ModelAdmin):
    list_display = ('post__title', 'volunteer__user__username', 'status', 'created_date')
    search_fields = ('post__title', 'volunteer__user__username', 'status')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'status', 'created_date', 'updated_date', 'verified_by')
    search_fields = ('status', 'location', 'category')
    actions = ['mark_verified', 'mark_rejected']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'volunteer_profile'):
            return qs.filter(location=request.user.volunteer_profile.address)
        return qs.none()
    
    def mark_verified(self, request, queryset):
        volunteer = getattr(request.user, 'volunteer_profile', None)
        if volunteer:
            for post in queryset:
                obj, created = PostVerification.objects.get_or_create(
                    post = post,
                    volunteer = volunteer,
                    defaults = {'status': 'true'}
                )
                if not created:
                    obj.status = 'true'
                    obj.save()
    mark_verified.short_description = "Mark selected posts as Verified"
    
    def mark_rejected(self, request, queryset):
        volunteer = getattr(request.user, 'volunteer_profile', None)
        if volunteer:
            for post in queryset:
                obj, created = PostVerification.objects.get_or_create(
                    post = post,
                    volunteer = volunteer,
                    defaults = {'status': 'false'}
                )
                if not created:
                    obj.status = 'false'
                    obj.save()
    mark_rejected.short_description = "Mark selected posts as Rejected"


    
# Register your models here.
