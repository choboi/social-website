from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        if 'url' in request.GET:
            form = ImageCreateForm(data=request.GET)
        else:
            form = ImageCreateForm()
    return render(request, 'images/image_create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    """
    Retrieves and renders the details of a specific image.

    Args:
        request: The HTTP request object.
        id: The ID of the image.
        slug: The slug of the image.

    Returns:
        An HTTP response containing the rendered template.
    """

    image = get_object_or_404(Image, id=id, slug=slug)
    print(image)  # Print the image object to the console
    return render(
        request,
        'images/image_detail.html',
        {'section': 'images', 'image': image}
    )
