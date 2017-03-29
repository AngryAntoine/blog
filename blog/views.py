from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from comments.models import Comment
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm


def blog_home(request):
    today = timezone.now().date()
    object_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        object_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'today': today,
    }
    return render(request, 'posts/home.html', context)


def blog_post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        context = {
            'message': 'You don\'t have administrative rights for creating posts! Get out here, dirty motherfucker!'
        }
        return render(request, 'posts/404.html', context)
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if not request.user == instance.user:
            raise Http404
        instance.save()
        messages.success(request, 'Successfully Created!')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'posts/post_form.html', context)


def blog_post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            return Http404
    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = request.POST.get('parent_id')
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = Comment.objects.filter_by_instance(instance)
    context = {
        'instance': instance,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'posts/post_detail.html', context)


def blog_post_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        context = {
            'message': 'You don\'t have administrative rights for updating posts! Get out here, fucking bastard!'
        }
        return render(request, 'posts/404.html', context)
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Updated!')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'posts/post_update.html', context)


def blog_post_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        context = {
            'message': 'You don\'t have administrative rights for deleting posts! Get out here, fucking bastard!'
        }
        return render(request, 'posts/404.html', context)

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully Deleted!')
    return redirect('blog:blog_home')
