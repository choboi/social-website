from django import forms
from .models import Image
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widget = {
            'url': forms.HiddenInput,
        }


def clean_url(self):
    url = self.cleaned_data['url']
    valid_extensions = ['jpg', 'jpeg', 'png']
    extension = url.rsplit('.', 1)[1].lower()
    if extension not in valid_extensions:
        raise forms.ValidationError('The given URL does not match valid images extensions.')
    return url


def save(self, force_insert=False, force_update=False, commit=True):
    image = super().save(commit=False)  # Save the model instance without saving the images yet

    image_url = self.cleaned_data['url']
    name = slugify(image.title)
    extension = image_url.rsplit('.', 1)[1].lower()
    image_name = f'{name}.{extension}'

    # Download images from the given URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception for unsuccessful downloads

    # Save the downloaded images to the model instance
    image.image.save(
        image_name,
        ContentFile(response.content),
        save=False
    )

    if commit:
        image.save()  # Save the model instance including the images

    return image
