from django.shortcuts import render, redirect,get_object_or_404
from filesapp.models import File,Image,Video,sample,Sub,Country,City,Person,Like,Comments,Download
from filesapp.forms import  ImageUploadModelForm,PersonForm,CommentsForm,SampleForm,SubForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from .forms import ImageForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from django.contrib.auth.models import User
from django.contrib import auth
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


from django.contrib.auth import authenticate,login,logout


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

def logout_request(request):
    logout(request)
    
    return redirect("/")  
def main_home(request):

    if request.method == 'POST':
        user=request.POST['username']
        password=request.POST['password']
        
        user = authenticate(username=user, password=password)
        print(user)
        if user is not None:

            if user.is_active:
                #print(user)
                login(request,user)
                return redirect('filesapp:home')
            else :
                return render(request, 'login.html')
    return render(request,'login.html')
def sample_cat(request,pk):
    
    p=''

    images=Image.objects.filter(sub=pk)
    #images=Image.objects.all()
    cat=sample.objects.all()
    downloads=Download.objects.all()
    print(images)
    print("---------------------------")
    print(downloads)
    # for each in images:
    #     print(each.filename)
    return render(request,'filesapp/image_list2.html',{'images':images,'cat':cat,'downloads':downloads,'p':p}) 

def sa(request, slug):
    print(slug)
    print('sai')
    ss=sample.objects.get(category=slug)
    p=Sub.objects.filter(category1=ss)

    images=Image.objects.filter(category1=ss)
    #images=Image.objects.all()
    cat=sample.objects.all()
    downloads=Download.objects.all()
    print(images)
    print("---------------------------")
    print(downloads)
    # for each in images:
    #     print(each.filename)
    dep=slug
    return render(request,'filesapp/image_list2.html',{'images':images,'cat':cat,'downloads':downloads,'p':p,'dep':dep}) 


def home(request):
    images=Image.objects.all()
    cat=sample.objects.all()
    downloads=Download.objects.all()
    print(images)
    print("---------------------------")
    print(downloads)
    # for each in images:
    #     print(each.filename)
    dep=''
    return render(request,'filesapp/image_list2.html',{'images':images,'cat':cat,'downloads':downloads,'dep':dep}) 

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
    # print(">>>>>>>>>>>>>>>>>viewdeatails>>>>>>>>>>>>>>")
    topic = get_object_or_404(Image,pk=pk)
    
   
    # print(topic.comments.all(),">>>>>>>>>>>>>>>>----------------------")
    download = Download.objects.filter(user=request.user)
    # print(download)
    # download = get_object_or_404(Download,pk=pk)
    # download = Download.objects.all()
    download = Download.objects.filter(user=request.user,po=topic)
    # print(User,"useeeeeeeeeeeeeeeeeeeeeeee")
    # if request.user==User:
    #     download = Download.objects.filter(user=request.user,po=topic)
    # else:
    #     print("hellllllllllllllllllllllll")    
    # for download in download:
    #     print(download.user,download.total_downloads,download.po,">>>>>>>>>>>>>")
    # print(download[4].total_downloads,download[4].user,"Dddddddddddddddddddddddd")
    print(topic,download)
    print(topic,pk)
    types=topic.filetype
    sap=topic.image.url
    saps=sap.split('.')[-1]
    form=CommentsForm()
    related=Image.objects.filter(category1=topic.category1).exclude(pk=pk)[:10]
    
    cat=sample.objects.all()
    
    
    return render(request, 'filesapp/topic.html', {'topic': topic,'form':form,'ids':pk,'type':saps,'download':download,'related':related,'cat':cat})

def user_list(request):
    s=Download.objects.all()
    t_d=0
    t_dl=[]
    for i in s:
        t_d=t_d+i.total_downloads
        t_dl.append(t_d)
    try:
        dow=t_dl[-1]
    except:
        dow=0
    users=User.objects.all().count()
    image=Image.objects.all().count()
    cat=sample.objects.all().count()
    subcat=Sub.objects.all().count()
   
    catss=sample.objects.all()
    

    return render(request,'filesapp/down_user.html',{'s':s,'dow':dow,'userss':users,'image':image,'cate':cat,'subcat':subcat,'cat':catss})

def LikeAndDislikeView(request,pk):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    post = get_object_or_404(Image, id=pk)
  
    
    liker = Like.objects.filter(po=post, user=request.user)
   
    
    
    if liker :
        likess=Like.objects.get(po=post,user=request.user)
        print(likess.likes)
        if likess.likes == 1:
        # if likes==1
            post.likes -=1
            post.save()
            liker.delete()    
        
    else:
         like=Like(po=post,user=request.user,likes=1)
         like.save()
         post.likes +=1
         post.save()

    return redirect('filesapp:main')
    
    
def AddCommentView(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Image, id=pk)
        form = CommentsForm(request.POST)
        if form.is_valid():
            post_comment = form.cleaned_data.get('post_comment')
            comments = Comments(
                user=request.user,
                comment = post_comment,
                po = post
            )
            comments.save()      
            return redirect('filesapp:main') 

def count_downloads(req):
    if req.method == "GET":
        pk = req.GET.get("obj")
        obj = Image.objects.get(pk=pk)
        obj.total_downloads += 1
        obj.save()

        print("inside save view")

    return JsonResponse({'status': obj.total_downloads})

    





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
    
    success_url = reverse_lazy('filesapp:person_changelist')

def forms(request):
    form=ImageForm()
    cat=SampleForm()
    subcat=SubForm()
    return render(request,'filesapp/image_form.html',{'form':form,'category':cat,'subcategory':subcat})


class CategoryUpdateView(UpdateView):
   
    model = Image
    form_class = ImageForm
    
    success_url = reverse_lazy('filesapp:person_changelist')



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
