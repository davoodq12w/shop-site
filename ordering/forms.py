from django import forms
from account.models import ShopUser
from .models import Order, Reject
from account.models import Address


class VerifyPhoneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'شماره ی خود را وارد کنید'}), max_length=11,
                            label='شماره تلفن')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('شماره تلفن از قبل وجود دارد لطفا ابتدا وارد حساب کاربری خود شوید ')

        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم باشد ')

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود ')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط عدد باشد')

        return phone


class CreatOrderForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Order
        fields = ('name', 'phone', 'province', 'city', 'postal_code', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'receiver-name'}),
            'phone': forms.TextInput(attrs={'class': 'receiver-phone'}),
            'province': forms.TextInput(attrs={'class': 'receiver-province'}),
            'city': forms.TextInput(attrs={'class': 'receiver-city'}),
            'postal_code': forms.TextInput(attrs={'class': 'receiver-postal-code'}),
            'address': forms.Textarea(attrs={'class': 'receiver-exact-address',
                                             'placeholder': 'مثال: خیابان امام کوچه پنج پلاک هفتم واحد دو'}),
        }
        labels = {
            'province': 'استان',
            'city': 'شهر',
            'address': 'آدرس دقیق',
            'postal_code': 'کد پستی',
            'name': 'نام و نام خانوادگی گیرنده',
            'phone': 'شماره تماس گیرنده',
        }

    def clean_postal_code(self):

        postal_code = self.cleaned_data.get('postal_code')
        
        if Address.objects.filter(postal_code=postal_code).exclude(user=self.request.user).exists():
            raise forms.ValidationError('کد پستی از قبل وجود دارد')

        if len(postal_code) != 10:
            raise forms.ValidationError('کد پستی باید 10 رقم باشد')

        if not postal_code.isdigit():
            raise forms.ValidationError('کد پستی باید عدد باشد')

        return postal_code

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


class RejectForm(forms.ModelForm):

    class Meta:
        model = Reject
        fields = ['quantity', 'description']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'quantity-of-reject-input', 'value': '1'},),
            'description': forms.Textarea(attrs={'class': 'description-of-reject-input'})
        }
        labels = {
            'quantity': "تعداد کالاهای ارجاعی",
            'description': "توضیحات دلیل ارجاع"
        }


