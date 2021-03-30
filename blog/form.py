from django.forms import ModelForm
import django.forms as form
from .models import Comment


class CommentForm(ModelForm):
    comment = form.CharField(max_length=200)

    class Meta:
        model = Comment
        fields = ['comment']

    def save(self):
        self.instance.comment = self.cleaned_data.get('comment')
        self.instance.save()
