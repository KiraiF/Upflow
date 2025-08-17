from django import forms
from .models import Post, Community
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'community', 'body']
    community = forms.ModelChoiceField(
    queryset=Community.objects.all(),
    required=True,
    empty_label="-- Select a community --"
    )
class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
class CleanUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help texts
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        # Optional: clean up labels too
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']