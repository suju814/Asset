from django.urls import re_path, path
from filesapp import views
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

from django.conf.urls import url
from django.conf.urls.static import static
from filesproject import settings
from django.views.generic import TemplateView
# from .views import PostUpdateView, PostListView, UserPostListView



# namespace
app_name = "filesapp"

urlpatterns = [

    
path('admin/', admin.site.urls),
    # Upload Files Using Model Form
    re_path(r'^uploadfile/$', views.model_form_upload, name='model_form_upload'),
    re_path(r'^uploadimage/$', views.image_form_upload, name='image_form_upload'),
    re_path(r'^uploadvideo/$', views.video_form_upload, name='video_form_upload'),

   path('sample_image', views.sample_image, name='person_changelist'),
    path('add/', views.CategoryCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.CategoryUpdateView.as_view(), name='person_change'),
    path('subcategory/<int:pk>/', views.sample_cat, name='sample_cat'),
    path('ajax/load-cities/', views.sample_data, name='sample_data'),
    path('category/<str:slug>/', views.sa,name='sa'),

    # path('', views.PersonListView.as_view(), name='person_changelist'),
    # path('add/', views.PersonCreateView.as_view(), name='person_add'),
    # path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    # path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),



   # path('main', views.main_home, name='main'),
     path('images', views.checking, name='checking'),
     # path('sample', views.sample_data, name='sample_data'),
    path('home', views.home, name='home'),  
    path('videos', views.home1, name='home1'),
    path('files',views.home2,name='home2'),
    url(r'view_details/(?P<pk>\d+)/$', views.view_details, name='view_details'),
    url(r'view_details_video/(?P<pk>\d+)/$', views.view_details_video, name='view_details_video'),
    url(r'view_details_file/(?P<pk>\d+)/$', views.view_details_file, name='view_details_file'),

    path('search_file', views.search_file, name='search_file'),
  path("logout", views.logout_request, name="logout"),
  path('user_list',views.user_list,name="user_list"),

  
  # path('file/', include("file_download.urls")),

# path('', PostListView.as_view(), name='home'),
#     path('post/new/', views.create_post, name='post-create'),
#     path('post/<int:pk>/', views.post_detail, name='post-detail'),
#     path('like/', views.like, name='post-like'),
#     path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
#     path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
 
#     path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),

  path('', views.main_home, name='main'),
  #   path('blogpost-like/<int:pk>', views.BlogPostLike, name="BlogPostLike"),
    
   # path('',views.IndexView.as_view(), name='index'),
    # path('post/<str:pk>/comment/', views.AddCommentView , name='comment'),
     #url(r'view_details_file/(?P<pk>\d+)/$', views.LikeAndDislikeView , name='like'),
     path('post/<pk>/like/', views.LikeAndDislikeView , name='like'),
      path('post/<pk>/comment/', views.AddCommentView , name='comment'),
      # path('blog-comments/<int:blog_id>/<str:comment>', views.save_comment, name='blog-comment'),
     


] 




if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)