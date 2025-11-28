from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Like, Comment
from members.models import Member
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            # In a real app, you'd set comment.author to the logged-in member
            # comment.author = Member.objects.first()  # Temporary/
            comment.author = Member.objects.get(name=request.user.name)  # Temporary
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # In a real app, you'd set post.author to the logged-in member
            post.author = Member.objects.get(name=request.user.name)  # Temporary
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'posts/post_form.html', context)

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # In a real app, you'd get the logged-in member
    member = Member.objects.get(name=request.user.name)  # Temporary
    
    like, created = Like.objects.get_or_create(member=member, post=post)
    if not created:
        like.delete()
    
    return redirect('post_detail', pk=post.pk)