
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from PIL import Image
import os
import numpy as np
from django.contrib import messages

from keras import layers, models, Sequential
import tensorflow as tf

model = Sequential()
model.add(layers.Rescaling(1./255, input_shape=(70, 70, 3)))
model.add(layers.Conv2D(70, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(140, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(140, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(70, activation='relu'))
model.add(layers.Dense(2))

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

checkpoint_path = "training_1/cp.ckpt"
model.load_weights(checkpoint_path).expect_partial()

def predict_logo(request):
    context = {}  # Initialize context outside of the try block

    if request.method == 'POST':
        try:
            # Assuming you have an input field named 'logo_image' in your HTML form
            logo_image = request.FILES.get('logo_image')

            # Load and resize the image
            img = Image.open(logo_image).resize((70, 70))
            img_array = np.asarray(img).reshape((1, 70, 70, 3))

            # Perform prediction
            results = model.predict(img_array)[0]

            # Output the prediction result
            prediction_result = "Fake" if results[0] > results[1] else "Real"

            # Update the context
            context = {'prediction': prediction_result}

        except (ValueError, FileNotFoundError, IOError, Image.UnidentifiedImageError) as e:
            context = {'error': f"Error: {e}. Please upload a valid image."}

    return render(request, 'logo.html', context)


def register(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        else:
            my_user=User.objects.create_user(
                username=uname,
                email=email,
                password=pass1,
                )
            my_user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            return redirect('predict_logo')
        else:
            messages.error(request, 'Username or Password incorrect.') 
    return render(request,'login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')