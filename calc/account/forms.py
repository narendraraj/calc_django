from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
# from account.models import MyUser


MyUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    # email= forms.EmailField(max_length=255, help_text= 'Required', )
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(
    #     label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', )


# class CustomUserCreationForm(forms.ModelForm):
#     email = forms.EmailField(max_length=100, help_text='Required', error_messages={
#         'required': 'Sorry, you will need an email'})
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label='Repeat password', widget=forms.PasswordInput)

#     class Meta:
#         model = MyUser
#         fields = ('email', )

#     def clean_email(self):
#         email = slef.cleaned_data['email']
#         if MyUser.objects.filter(email=email).exists():
#             raise forms.ValidationError('Please use another Email, that is already taken')
#         return email

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['passowrd'] != cd['password2']:
#             raise froms.ValidationError('Passwords do not match.')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'E-mail', 'name':'email', 'id':'id_email'})
#         self.fields['password'].widget.attrs.update(
#             {'class': 'form-control', 'placeholder': 'Password'})
#         self.fields['password2'].widget.attrs.update(
#             {'class': 'form-control', 'placeholder': 'Repeat Password'})


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ("email",)


'''


class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField(max_length=255, help_text= 'Required', )

    class Meta:
        model = MyUser
        fields = ('email', "password1", "password2")
        
        


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'is_active', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password',  'is_active', 'is_admin',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


###############################################################
# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = MyUser
#         fields = ('email',)


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = MyUser
#         fields = ('email',)



##############################################################
# class CustomUserCreationForm(forms.ModelForm):

#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model: MyUser
#         fields = ['email']

#     def clean_password2(self):
#         """
#         Verify both passwords match.

#         """

#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1!= password2:
#             raise ValueError("Passwords dont match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data)["password1"]
#         if commit:
#             user.save()
#         return user


# class CustomUserChangeForm(forms.ModelForm):
    
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = MyUser
#         fields = ('email', 'password', 'is_active', 'is_admin')
    
        
'''
