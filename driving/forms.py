from django import forms
from .models import Question, Option

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

OptionFormSet = forms.inlineformset_factory(
    Question, Option, 
    form=OptionForm,
    extra=4,  # Number of option fields to show
    min_num=2,  # Minimum number of options required
    validate_min=True,
    can_delete=False
)
