from django import forms


class CreatePosts(forms.Form):
    thepost = forms.CharField(label="Post", widget=forms.Textarea 
    (attrs={'class':'inputs', 'id':'input1', 'placeholder': 'Post something...'}))

class PostImage(forms.Form):
    thepic = forms.URLField(max_length=599, label="Image URL", required=False, widget=forms.URLInput 
    (attrs={'class':'inputs', 'id':'input2'}))