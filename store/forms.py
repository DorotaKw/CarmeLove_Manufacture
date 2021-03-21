import re

from django.forms import *


from .models import ProductOpinion, OrderComment


class ProductOpinionForm(ModelForm):
    class Meta:
        model = ProductOpinion
        fields = '__all__'

    rating = IntegerField(min_value=1, max_value=5, required=False)
    title = CharField(widget=TextInput(attrs={'placeholder': 'Title of opinion...'}), max_length=250, required=False)
    opinion = CharField(widget=Textarea(attrs={'placeholder': 'Opinion...'}), max_length=1500, required=False)

    def clean_title(self):
        initial = self.cleaned_data['title']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean_opinion(self):
        initial = self.cleaned_data['opinion']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


class OrderCommentForm(ModelForm):
    class Meta:
        model = OrderComment
        fields = ('comment',)

    comment = CharField(widget=Textarea(attrs={'placeholder': 'Your comment for order...'}),
                        max_length=500,
                        required=False)

    def clean_comment(self):
        initial = self.cleaned_data['comment']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)
