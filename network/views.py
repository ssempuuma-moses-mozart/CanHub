import logging
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import json
from django.db.models import Count, Prefetch
from network.forms import UserProfileForm
from public.models import Crowdfunding, Donation
from django.views.decorators.http import require_GET
from django.http import HttpResponseBadRequest
from .models import *
from .models import FollowersCount
from django.contrib import messages
from itertools import chain
import random
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from django.views import View
from .forms import GroupForm

logger = logging.getLogger(__name__)


def index(request):
    # Fetch all posts and order by date_created, including comments
    all_posts = Post.objects.all().prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('commenter').order_by('comment_time'))
    ).order_by('-date_created')
    
    # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated
    
    # Initialize variables for authenticated users
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0

     # Get counts for the logged-in user
    follower_count = Follow.objects.filter(followed=request.user).count() if is_logged_in else 0
    following_count = Follow.objects.filter(follower=request.user).count() if is_logged_in else 0

    all_users = User.objects.exclude(id=request.user.id) if is_logged_in else User.objects.all()
    # Prepare a dictionary to hold follow statuses
    follow_statuses = {}
    
    if is_logged_in:
        # Get user's full name and profile picture URL
        full_name = request.user.get_full_name()
        user_profile_picture = request.user.profile_pic.url if request.user.profile_pic else None

        followed_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        follow_statuses = {user.id: user.id in followed_users for user in all_users}

    
    
    posts = Post.objects.all().annotate(num_comments=Count('comments'))

    groups = Group.objects.all()

    # Debug: Print the number of groups
    print(f"Number of groups: {groups.count()}")
    
    # Render the index page with context
    return render(request, "network/index.html", {
        "posts": posts,
        'all_posts': all_posts,
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'all_users': all_users,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'groups': groups,
        'profile': False,
        'follow_statuses': follow_statuses,  # Pass follow statuses to the template
        'follower_count': follower_count,
        'following_count': following_count,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/index.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        print(f"--------------------------Profile: {profile}----------------------------")
        cover = request.FILES.get('cover')
        print(f"--------------------------Cover: {cover}----------------------------")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/index.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover           
            user.save()
        
        except IntegrityError:
            return render(request, "network/index.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")
    

@login_required
def profile(request):
    user = request.user
    post_count = Post.objects.filter(creater=user).count()
    return render(request, 'index.html', {'post_count': post_count})



@login_required
def upload_post(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text', '')
        content_image = request.FILES.get('content_image')
        content_video = request.FILES.get('content_video')

        # Create and save the new post
        new_post = Post(
            creater=request.user,
            content_text=content_text,
            content_image=content_image,
            content_video=content_video
        )
        new_post.save()

        return redirect('index')  # Redirect to the index or another appropriate page

    return redirect('index')  # Redirect to the index or another appropriate page if not POST


@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@csrf_exempt
def dashboad_view(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    # Get all donations related to the item
    # donations = Donation.objects.filter(item=item)
    
    # Filter donations related to the item by the current logged-in user
    donations = Donation.objects.filter(item=item, user=request.user)

    posts = Post.objects.all().order_by('-date_created')
    # Assuming you have a queryset of crowdfunding items
    crowdfunding = Crowdfunding.objects.all()

    # Pass user details to the context
    user = request.user

    # Calculate total donation amount for the current user
    total_donation = Donation.objects.filter(user=request.user).aggregate(models.Sum('amount'))['amount__sum']
     # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'crowdfunding': crowdfunding,
        'closing_date': item.closing_date,
        "posts": posts,
        'donations': donations,  # Pass donations to the context
        'user': user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/dashboad.html', context)


@login_required
@csrf_exempt
def my_donations_view(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    donations = Donation.objects.filter(item=item, user=request.user)
    crowdfunding = Crowdfunding.objects.all()
    user = request.user
    total_donation = Donation.objects.filter(user=request.user).aggregate(models.Sum('amount'))['amount__sum']
     # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'crowdfunding': crowdfunding,
        'closing_date': item.closing_date,
        'donations': donations,  # Pass donations to the context
        'user': user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/my_donations.html', context)



@login_required
def campaigns_view(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    # Get donations related to the item by the current logged-in user
    donations = Donation.objects.filter(item=item, user=request.user)

    # Filter crowdfunding items to include only campaigns that the user has donated to
    crowdfunding = Crowdfunding.objects.filter(donation__user=request.user).distinct().order_by('-id')

    # Calculate total donation amount for the current user
    total_donation = donations.aggregate(models.Sum('amount'))['amount__sum']
    # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'crowdfunding': crowdfunding,
        'closing_date': item.closing_date,
        'donations': donations,  # Pass donations to the context
        'user': request.user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/campaigns.html', context)


def user_logout_view(request):
    logout(request)
    return render(request, 'public/home.html')     


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the user's profile after saving
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'index.html', {'form': form})


@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if post.likers.filter(id=user.id).exists():
        post.likers.remove(user)
        liked = False
    else:
        post.likers.add(user)
        liked = True

    like_count = post.likers.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})


@require_POST
def submit_comment(request, post_id):
    try:
        data = json.loads(request.body)
        post = get_object_or_404(Post, id=post_id)

        comment_content = data.get('comment_content', '').strip()
        print(f"Comment Content: '{comment_content}'")  # Debugging output

        if not request.user.is_authenticated:
            print("User is not authenticated.")
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        if not comment_content:
            print("Received empty comment content.")
            return JsonResponse({'error': 'Empty comment not allowed'}, status=400)

        # Save the new comment
        new_comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=comment_content,
            comment_time=timezone.now()
        )
        
        print("Comment saved successfully:", new_comment)  # Debugging output
        return JsonResponse(new_comment.serialize(), status=201)

    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"An error occurred while saving comment: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)
    


@require_POST
def group_comment(request, post_id):
    try:
        data = json.loads(request.body)
        group_post = get_object_or_404(GroupPost, id=post_id)

        comment_content = data.get('comment_content', '').strip()
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        if not comment_content:
            return JsonResponse({'error': 'Empty comment not allowed'}, status=400)

        # Save the new comment
        new_comment = GroupComment.objects.create(
            group_post=group_post,
            commenter=request.user,
            comment_content=comment_content,
            comment_time=timezone.now()
        )

        return JsonResponse(new_comment.serialize(), status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"An error occurred while saving comment: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)



def my_network_view(request):
    # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated
    
    # Initialize variables for authenticated users
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0

    groups = Group.objects.all()
    # Debug: Print the number of groups
    print(f"Number of groups: {groups.count()}")
    
    if is_logged_in:
        # Get user's full name and profile picture URL
        full_name = request.user.get_full_name()
        user_profile_picture = request.user.profile_pic.url if request.user.profile_pic else None


    # Check if the user is a member of each group
    is_member = {group.id: GroupMembership.objects.filter(user=user, group=group).exists() for group in groups}
    # Get all users, excluding the current user if desired
    all_users = User.objects.exclude(id=request.user.id) if is_logged_in else User.objects.all()

    # Prepare a dictionary to hold follow statuses
    follow_statuses = {}
    if is_logged_in:
        followed_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        follow_statuses = {user.id: user.id in followed_users for user in all_users}

    posts = Post.objects.all().annotate(num_comments=Count('comments'))

    # Render the index page with context
    return render(request, "network/my_network.html", {
        "posts": posts,
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'all_users': all_users,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'profile': False,
        'groups':groups,
        'is_member':is_member,
        'follow_statuses': follow_statuses,  # Pass follow statuses to the template
    })


def groups_view(request):
    success_message = None  # Variable to hold the success message
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user  # Assuming the admin is the current logged-in user
            group.save()
            success_message = "Group Created Successfully!"  # Set the success message
            form = GroupForm()  # Reinitialize the form after successful submission
            # return redirect('groups')  # Redirect to a success page
            
    else:
        form = GroupForm()
     # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated
     # Initialize variables for authenticated users
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0
             # Fetch all groups
    groups = Group.objects.all()
    # Debug: Print the number of groups
    print(f"Number of groups: {groups.count()}")
    
    if is_logged_in:
        # Get user's full name and profile picture URL
        full_name = request.user.get_full_name()
        user_profile_picture = request.user.profile_pic.url if request.user.profile_pic else None

     # Check if the user is a member of each group
    is_member = {group.id: GroupMembership.objects.filter(user=user, group=group).exists() for group in groups}    

    all_users = User.objects.exclude(id=request.user.id) if is_logged_in else User.objects.all()  # Exclude the current user if desired

    return render(request, 'network/groups.html',{
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'all_users':all_users,
        'groups': groups,  # Pass groups to the template
        'profile': False,
        'form': form,  # Pass the form to the template
        'is_member':is_member,
        'success_message': success_message  # Pass the success message to the template
    })



def notifications_view(request):
     # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated
     # Initialize variables for authenticated users
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0
    
    if is_logged_in:
        # Get user's full name and profile picture URL
        full_name = request.user.get_full_name()
        user_profile_picture = request.user.profile_pic.url if request.user.profile_pic else None

    return render(request, 'network/notifications.html',{
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'profile': False
    })



def group_detail_view(request, id):
        # Fetch all posts and order by date_created, including comments
    all_posts = GroupPost.objects.all().prefetch_related(
        Prefetch('group_comments', queryset=GroupComment.objects.select_related('commenter').order_by('comment_time'))
    ).order_by('-date_created')
    group = get_object_or_404(Group, id=id)
    is_logged_in = request.user.is_authenticated
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0
    groups = Group.objects.all()
    number_of_members = GroupMembership.objects.filter(group=group).count()

    print(f"Number of groups: {groups.count()}")
    posts = []

      # Create a dictionary to hold membership statuses
    membership_status = {}

    if is_logged_in:
        full_name = user.get_full_name()
        user_profile_picture = user.profile_pic.url if user.profile_pic else None
        is_member = GroupMembership.objects.filter(user=user, group=group).exists()

        memberships = GroupMembership.objects.filter(user=user)
        membership_status = {membership.group.id: True for membership in memberships}
       
        
        # Fetch posts for the group and order by date_created descending
        # posts = GroupPost.objects.filter(group=group).order_by('-date_created')
        posts = GroupPost.objects.filter(group=group).annotate(num_comments=Count('group_comments')).order_by('-date_created')


        if request.method == "POST":
            if not is_member:
                GroupMembership.objects.create(user=user, group=group)
                print(f"{user.username} has joined the group {group.group_name}.")

            # Handle post creation
            content_text = request.POST.get('content_text', '').strip()  # Strip whitespace
            content_image = request.FILES.get('content_image')
            content_video = request.FILES.get('content_video')

            # Only create a new post if there is content
            if content_text or content_image or content_video:
                new_post = GroupPost(
                    creater=user,
                    content_text=content_text,
                    content_image=content_image,
                    content_video=content_video,
                    group=group,  # Associate the post with the group
                )
                new_post.save()
                messages.success(request, "Your post has been created!")
            else:
                messages.warning(request, "You need to provide some content to create a post.")
                
            return redirect('group_detail', id=id)

    else:
        is_member = False

    all_users = User.objects.exclude(id=request.user.id) if is_logged_in else User.objects.all()

    return render(request, 'network/group_detail.html', {
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'all_users': all_users,
        'groups': groups,
        'profile': False,
        'group': group,
        'number_of_members': number_of_members,
        'is_member': is_member,
        'membership_status': membership_status,  # Pass the membership status to the template
        'posts': posts,  # Pass posts to the template
        'all_posts':all_posts,
    })


@require_POST
def toggle_like_group(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)
    user = request.user
    
    if post.likers.filter(id=user.id).exists():
        post.likers.remove(user)
        liked = False
    else:
        post.likers.add(user)
        liked = True

    like_count = post.likers.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})




@require_POST
def toggle_follow(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    follower_user = request.user

    follow_instance = Follow.objects.filter(follower=follower_user, followed=followed_user).first()

    if follow_instance:
        # Unfollow
        follow_instance.delete()
        following = False
    else:
        # Follow
        Follow.objects.create(follower=follower_user, followed=followed_user)
        following = True

    # Optionally, return the follow count or other relevant information
    follow_count = followed_user.followers.count()  # Adjust if you want to get the follower count

    return JsonResponse({'following': following, 'follow_count': follow_count})



def messaging_view(request):
    # Variable to hold the success message (if any)
    success_message = None

    # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated

    # Initialize variables for authenticated users
    user_profile_picture = None
    full_name = None
    user = request.user if is_logged_in else None
    post_count = Post.objects.filter(creater=user).count() if is_logged_in else 0

    # Fetch all groups
    groups = Group.objects.all()

    # Debug: Print the number of groups
    print(f"Number of groups: {groups.count()}")

    if is_logged_in:
        # Get user's full name and profile picture URL
        full_name = request.user.get_full_name()
        user_profile_picture = request.user.profile_pic.url if request.user.profile_pic else None

    # Check if the user is a member of each group
    is_member = {group.id: GroupMembership.objects.filter(user=user, group=group).exists() for group in groups}

    # Fetch all users, excluding the current user if desired
    all_users = User.objects.exclude(id=request.user.id) if is_logged_in else User.objects.all()

    return render(request, 'network/messaging.html', {
        'user_profile_picture': user_profile_picture,
        'full_name': full_name,
        'post_count': post_count,
        'is_logged_in': is_logged_in,
        'all_users': all_users,
        'groups': groups,  # Pass groups to the template
        'profile': False,
        'is_member': is_member,
        'success_message': success_message  # Pass the success message to the template (if needed)
    })


User = get_user_model()

def messaging_view(request):
    # Fetch all users except the logged-in user
    users = User.objects.exclude(id=request.user.id)
    context = {
        'users': users
    }
    return render(request, 'network/messaging.html', context)




