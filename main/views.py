from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.response import Response
from .serializers import CommentSerializer, PostSerializer, LikeSerializer, UserSerializer
from rest_framework.decorators import api_view
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse

# Login Page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'main/login.html', context)

# Register Page
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'main/register.html', {'form': form})

# Logout User
def logoutUser(request):
    logout(request)
    return redirect('home')

# Check User Name
def check_name(request):
    username = request.GET.get('name')
    response = {
        'is_taken': User.objects.filter(name__iexact=username).exists()
    }
    return JsonResponse(response)

# Home Page
def home(request):
    return HttpResponse('dwa')


# # User Page
# @login_required(login_url='login')
# def userProfile(request, slug):
#     user = User.objects.get(name=slug)
#     if request.method == 'POST' and 'follow' in request.POST:
#         try:
#             follow = Subscriber.objects.get(user=user, name=request.user)
#             follow.delete()
#         except:
#             Subscriber.objects.create(user=user, name=request.user)
#     posts = user.post_set.filter(user=user)
#     total_posts = posts.count()
#     total_subscribers = user.subscriber_set.filter(user=user).count()
#     subscribers = user.subscriber_set.filter(user=user)
#     user_subs = Subscriber.objects.filter(user = user)
#     subscribes = Subscriber.objects.filter(name=user)
#     total_subscribes = subscribes.count()
#     context = {'user': user,
#                'posts': posts,
#                'subscribes':subscribes,
#                'total_subscribes':total_subscribes,
#                'total_subscribers':total_subscribers,
#                'subscribers':subscribers,
#                'total_posts':total_posts,
#                'all_subs':user_subs}
#     return render(request, 'main/profile.html', context)

# # Favorite Posts Page
# @login_required(login_url='login')
# def favoritePost(request, slug):
#     user = User.objects.get(name=slug)
#     my_likes = Like.objects.filter(user__name=user.name)
#     if request.method == 'POST' and 'like' in request.POST:
#         like = request.POST.get('like')
#         post = Post.objects.get(id=like)
#         try:
#             like = Like.objects.get(user=request.user, post=post)
#             like.delete()
#         except:
#             Like.objects.create(user = request.user, post=post)
#         return redirect('favorite', slug=user.name)
#     return render(request, 'main/favorite.html', {'my_likes': my_likes})

# # Update User Page
# @login_required(login_url='login')
# def updateUser(request):
#     user = request.user
#     form = UserForm(instance=user)

#     if request.method == 'POST':
#         form = UserForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile', slug=user.name)

#     return render(request, 'main/update_user.html', {'form': form})


# # Delete Comment
# @login_required(login_url='login')
# def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect('post', pk=comment.post.id)


# API
@api_view(['GET'])
def ApiOverView(request):
    api_conf={
        'List':'post-list/',
        'Detail':'post-detail/id/',
        'Create':'post-create/',
        'Update':'post-update/id/',
        'Delete':'post-delete/id/',

        'Comment Create':'comment-create/',
        'Comment Delete':'comment-delete/id/',

        'Like Create':'like-create/',
        'Like Delete':'like-delete/id',

        'Users':'users/',
        
        'Message List':'messages/',
        'Message Detail':'message/id/',
        'Message Create':'message-create/',
        'Message Update':'message-update/id/',
        'Message Delete':'message-delete/id/'
    }
    return Response(api_conf)



@api_view(['GET'])
def postList(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def postCreate(request):
    post = PostSerializer(data=request.data)
    if post.is_valid():
        post.save()
    return Response(post.data)


@api_view(['POST'])
def postUpdate(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def postDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response("Item successfully deleted")

@api_view(['POST'])
def commentCreate(request):
    comment = CommentSerializer(data=request.data)
    if comment.is_valid():
        comment.save()
    return Response(comment.data)


@api_view(['DELETE'])
def commentDelete(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return Response("Item successfully deleted")


@api_view(['POST'])
def likeCreate(request):
    like = LikeSerializer(data=request.data)
    if like.is_valid():
        like.save()
    return Response(like.data)

@api_view(['DELETE'])
def likeDelete(request, pk):
    like = Like.objects.get(id=pk)
    like.delete()
    return Response("Item successfully deleted")


@api_view(['GET'])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)