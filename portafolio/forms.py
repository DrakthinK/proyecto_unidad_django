
from django import forms
class ProyectoForm(forms.Form):
    foto=forms.ImageField()
    fecha=forms.DateField()
    titulo = forms.CharField(max_length=50)
    descripcion =  forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    tag=forms.CharField(max_length=50)
    url_github=forms.URLField()