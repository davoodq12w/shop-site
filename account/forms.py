from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class ShopUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['phone'].label = 'شماره تلفن'
        self.fields['first_name'].label = 'نام'
        self.fields['last_name'].label = 'نام خانوادگی'
        self.fields['password1'].label = 'رمز'
        self.fields['password2'].label = 'تایید رمز'

    class Meta(UserCreationForm.Meta):

        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'phone-input', }),
            'first_name': forms.TextInput(attrs={'class': 'first-name-input', }),
            'last_name': forms.TextInput(attrs={'class': 'last-name-input', }),
            'password1': forms.PasswordInput(attrs={'class': 'password1-input', }),
            'password2': forms.PasswordInput(attrs={'class': 'password2-input', }),
        }
        required_fields = ['phone', 'first_name', 'last_name', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('شماره تلفن درحال حاضر موجود میباشد')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('شماره تلفن درحال حاضر موجود میباشد')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط عدد باشد')

        if len(phone) != 11:
            raise forms.ValidationError('تعداد ارقام باید 11 رقم باشد')

        if not phone.startswith('09'):
            forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        return phone

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('رمز ها یکسان نیستند')
        return self.cleaned_data['password2']


class ShopUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].label = 'شماره تلفن'
        self.fields['first_name'].label = 'نام'
        self.fields['last_name'].label = 'نام خانوادگی'
        self.fields['password'].help_text = None
        self.fields['password'].label = 'رمز'

    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name',)

    def clean_phone(self):

        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('شماره تلفن درحال حاضر موجود میباشد')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('شماره تلفن درحال حاضر موجود میباشد')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط عدد باشد')

        if len(phone) != 11:
            raise forms.ValidationError('تعداد ارقام باید 11 رقم باشد')

        if not phone.startswith('09'):
            forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        return phone


class ShopLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'login-phone'}), required=True, label='شماره تلفن')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-password'}), required=True,
                               label='رمز')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise forms.ValidationError('شماره تلفن وجود ندارد')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط عدد باشد')

        if len(phone) != 11:
            raise forms.ValidationError('تعداد ارقام باید 11 رقم باشد')

        if not phone.startswith('09'):
            forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        return phone

    def clean_password(self):
        user = ShopUser.objects.get(phone=self.cleaned_data.get('phone'))
        password = self.cleaned_data.get('password')
        if not user.check_password(password):
            raise forms.ValidationError('رمز اشتباه میباشد')
        return password


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['province', 'city', 'exact_address', 'postal_code', 'receiver_name', 'receiver_phone']
        widgets = {
            'exact_address': forms.Textarea(attrs={'placeholder': 'مثال: خیابان امام کوچه پنج پلاک هفتم واحد دو'}),
            'receiver_name': forms.TextInput(attrs={'class': 'receiver-name'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'receiver-phone'}),
        }
        labels = {
            'province': 'استان',
            'city': 'شهر',
            'exact_address': 'آدرس دقیق',
            'postal_code': 'کد پستی',
            'receiver_name': 'نام و نام خانوادگی گیرنده',
            'receiver_phone': 'شماره تماس گیرنده',
        }

    def clean_postal_code(self):

        postal_code = self.cleaned_data.get('postal_code')

        if self.instance.pk:
            if Address.objects.filter(postal_code=postal_code).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('کد پستی از قبل وجود دارد')
        else:
            if Address.objects.filter(postal_code=postal_code).exists():
                raise forms.ValidationError('کد پستی از قبل وجود دارد')

        if len(postal_code) != 10:
            raise forms.ValidationError('کد پستی باید 10 رقم باشد')

        if not postal_code.isdigit():
            raise forms.ValidationError('کد پستی باید عدد باشد')

        return postal_code

    def clean_receiver_phone(self):

        phone = self.cleaned_data.get('receiver_phone')

        if not phone:
            raise forms.ValidationError('شماره تلفن وجود ندارد')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط عدد باشد')

        if len(phone) != 11:
            raise forms.ValidationError('تعداد ارقام باید 11 رقم باشد')

        if not phone.startswith('09'):
            forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        return phone


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('Criticism', 'انتقاد'),
        ('Proposal', 'پیشنهاد'),
        ('Report', ' گزارش'),
    )
    subject = forms.ChoiceField(required=True, choices=SUBJECT_CHOICES, label='موضوع')
    name = forms.CharField(required=True, max_length=100, label='نام')
    phone = forms.CharField(required=True, max_length=11, min_length=11, label='شماره تلفن')
    email = forms.CharField(required=True, max_length=250, label='ایمیل')
    message = forms.CharField(required=True, widget=forms.Textarea(), label='متن تیکت')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError('Invalid phone number')
        return phone
