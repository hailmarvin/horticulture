from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog, News, Profile, Comment, Gallery
from django.http import HttpResponse, HttpRequest
from itertools import chain

# Create your views here.
@login_required(login_url='/auth')
def index(request):
    if request.user.is_authenticated and not request.user.is_staff :
        user_profile = Profile.objects.get(user=request.user)
        return render(request, 'index.html', {'user_profile': user_profile})
    elif request.user.is_staff:
        user_profile = request.user
        return render(request, 'index.html', {'user_profile': user_profile})    
    else:
        return render(request, 'index.html')

def authentication(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if 'email' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('/auth')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('/auth')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    #log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    #create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('/')
            else:
                messages.info(request, 'Password not Matching')
                return redirect('/auth')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Wrong username or password!')
            return redirect('/auth')

    else:
        return render(request, 'auth.html')

@login_required(login_url='/auth')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='/auth')
def del_user(request, pk):    
    try:
        u = User.objects.get(id = pk)
        if u.is_staff is not True:
            u.delete()
            messages.success(request, "User account deleted")  
            return render(request, 'auth.html')          
        else:
            messages.info(request, "You cannot delete an admin account")  
            return render(request, 'auth.html')

    except Exception as e: 
        return render(request, 'auth.html',{'err':e.message})

@login_required(login_url='/auth')
def change(request: HttpRequest, user_id: str) -> HttpResponse:
    user_profile = Profile.objects.get(id=user_id)
    user_profile.is_employee = not user_profile.is_employee
    user_profile.save()
    return index(request)

@login_required(login_url='/auth')
def blog(request):
    blogs = Blog.objects.all().order_by('-id')

    if request.user.is_authenticated:
        if not request.user.is_staff:
            user_profile = Profile.objects.get(user=request.user)
            return render(request, 'blog.html', {'blogs': blogs, 'user_profile': user_profile})
        else:
            user_profile= request.user
            return render(request, 'blog.html', {'blogs': blogs, 'user_profile': user_profile})

    else:
         return render(request, 'blog.html', {'blogs': blogs})       

@login_required(login_url='/auth')
def blog_profile(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.filter(blog=blog)

    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'blog_profile.html', {'blog': blog, 'admin': True, 'comments': comments})

        
        user_profile = Profile.objects.get(user=request.user)
        str_user = str(user_profile)

        if request.method == "POST":
            comment = request.POST['comment']

            Comment.objects.create(
                comment = comment,
                user = request.user,
                blog = blog
            )
            return render(request, 'blog_profile.html', {'blog': blog, 'user_profile': user_profile, 'str_user': str_user, 'comments': comments})

        return render(request, 'blog_profile.html', {'blog': blog, 'user_profile': user_profile, 'str_user': str_user, 'comments': comments})

    else:
        return render(request, 'blog_profile.html', {'blog': blog,'comments': comments})

@login_required(login_url='/signin')
def update_blog(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    blog = Blog.objects.get(id=pk)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = blog.image
            title = request.POST['title']
            info = request.POST['info']

            blog.title = title
            blog.image = image
            blog.info = info
            blog.is_edited = True
            blog.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            title = request.POST['title']
            info = request.POST['info']

            blog.title = title
            blog.profile_img = image
            blog.info = info
            blog.is_edited = True
            blog.save()
        messages.info(request, "Update Successful") 
        return redirect(f'/blogs/{blog.id}')    

    return render(request, 'update_blog.html', {'user_profile': user_profile, 'blog': blog})

@login_required(login_url='/auth')
def upload_blog(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        title = request.POST['title']
        info = request.POST['info']
        image = request.FILES.get('image')

        user = request.user.username

        blog = Blog.objects.create(
            user=user,
            title=title,
            info=info,
            image=image
        )
        
        blog.save()

        messages.info(request, "Upload Successful")
        return redirect('/blogs')

    return render(request, 'blog_upload.html', {'user_profile': user_profile})

@login_required(login_url='/auth')
def delete_blog(request,pk):
    user_profile = request.user
    blog_to_delete=Blog.objects.get(id=pk)
    str_user = str(user_profile)

    if blog_to_delete.user == str_user:
        blog_to_delete.delete()
        messages.info(request, "Blog deleted")
        return redirect('/')
    else:
        return redirect('/')

def news(request):
    news = News.objects.all().order_by('-id')

    if request.user.is_authenticated:
        if not request.user.is_staff:
            user_profile = Profile.objects.get(user=request.user)
            return render(request, 'news.html', {'news': news, 'user_profile': user_profile})
        else:
            user_profile= request.user
            return render(request, 'news.html', {'news': news, 'user_profile': user_profile})
    else:
        return render(request, 'news.html', {'news': news})

@login_required(login_url='/auth')
def news_profile(request, pk):
    news = News.objects.get(id=pk)
    
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        return render(request, 'news_profile.html', {'news': news, 'user_profile': user_profile})
    else:
        return render(request, 'news_profile.html', {'news': news, })

@login_required(login_url='/auth')
def upload_news(request):
    user_profile = Profile.objects.get(user=request.user)

    if user_profile.is_employee == True:
        if request.method == "POST":
            title = request.POST['title']
            info = request.POST['info']
            image = request.FILES.get('image')

            user = request.user.username

            news = News.objects.create(
                title=title,
                info=info,
                image=image
            )
            
            news.save()

            messages.info(request, "Upload Successful")
            return redirect('/')

    else:
        messages.info(request, "You are not authenticated to view that page")
        return redirect('/')

    return render(request, 'news_upload.html', {'user_profile': user_profile})

@login_required(login_url='/auth')
def update_news(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    news = News.objects.get(id=pk)

    if user_profile.is_employee == True:

        if request.method == 'POST':

            if request.FILES.get('image') == None:
                image = news.image
                title = request.POST['title']
                info = request.POST['info']

                news.title = title
                news.image = image
                news.info = info
                news.is_edited = True
                news.save()
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                title = request.POST['title']
                info = request.POST['info']

                news.title = title
                news.profile_img = image
                news.info = info
                news.is_edited = True
                news.save()
            messages.info(request, "Update Successful")
            return redirect(f'/news/{news.id}')    

        return render(request, 'update_news.html', {'user_profile': user_profile, 'news': news})
    else:
        messages.info(request, "You are not authenticated to view that page")
        return redirect('index')

@login_required(login_url='/auth')
def delete_news(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    news_to_delete=News.objects.get(id=pk)

    if user_profile.is_employee == True:
        news_to_delete.delete()
        messages.info(request, "News deleted")
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/auth')
def dashboard(request):
    if request.user.is_staff:
        users = Profile.objects.all().order_by('-id')
        return render(request, 'admin_dashboard.html', {'users': users })
    else:
        user_profile = Profile.objects.get(user=request.user)
        str_user= str(user_profile)
        user_blogs = Blog.objects.filter(user=str_user)
        return render(request, 'dashboard.html', {'user_profile': user_profile, 'user_blogs': user_blogs})

@login_required(login_url='/auth')
def gallery(request):
    galleries = Gallery.objects.order_by('-id')
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        return render(request, 'gallery.html', {'user_profile': user_profile, 'galleries': galleries})
    else:
        return render(request, 'gallery.html', {'galleries': galleries})

def upload_gallery(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        media = request.FILES.get('media')
        title = request.POST['title']
        is_video = request.POST['mediatype']

        if is_video == 'video':
            Gallery.objects.create(
                title = title,
                media = media,
                is_video = True
            )
        else:
            Gallery.objects.create(
                title = title,
                media = media
            )
        messages.info(request, "Upload SUccessful")
        return redirect('/gallery')
    else:
        return render(request, 'upload_gallery.html', {'user_profile': user_profile})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        blog_titles_object = Blog.objects.filter(title__icontains=search)
        news_titles_object = News.objects.filter(title__icontains=search)

        blogs = []
        news_list = []
        total_list = []

        for blog in blog_titles_object:
            blogs.append(blog.id)

        for news in news_titles_object:
            news_list.append(news.id)

        for ids in blogs:
            blog_lists = Blog.objects.filter(id=ids)
            total_list.append(blog_lists)

        for ids in news_list:
            news_lists = News.objects.filter(id=ids)
            total_list.append(news_lists)

        combined_list = list(chain(*total_list))


    return render(request, 'search.html', { 'combined_list': combined_list})

@login_required(login_url='/auth')
def signout(request):
    auth.logout(request)
    return redirect('/auth')