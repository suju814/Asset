from django.db import models
import os
from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


import uuid

class Like(models.Model):
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    po = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='likes_related_name', null = True)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user} Likes {self.po}"
    class Meta:
        ordering = ('-date',)

# class Download(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     po = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='download', null = True)
#     date = models.DateTimeField(default=timezone.now)
#     def __str__(self):
#         return f"{self.user} download {self.po}"
#     class Meta:
#         ordering = ('-date',)

def generate_post_name(instance, filename):
    url = "images/{0}/{1}/{2}".format(
        instance.category1, instance.sub,filename)
    return url
class sample(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return self.category
    def get_absolute_url(self):
        return "/category/" + self.category

    
class Sub(models.Model):
	category1 = models.ForeignKey(sample, on_delete=models.CASCADE)
	sub_category=models.CharField(max_length=50)
	def __str__(self):
		return self.sub_category
    

class File(models.Model):
	file = models.FileField(upload_to="files")
	
	tags = models.CharField(max_length=20, verbose_name="filetags")
	
	filetype = models.CharField(max_length=10, default="File")
	created = models.DateTimeField(auto_now_add=True)
	
	
	def __unicode__(self):
		return os.path.basename(self.file.name),self.filetype
	def filename(self):
		return os.path.basename(self.file.name)
	    # temp = str(file)
	    
class Image(models.Model):
    total_downloads = models.IntegerField(default=0)
   
    image = models.ImageField(upload_to=generate_post_name, width_field = 'image_width', height_field='image_height',null=True,blank=True)
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    tags = models.CharField(max_length=20, verbose_name="imagetags")
    filetype = models.CharField(max_length=10, default="Image")
    created = models.DateTimeField(auto_now_add=True)
    category1 = models.ForeignKey(sample, on_delete=models.SET_NULL, null=True)
    sub = models.ForeignKey(Sub, on_delete=models.SET_NULL, null=True)
    likes = models.IntegerField(default=0)
    discription = models.TextField(max_length=1000)
    # def number_of_likes(self):
    #     return self.likes.count()
    def __unicode__(self):
        return os.path.basename(self.image.name),self.filetype
    def filename(self):
        return os.path.basename(self.image.name)


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    po = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='Download_name', null = True)
    total_downloads = models.IntegerField(default=0)
    
#     def __str__(self):
#         return f"{self.user} downloded this  {self.po}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    po = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='comments', null = True , blank = True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} comments on 's image"
    class Meta:
        ordering = ('-date',)


class BlogComments(models.Model):
    blog_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    like = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # liked_user = models.TextField(default="string")

    def __str__(self):
        return str(self.comments)


class Video(models.Model):
	file = models.FileField(upload_to="videos")
	tags = models.CharField(max_length=20, verbose_name="videotags")
	filetype = models.CharField(max_length=10, default="Video")
	created = models.DateTimeField(auto_now_add=True)
	
	
	def __unicode__(self):
		return os.path.basename(self.file.name),self.filetype
	def filename(self):
		return os.path.basename(self.file.name)

# class sample(models.Model):
# 	category = models.CharField(max_length=50)



class Country(models.Model):
    category = models.CharField(max_length=30)
    def __str__(self):
        return self.category


class City(models.Model):
    category1 = models.ForeignKey(Country, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=30)

    def __str__(self):
        return self.sub_category


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    category1 = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    sub = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# class Comments(models.Model):
# 	post = models.ForeignKey(Image, related_name='details', on_delete=models.CASCADE)
# 	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
# 	comment = models.CharField(max_length=255)
# 	comment_date = models.DateTimeField(default=timezone.now)

# class Like(models.Model):
# 	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
# 	post = models.ForeignKey(Image, related_name='likes', on_delete=models.CASCADE)	





class DownloadStatistic(models.Model):
    """
    Holds the information about how often a certain file was downloaded.

    :download_url: The URL from where the file was downloaded.
    :count: The amount of times this URL was clicked.

    """

    download_url = models.CharField(
        verbose_name=_('Download URL'),
        max_length=512,
    )

    count = models.PositiveIntegerField(
        verbose_name=_('Count'),
        default=1,
    )

    def __unicode__(self):
        return '{} ({})'.format(
            self.download_url[:50] + '...' if len(self.download_url) > 50
            else self.download_url, self.count)