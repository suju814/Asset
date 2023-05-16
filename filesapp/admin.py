from django.contrib import admin
from .models import File,Image,Video,Sub,sample,Country,City,Person,Like,Comments,Download
# Register your models here.,Countrt,SC

admin.site.register(File)
admin.site.register(Image)    
admin.site.register(Video) 	
admin.site.register(sample) 
admin.site.register(Sub)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Person)
# admin.site.register(BlogComments)
admin.site.register(Like)
admin.site.register(Comments)
admin.site.register(Download)


