import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from django.contrib.auth.models import User
from filesapp.models import Download,Image
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse






def file_download(request, file_path):
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)


def media_file_download(request, file_path):
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404



def stream_http_download(request, file_path):
    try:
        response = StreamingHttpResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404

def file_response_download1(request, file_path):
    print(pk)

    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


def file_response_download(request, file_path,pk):
    post = get_object_or_404(Image, id=pk)
    print(post)
  

    liker = Download.objects.filter(po=post, user=request.user)
    print("liker",liker)
    if liker:
        likess=Download.objects.get(po=post, user=request.user)
        post.total_downloads +=1
        post.save()
        likess.total_downloads +=1
        likess.save()
    else:
        post.total_downloads +=1
        post.save()
        like = Download(
        user=request.user,
        po=post,total_downloads=1,
        )
        like.save()
        
       
    ext = os.path.basename(file_path).split('.')[-1].lower()
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        raise Http404

