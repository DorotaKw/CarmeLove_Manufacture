from django.forms import *


from .models import ProductOpinion, OrderComment


class ProductOpinionForm(ModelForm):
    class Meta:
        model = ProductOpinion
        fields = '__all__'

    rating = IntegerField(min_value=1, max_value=5, required=False)
    title = CharField(widget=TextInput(attrs={'placeholder': 'Title of opinion...'}), max_length=250, required=False)
    opinion = CharField(widget=Textarea(attrs={'placeholder': 'Opinion...'}), max_length=1500, required=False)


class OrderCommentForm(ModelForm):
    class Meta:
        model = OrderComment
        fields = ('comment',)

    comment = CharField(widget=Textarea(attrs={'placeholder': 'Your comment for order...'}),
                        max_length=400,
                        required=False)
