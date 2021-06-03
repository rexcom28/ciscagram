import json
from django.shortcuts import render,redirect, reverse
from .models import Category, Post, Doc
from conversation.models import postMessage
from django.http import JsonResponse, HttpResponse
from .forms import PostForm, CategoryForm,PostCategoryForm
from profiles.models import Profile
from django.contrib.auth.models import User
from .utils import action_permission
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import re
from notification.utilities import create_notification
from django.contrib import messages

class MainView(TemplateView):
    template_name = 'posts/main2.html'

def file_upload_view(request):
    #print(request.FILES)
    if request.method =='POST':
        my_file = request.FILES.get('file')
        Doc.objects.create(upload=my_file)

        return HttpResponse('')
    return JsonResponse({'post': 'false'})

@login_required
def image_upload_view(request,pk=None):
    

    if request.method == 'POST':
        img = request.FILES.get('file' or None)
        new_post_id = request.POST.get('new_post_id')
        if img is not None:
            
            post = Post.objects.get(id=new_post_id)
            Doc.objects.create(photo_id=post, upload=img )
        
    return HttpResponse()
    
@login_required
def post_list_and_create(request):
    print('post_list_and_create')
    form = PostForm(request.POST or None)
    
    if request.is_ajax(): 
        if form.is_valid():
            author = User.objects.get(username=request.user.username)
            instance = form.save(commit=False)
            instance.author = author   
            print('request.POST.get("visible")  ',request.POST.get('visible')) 
            instance.visible = True if request.POST.get('visible') =='true' else False
            instance.save()
            results = re.findall("(^|[^@\w])@(\w{1,20})",instance.body)
            for result in results:
                result = result[1]
                if User.objects.filter(username = result).exists() and result != request.user.username:
                    
                    create_notification(request, User.objects.get(username=result), 'mention', instance)
            return JsonResponse({
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.username,
                'id': instance.id,
            })
        
    context = {
        'form': form,
    }

    return render(request, 'posts/main.html', context)

@login_required
def post_detail(request, pk):
    
    obj = Post.objects.get(pk=pk)
    form = PostForm()
    messages_post = postMessage.objects.filter(message_post_id__in=[obj.pk]) 
    if messages_post is None :
        messages_post = {}
    context = {
        'obj': obj,
        'form': form,
        'messages_post':messages_post
    }

    return render(request, 'posts/detail.html', context)
    
@login_required
def load_post_data_view(request, num_posts):
    print('load_post_data_view      request.is_ajax()', request.is_ajax(),'  num_posts ',num_posts)
    if request.is_ajax():
        

        visible = 3                
        upper = num_posts 
        lower = upper - visible 
        size = Post.objects.all().filter(visible=True).count()        
        qs = Post.objects.all().filter(visible=True)

        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'liked': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                #'author': obj.author.user.username
                'author': obj.author.username
            }
            data.append(item)
        return JsonResponse({'data':data[lower:upper], 'size': size})

@login_required
def post_detail_data_view(request, pk):
    print('post_detail_data_view')
    if request.is_ajax():
        
        obj = Post.objects.get(pk=pk)
        print('obj.visible   ',obj.visible)
        data = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            'author': obj.author.username,
            'avatar': obj.author.profile.avatar.url,
            'logged_in': request.user.username,
            'category': obj.category.id,
            'visible': obj.visible
        }
        return JsonResponse({'data': data})
    return redirect('posts:main-board')

@login_required
def like_unlike_post(request):
    
    if request.is_ajax():
        pk = request.POST.get('pk')

        #print(type(pk), '   ',pk, '         ',request.is_ajax())
        if pk == None:
            data = json.loads(request.body)
            pk = data['pk']
            obj = Post.objects.get(id=pk)
        else:
            obj = Post.objects.get(id=pk)
       

        
        print(obj)
        #body = data['body']
        
        if request.user in obj.liked.all():
            liked = False
            obj.liked.remove(request.user)
        else:
            liked = True
            obj.liked.add(request.user)
            

            to_user = User.objects.get(username=obj.author)
            
            if str(request.user) != str(to_user.username):                
                create_notification(request, to_user, 'like', obj)

        return JsonResponse({'liked': liked, 'count': obj.like_count})
    return redirect('posts:main-board')

@login_required
@action_permission
def update_post(request, pk):
    print('update_post---- request.is_ajax()',request.is_ajax())
    obj = Post.objects.get(id=pk)
    
    if request.is_ajax():
        new_title    = request.POST.get('title')
        new_body     = request.POST.get('body')
        new_category = request.POST.get('category')
        #new_category = Category.objects.get(title=new_category)
        visible      = True if request.POST.get('visible')=='true' else False
        print('visible  ',request.POST.get('visible'),'  ',new_category)
        obj.title = new_title
        obj.body = new_body
        #obj.category = new_category
        obj.visible = visible
        obj.save()
        results = re.findall("(^|[^@\w])@(\w{1,20})",obj.body)
        for result in results:
            result = result[1]
            if User.objects.filter(username = result).exists() and result != request.user.username:
                create_notification(request, User.objects.get(username=result), 'mention', obj)
        return JsonResponse({
            'title': new_title,
            'body': new_body,
            'id':obj.id,
            'category':obj.category.id,
            'visible':obj.visible

        })
    return redirect('posts:main-board')

@login_required
@action_permission
def delete_post(request, pk):
    obj = Post.objects.get(id=pk)
    if request.is_ajax():
        obj.delete()
        return JsonResponse({'msg':'some message'})
    return redirect('posts:main-board')



def unpa(**kwargs):
    
    qs = ''
    check   = kwargs['check'][0]    
    val     = kwargs['val'][0]
    author  = kwargs['author'][0]
    
    if check =='false':
        if author=='true':
            #qs = Post.objects.filter(author__user__username__icontains=val, visible=True) 
            qs = Post.objects.filter(author__username__icontains=val, visible=True) 
        else:
            qs = Post.objects.filter(title__icontains=val, visible=True) 
    else:
        if author=='true':
            qs = Post.objects.filter(author__username__icontains=val)
        else:
            qs = Post.objects.filter(title__icontains=val) 
    
    return qs,val

def search_results(request):
    if request.is_ajax():
        res = None
        qs,val = unpa(**request.POST)        
        if len(qs)> 0 and len(val)> 0:
            data=[]
            for pos in qs:

                item = {
                    'pk': pos.pk,
                    'title': pos.title,
                    'body': pos.body,
                    'image': [i.upload.url for i in pos.photo_set.all()[0:1]],
                    'author': pos.author.username
                }
                data.append(item)
            res = data
        else:
            res='No Posts Found...'

        return JsonResponse({'data':res})
    return JsonResponse({})

@login_required
def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'posts/Categories.html', context)

@login_required
def category_Add(request):
    print(request.method)
    if request.method == 'POST':
        #form = CategoryForm(request.POST)
        form = CategoryForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            
            category.save()

            #messages.success(request, 'The category has been added!')

            return redirect('posts:category', category=category.title)
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/CategoriesAdd.html', context)

@login_required
def category(request, category):
    
    
    if request.is_ajax():
        form = PostCategoryForm(request.POST or None)
        if form.is_valid():
            author = User.objects.get(username=request.user.username)
            instance = form.save(commit=False)
            instance.author = author        
            instance.save()
            results = re.findall("(^|[^@\w])@(\w{1,20})",instance.body)
            for result in results:
                result = result[1]
                if User.objects.filter(username = result).exists() and result != request.user.username:
                    
                    create_notification(request, User.objects.get(username=result), 'mention', instance)
            return JsonResponse({
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.username,
                'id': instance.id,
            })
    else:
        
        posts = Post.objects.filter(category__title__in=[category])
        category_id = Category.objects.get(title=category)
        
        form = PostCategoryForm(request.POST or None)    
    

    context={
        'posts':posts,
        'CATEGORY':category_id,
        'CATEGORY_ID':category_id.id,
        'form':form
    }
    return render(request, 'posts/Category.html', context)

@login_required
def categoryEdit(request, category):
    print(request.method)
    if request.method =='GET':
        cat = Category.objects.get(title=category)
        form = CategoryForm(instance=cat)
    else:    
        cat = Category.objects.get(title=category)
        form = CategoryForm(request.POST or None, request.FILES or None, instance=cat)
        
        if form.is_valid():
            instance = form.save(commit=False)
            print(instance.upload)
            instance.save()
            return redirect('posts:category', category=instance.title)
    

    context = {
        'form':form,
        'category':category
    }
    return render(request, 'posts/CategoryEdit.html', context)
