from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import *

from store.models import Customer


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = '__all__'

    name = CharField(widget=TextInput(attrs={'placeholder': 'Your name...'}),
                     max_length=70)
    email = EmailField(widget=EmailInput(attrs={'placeholder': 'harrypotter@hogwart.com'}),
                       max_length=40)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = False
        result = super().save(commit)
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        customer = Customer(user=result, name=name, email=email)
        if commit:
            customer.save()
        return result
