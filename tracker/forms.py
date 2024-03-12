from django import forms

from .models import YoutubeFilterTracker


class YoutubeFilterTrackerForm(forms.ModelForm):
    """
    YouTube filter tracker form.
    This form is used to create a new YouTube filter tracker.
    """

    CATEGORY_CHOICES = (('1', 'Film & Animation'),)

    date_range = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'date_range',
                'placeholder': 'Select date range',
            }
        ),
        required=True,
    )

    # set default selected category to '4' (Entertainment)
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                'id': 'category',
                'placeholder': 'Select category',
                'value': '1',
            }
        ),
        required=True,
    )

    class Meta:
        model = YoutubeFilterTracker
        fields = ['category', 'channels', 'start_date', 'end_date', 'video_tags']
        widgets = {
            'category': forms.Select(attrs={'placeholder': 'Select category'}),
            'channels': forms.TextInput(
                attrs={
                    'placeholder': 'Enter channels ID or URL',
                    'value': 'UCsgC5cbz3DE2Shh34gNKiog',
                }
            ),
            'video_tags': forms.TextInput(attrs={'placeholder': 'Enter video tags'}),
            'title': forms.HiddenInput(),
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }
        error_messages = {
            'category': {
                'required': 'Please select a category',
            },
            'channels': {
                'required': 'Please enter a channels ID or URL',
            },
        }

    def clean_date_range(self):
        date_range = self.cleaned_data.get('date_range')
        start_date, end_date = date_range.split(' - ')
        self.cleaned_data['start_date'] = start_date
        self.cleaned_data['end_date'] = end_date
        return date_range
