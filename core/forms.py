from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, Place, Relationship, Activity, Wish
)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='请输入有效的电子邮件地址'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用户名'
        self.fields['username'].help_text = '请输入不超过150个字符的用户名，只能包含字母、数字和 @/./+/-/_ 字符'
        self.fields['email'].label = '邮箱'
        self.fields['password1'].label = '密码'
        self.fields['password1'].help_text = '密码必须包含至少8个字符，不能是纯数字'
        self.fields['password2'].label = '确认密码'
        self.fields['password2'].help_text = '请再次输入相同的密码进行确认'

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label='邮箱',
        disabled=True,
        required=False
    )
    relationship_status = forms.CharField(
        label='感情状态',
        disabled=True,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['nickname', 'gender', 'birthday']
        widgets = {
            'birthday': forms.DateInput(
                attrs={
                    'type': 'text',
                    'placeholder': '选择生日日期',
                    'autocomplete': 'off'
                }
            ),
            'gender': forms.Select(choices=[('M', '男'), ('F', '女')]),
        }
        labels = {
            'nickname': '昵称',
            'gender': '性别',
            'birthday': '生日',
        }

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'location', 'visit_date', 'description', 'photo']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': '地点名称',
            'location': '具体位置',
            'visit_date': '访问日期',
            'description': '描述',
            'photo': '照片'
        }

class RelationshipForm(forms.ModelForm):
    partner_email = forms.EmailField(
        label='伴侣邮箱',
        help_text='请输入您伴侣的注册邮箱',
        widget=forms.EmailInput(attrs={'placeholder': '例如：partner@example.com'})
    )

    class Meta:
        model = Relationship
        fields = ['started_at']
        widgets = {
            'started_at': forms.DateInput(
                attrs={
                    'type': 'text',
                    'placeholder': '选择恋爱开始日期',
                    'autocomplete': 'off'
                }
            ),
        }
        labels = {
            'started_at': '恋爱开始日期',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_partner_email(self):
        email = self.cleaned_data['partner_email']
        try:
            partner = User.objects.get(email=email)
            if self.user and partner == self.user:
                raise forms.ValidationError('不能选择自己作为伴侣')
            
            if (Relationship.objects.filter(user1=partner).exists() or 
                Relationship.objects.filter(user2=partner).exists()):
                raise forms.ValidationError('该用户已经在一段关系中了')
                
            return email
        except User.DoesNotExist:
            raise forms.ValidationError('该邮箱未注册')

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'date', 'photo']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'text',
                    'placeholder': '选择活动日期',
                    'autocomplete': 'off'
                }
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': '活动标题',
            'description': '活动描述',
            'date': '活动日期',
            'photo': '活动照片'
        }

class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': '心愿标题',
            'description': '心愿描述'
        }