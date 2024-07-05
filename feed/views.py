from django.shortcuts import render, redirect
from accounts.models import Profile
from feed.models import Post, PostMedia, Comment, Reaction
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'feed/feed.html', {})

def explore(request):
    return render(request, 'feed/explore.html', {})

def create_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        caption = request.POST.get('comment')
        print(caption)

        images = request.FILES.getlist('images')
        saved_files = []
        
        newpost = Post(caption=caption, user_id=request.user)
        newpost.save()

        for image in images:
            file_name = default_storage.save("posts/"+image.name, ContentFile(image.read()))
            file_url = default_storage.url(file_name)
            print(file_url)
            saved_files.append(file_url)
            attachment = PostMedia(post_id = newpost, image=file_name)
            attachment.save()

        # Check if a user with the provided username exists
        if newpost:
            return JsonResponse({'success': True, 'message': 'Post Successful'}, status=200)
        return JsonResponse({'success': False, 'message': 'Something Went Wrong'}, status=406)
    return redirect('home')

def search(request):
    return render(request, 'feed/search.html', {})

def notifications(request):
    return render(request, 'feed/feed.html', {})

def profile(request, username):
    try:
        user = Profile.objects.get(username=username)
        user_followers = Profile.objects.filter(following=user)
        user_following = user.following.all()
        user_posts = Post.objects.filter(user_id=user).count()
        if request.user.is_authenticated:
            if request.user.following.filter(username=username).exists():
                am_i_following = True
            else:
                am_i_following = False
        else:
            am_i_following = False

        return render(request, 'feed/profile.html', status=200, context={"user": user, "am_i_following": am_i_following, "user_posts": user_posts, "user_followers": user_followers, "user_following": user_following})
    except Profile.DoesNotExist:
        return render(request, '404.html', {}, status=404)
    except Exception as e:
        return render(request, '404.html', {}, status=404)

def profile_post(request, username, post):
    try:
        user = Profile.objects.get(username=username)
        post = Post.objects.get(id=post, user_id=user)
        comments = Comment.objects.filter(post_id=post, parent_comment=None).order_by('-created_at')

        user_has_liked = post.likes.filter(user_id=user).exists()

        context = {
            "user":user,
            'post': post,
            'comments': comments,
            'user_has_liked': user_has_liked,
        }

        return render(request, 'feed/post.html', context=context, status=200)
    except Profile.DoesNotExist:
        return render(request, '404.html', {}, status=404)
    except Post.DoesNotExist:
        return render(request, '404.html', {}, status=404)
    except Exception as e:
        return redirect(f'/{username}/', status=302)
    
def post_comment(request):
    if request.method == "POST" and request.user.is_authenticated:
        parent_comment = request.POST.get('parent_comment')
        post_comment = request.POST.get('post_comment')
        post_id = request.POST.get('post_id', None)

        post = Post.objects.get(id=post_id)

        new_comment = Comment(user_id = request.user, post_id = post, text=post_comment)

        if parent_comment:
            parent = Comment.objects.get(id=parent_comment)
            new_comment.parent_comment = parent

        # Check if a user with the provided username exists
        if new_comment:
            new_comment.save()
            return JsonResponse({'success': True, 'message': 'Post Successful'}, status=200)
        
        return JsonResponse({'success': False, 'message': 'Something Went Wrong'}, status=406)
    return redirect('home')

@login_required
def post_like(request):
    if request.method == "POST":
        try:
            postId = request.POST.get('post')
            print(postId)
            user = request.user
            post = Post.objects.get(id=postId)
            if user.likes.filter(post_id=post).exists():
                user.likes.filter(post_id=post).delete()
                return JsonResponse({'success': True, 'message': 'Post Unliked!'}, status=200)
            else:
                newReaction = Reaction(user_id=user, post_id=post)
                newReaction.save()
                user.likes.add(newReaction)
                return JsonResponse({'success': True, 'message': 'Post Liked!'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Post does not exist!'}, status=404)
    return redirect('home')