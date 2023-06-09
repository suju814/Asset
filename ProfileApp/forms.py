class SignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-1','placeholder':'email'}))
    first_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class':'input-1','placeholder':'first name'}))
    last_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class':'input-1','placeholder':'last name'}))
    username = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class':'input-1','placeholder':'username'}))
    password = forms.CharField(max_length=70, widget=forms.PasswordInput(attrs={'class':'input-1','placeholder':'password'}))
    class Meta:
        model= User
        fields = ['email','first_name','last_name','username','password']