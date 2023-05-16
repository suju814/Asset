from django.shortcuts import render, redirect,get_object_or_404
from filesapp.models import File,Image,Video,sample,Sub,Country,City,Person,Post,Like,BlogPost
from filesapp.forms import  ImageUploadModelForm,PersonForm,NewCommentForm,NewPostForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from .forms import ImageForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
import uuid
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.template.defaultfilters import filesizeformat
from django.db.models import Q
from moviepy.editor import VideoFileClip

import os

from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import View
from django.utils.encoding import smart_str
from .models import DownloadStatistic


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

class BlogPostDetailView(DetailView):
    print(">>>>>>>>>>>>>>>>blog>>>>>>>>>>>>>>>>>>>>>")
    model = BlogPost
    # template_name = MainApp/BlogPost_detail.html
    # context_object_name = 'object'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(BlogPost, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

def BlogPostLike(request, pk):
    print(BlogPost.objects.all())
    print(">>>>>>>>>>>>>>>>>>>LIKE>>>>>>>>>>>>>>>>")
    post = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
    print(">>>>>>>",post)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(topic.html, pk=pk)

def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user== post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect('home')

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user = self.request.user, post=i)]
        context['liked_post'] = liked
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user_name=user).order_by('-date_posted')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description', 'pic', 'tags']
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_name:
            return True
        return False

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
            context['liked_post'] = liked
        return context
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked= False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(user=user, post=post)
    resp = {
        'liked':liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")

def create_post(request):
    user = request.user
    if request.method == "POST":

        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request, f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'create_post.html', {'form':form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked =  Like.objects.filter(user=user, post=post)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'post_detail.html', {'post':post, 'is_liked':is_liked, 'form':form})






class DownloadView(View):
    """View that increments download counts and serves the files."""
    def dispatch(self, request, *args, **kwargs):
        self.requested_file = kwargs.get('requested_file')
        self.file_name = os.path.basename(self.requested_file)
        self.full_file_path = os.path.join(settings.MEDIA_ROOT,
                                           self.requested_file)
        if not self.requested_file or not os.path.exists(self.full_file_path):
            raise Http404

        return super(DownloadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        with open(self.full_file_path) as f:
            response = HttpResponse(content=f.read(),
                                    content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            smart_str(self.file_name))
        # the usual case is that there is already at least one download of a
        # file, so only on creation we would trigger an additional query
        if not DownloadStatistic.objects.filter(
                download_url=self.full_file_path).update(count=F('count')+1):
            DownloadStatistic.objects.create(download_url=self.full_file_path)
        return response


def main_home(request):
    return render(request,'filesapp/base.html')


def home(request):
    # images=Image.objects.all()
    # for each in images:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    return render(request,'image.html')

def home1(request):
    images=Video.objects.all()
    # for each in images:
    #     print(each.filename)
    return render(request,'video.html',{'images':images})
def home2(request):
    images=File.objects.all()
    # for each in images:
    #     print(each.filename)
    return render(request,'file.html',{'images':images})
    
def view_details(request,pk):
    print(">>>>>>>>>>>>>>>>>viewdeatails>>>>>>>>>>>>>>")
    topic = get_object_or_404(Image,pk=pk)
    types=topic.filetype
    sap=topic.image.url
    saps=sap.split('.')[-1]
    
    # if types=="Video":
    #     clip = VideoFileClip(r"C:\Users\TNLUSER\Downloads\django-file-upload-download-master\django-file-upload-download-master\{}".format(sap))
    #     dep=clip.duration
       
    #     return render(request, 'topic.html', {'topic': topic,'durations':dep})
    

    return render(request, 'filesapp/topic.html', {'topic': topic,'type':saps})

def view_details_video(request,pk):
    topic = get_object_or_404(Video,pk=pk)
    types=topic.filetype
    sap=topic.file.url
    saps=sap.split('.')[-1]
    
    if types=="Video":
        clip = VideoFileClip(r"C:\Users\Tnluser.5CG92394Q7\Downloads\django-file-upload-download-master\{}".format(sap))
        dep=clip.duration
       
        return render(request, 'topic_video.html', {'topic': topic,'durations':dep})
    

    return render(request, 'topic_video.html', {'topic': topic,'type':saps})
def view_details_file(request,pk):
    topic = get_object_or_404(File,pk=pk)
    print(topic)
    types=topic.filetype
    sap=topic.file.url
    saps=sap.split('.')[-1]
    
    if types=="Video":
        clip = VideoFileClip(r"C:\Users\TNLUSER\Downloads\django-file-upload-download-master\django-file-upload-download-master\{}".format(sap))
        dep=clip.duration
       
        return render(request, 'topic_file.html', {'topic': topic,'durations':dep})
    

    return render(request, 'topic_file.html', {'topic': topic,'type':saps})

    
def view_details_video(request,pk):
    topic = get_object_or_404(Video,pk=pk)
    print(topic)
    types=topic.filetype
    sap=topic.file.url
    saps=sap.split('.')[-1]
    
    if types=="Video":
        clip = VideoFileClip(r"D:\django-file-upload-download-master\{}".format(sap))
        dep=clip.duration
       
        return render(request, 'topic_video.html', {'topic': topic,'durations':dep})
    

    return render(request, 'topic_video.html', {'topic': topic,'type':saps})
def view_details_file(request,pk):
    topic = get_object_or_404(File,pk=pk)
    print(topic)
    types=topic.filetype
    sap=topic.file.url
    saps=sap.split('.')[-1]
    
    if types=="Video":
        clip = VideoFileClip(r"C:\Users\TNLUSER\Downloads\django-file-upload-download-master\django-file-upload-download-master\{}".format(sap))
        dep=clip.duration
       
        return render(request, 'topic_file.html', {'topic': topic,'durations':dep})
    

    return render(request, 'topic_file.html', {'topic': topic,'type':saps})
# Show file list   
# Show file list
def search_file(request):
    if request.method == 'GET':
        pro = request.GET['search']
        data={}
        data['images'] = File.objects.filter(Q(file__istartswith=pro)|Q(file__iexact=pro)|Q(file__icontains=pro)|Q(tags__istartswith=pro)|Q(tags__iexact=pro)|Q(tags__icontains=pro))
        
        
        
        
    return render(request,'home.html',data)

def file_list(request):
    files = Image.objects.all().order_by("-id")
    filess = Image.objects.all().count()
    filess = Image.objects.values('image')
    
    return render(request, 'filesapp/file_list.html', {'files': files,'filess':filess})



def handle_uploaded_file(file):
    file_name = file.name
   
    # file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


# Upload File with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            return redirect("file_upload:home2")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload Files '})
def image_form_upload(request):
    if request.method == "POST":
        form = ImageUploadModelForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            return redirect("home")
    else:
        form = ImageUploadModelForm()

    return render(request, 'upload_image_form.html', {'form': form,
                                                            'heading': 'Upload Images '})


def file_download(request, file_path):
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)





def video_form_upload(request):
    if request.method == "POST":
        form = VideoUploadModelForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            return redirect("file_upload:home1")
    else:
        form = VideoUploadModelForm()

    return render(request, 'file_upload/upload_video_form.html', {'form': form,
                                                            'heading': 'Upload Videos'})





# def sample_data(request):

#     userlist=sample.objects.all()
#     sub_userlist=sub_category.objects.all()
#     print(userlist)
#     print(sub_userlist)
#     category_id = request.GET.get('category')
#     sub_userlist = sub_category.objects.filter(category_id=category_id).order_by('sub_category')
#     print(sub_userlist)
#     location = sub_category.objects.filter(sub_category=sub_category)
#     print(location)
#     return render(request,'file_upload/base.html',{'userlist': userlist,'sub_userlist':sub_userlist})

def sample_data(request):
    print("-------------------------------------------")
    category1_id = request.GET.get('category1')
    cities = Sub.objects.filter(category1_id=category1_id).order_by('sub_category')
    print(cities)
    return render(request, 'filesapp/city_dropdown_list_options.html', {'cities': cities})





class CategoryListView(ListView):
    model = Image
    context_object_name = 'people'


class CategoryCreateView(CreateView):
    model = Image
    form_class = ImageForm
    
    success_url = reverse_lazy('person_changelist')


class CategoryUpdateView(UpdateView):
   
    model = Image
    form_class = ImageForm
    
    success_url = reverse_lazy('person_changelist')



def sample_image(request):
    images=Image.objects.all()
    for each in images:
        print(each.filename)
    return render(request,'filesapp/image_list.html',{'images':images})



def checking(request):

    images=Image.objects.all()
    for each in images:
        print(each.filename)
    return render(request,'filesapp/image_list.html',{'images':images})    
# def sample_image(request):
    
#     # files=os.listdir(r'D:\filesupload\filesproject\media\images\posts\3d\3d1')
#     # print(files)
#     # for files in files:
#     #     print(files)
#     filess = Image.objects.values('image')
#     # print(filess[0])
#     # for i in filess:
#     #     print(">>>>>>>>>>>>>>>>>>>>>>",filess[0]['image'])
#     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",filess[0]['image'])

#     # images=Image.objects.values()
   
#     # for images in images:
#     #     print(images['image'])
#     print(">",filess)
#     list=[]
#     print(">>",filess[0])
#     for i in filess:
#         image=i['image']
        
        

#         # return render(request, 'filesapp/image_list.html', {'filess':filess[i]})     
    
#         print(">>>>>",image)
    # return render(request, 'filesapp/image_list.html',{'filess':filess})  




class PersonListView(ListView):
    model = Person
    context_object_name = 'people'
    


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')



def load_cities(request):
    print("-------------------------------------------")

    category1_id = request.GET.get('category1')
    cities = City.objects.filter(category1_id=category1_id).order_by('sub_category')
    return render(request, 'filesapp/city_dropdown_list_options.html', {'cities': cities})
