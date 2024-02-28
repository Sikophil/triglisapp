from accounts.models import customuser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Book

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'field', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'field', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'field', 'placeholder':'Last Name'}))

	class Meta:
		model = customuser
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'field'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = ''

		self.fields['password1'].widget.attrs['class'] = 'field'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = ''
        #   <ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>

		self.fields['password2'].widget.attrs['class'] = 'field'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = ''
        #   <span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



# class SignUpForm(UserCreationForm):
# 	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control form form_4', 'placeholder':'Email Address'}))
# 	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control form form_2', 'placeholder':'First Name'}))
# 	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control form form_3', 'placeholder':'Last Name'}))

# 	class Meta:
# 		model = customuser
# 		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# 	def __init__(self, *args, **kwargs):
# 		super(SignUpForm, self).__init__(*args, **kwargs)

# 		self.fields['username'].widget.attrs['class'] = 'form-control form form_1'
# 		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
# 		self.fields['username'].label = ''
# 		self.fields['username'].help_text = ''

# 		self.fields['password1'].widget.attrs['class'] = 'form-control form form_5'
# 		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
# 		self.fields['password1'].label = ''
# 		self.fields['password1'].help_text = ''
#         #   <ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>

# 		self.fields['password2'].widget.attrs['class'] = 'form-control form form_6'
# 		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
# 		self.fields['password2'].label = ''
# 		self.fields['password2'].help_text = ''
#         #   <span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


# class OrderForm(forms.ModelForm):
#     # date = forms.CharField( max_length=100,label="Order Date", widget=forms.TextInput(attrs={'class': 'form-control form form_2', 'placeholder': 'YYYY-MM-DD'}))
#     # time = forms.CharField(max_length=100,label="Order Time", widget=forms.TextInput(attrs={'class': 'form-control form form_1', 'placeholder': 'HH:MM'}))
#     # guests = forms.CharField(max_length=100,label="Number of guests", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    
#     class Meta:
#         model = Book
#         fields = ['time', 'date','guests']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['time'].widget.attrs['class'] = 'form-control form form_1'
#         self.fields['date'].widget.attrs['class'] = 'form-control form form_2'
#         self.fields['guests'].widget.attrs['class'] = 'form-control'
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['time', 'date','guests']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].label = ''
        self.fields['time'].widget.attrs['class'] = "new_book_button"
        self.fields['time'].widget.attrs['placeholder'] = 'Zeit'
		
        self.fields['date'].widget.attrs['class'] = "new_book_button"
        self.fields['date'].widget.attrs['placeholder'] = 'Datum'
        self.fields['date'].label = ''
        
        self.fields['guests'].widget.attrs['class'] = "new_book_button"
        self.fields['guests'].widget.attrs['placeholder'] = 'Anzahl der Gäste'
        self.fields['guests'].label = ''


class NotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
