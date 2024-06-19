import cv2
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import UploadImageForm
from .mongo import collection
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            colors = analyze_image(image)
            collection.insert_one({'colors': colors})
            return JsonResponse(colors, safe=False)  # Set safe=False here
    else:
        form = UploadImageForm()
    return render(request, 'upload.html', {'form': form})

def analyze_image(image):
    # Read image using OpenCV
    image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    height, width, _ = image.shape

    # Assume the strip is in the center and extract the colors
    strip_width = width // 10
    colors = []
    for i in range(10):
        roi = image[height//2 - strip_width//2 : height//2 + strip_width//2, i*strip_width : (i+1)*strip_width]
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        colors.append({'RGB': [int(avg_color[0]), int(avg_color[1]), int(avg_color[2])]})
    return colors

def index(request):
    return render(request, 'index.html')
