from django import forms
from myapp.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'intro_course', 'time', 'avg_age']
        widgets = {'time': forms.RadioSelect()}
        labels = {'time':'Preferred Time', 'avg_age':'What is your age','intro_course':'This should be an introductory level course'}

class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((1,'Yes'),(0,'No')))
    age = forms.IntegerField(initial=20)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments',required=False)

class StudentForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    province = forms.CharField()
    age = forms.IntegerField()


class ChangePwd(forms.Form):
    password = forms.CharField()
    newpassword = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"Username",
        error_messages={'required': 'Please Input Username'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"Username",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"Password",
        error_messages={'required': u'Please Input Password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"Password",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"Username and Password are required fields. ")
        else:
            cleaned_data = super(LoginForm, self).clean()

class UserForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
