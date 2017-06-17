from django import forms
from myapp.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'intro_course', 'time', 'avg_age']
    form = TOpicForm()
    subject = forms.CharField(max_length=100)
    intro_course = forms.CharField(widget=forms.Textarea)
    time = forms.DateField
    avg_age = forms.IntegerField(default=0)

class InterestForm(forms.Form):
