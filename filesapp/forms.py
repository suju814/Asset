from django import forms
from .models import File,Image,Video,Sub, Person, City,Country,Comments,sample



class CommentsForm(forms.Form):
        post_comment = forms.CharField(max_length=100 , widget=forms.TextInput(attrs={
            'class':'form-control',
            'border':'none',
            'background':'transparent',
            'outline':'none',
            'placeholder':'add comment',

        }))


class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'tags')
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
         }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        
        return file

class ImageUploadModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'tags','category1','sub')
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'category1': forms.Select(attrs={'class': 'form-control'}),
            'sub': forms.Select(attrs={'class': 'form-control'}),
            
            }

    def clean_file(self):
        image = self.cleaned_data['image']
        ext = image.name.split('.')[-1].lower()
        
        return image

class VideoUploadModelForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('file', 'tags')
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        
        return file



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'tags', 'category1', 'sub')
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category1': forms.Select(attrs={'class': 'form-control'}),
            'sub': forms.Select(attrs={'class': 'form-control'}),
            
            }
        def clean_file(self):
            image = self.cleaned_data['image']
            ext = image.name.split('.')[-1].lower()
            
            return image 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub'].queryset = Sub.objects.none()

        if 'category1' in self.data:
            try:
                category1_id = int(self.data.get('category1'))
                self.fields['sub'].queryset = Sub.objects.filter(category1_id=category1_id).order_by('sub_category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub'].queryset = self.instance.category1.sub_set.order_by('sub_category')

class SubForm(forms.ModelForm):
    class Meta:
        model = Sub
        fields = ['category1','sub_category']
        widgets = {
            'sub_category': forms.TextInput(attrs={'class': 'form-control'}),
            'category1': forms.Select(attrs={'class': 'form-control'}),
            
            
            
            }
class SampleForm(forms.ModelForm):
    class Meta:
        model = sample
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            
            
            
            }
        

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'category1', 'sub')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub'].queryset = City.objects.none()

        if 'category1' in self.data:
            try:
                category1_id = int(self.data.get('category1'))
                self.fields['sub'].queryset = City.objects.filter(category1_id=category1_id).order_by('sub_category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub'].queryset = self.instance.category1.city_set.order_by('sub_category')
