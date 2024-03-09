
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login ,logout
from PIL import Image
import os
import numpy as np
from django.contrib import messages
from .models import *

from keras import layers, models, Sequential
import tensorflow as tf

################### First
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
    user=request.user
    context = {}  # Initialize context outside of the try block
    if request.method == 'POST':
        
            # Assuming you have an input field named 'logo_image' in your HTML form
        logo_image = request.FILES.get('logo_image')

            # Load and resize the image
        img = Image.open(logo_image).resize((70, 70))
        img_array = np.asarray(img).reshape((1, 70, 70, 3))

            # Perform prediction
        results = model.predict(img_array)[0]

            # Output the prediction result
        prediction_result = "Fake" if results[0] > results[1] else "Real"

            # save predicted result and logo image to database
        predict=LogoPrediction.objects.create(
            result=prediction_result,
            image=logo_image,
            user=user
            )
        predict.save()

            # Query all Category objects
            

            # Update the context
        context = {
            'prediction': prediction_result,
        }

    return render(request,'logo.html',context)

############second

def category(request):
    categories = Category.objects.all()
    context = {
            
            'categories':categories
        }
    return render(request,'category.html',context)

############# third 
def register(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        fname=request.POST.get('name')
        address=request.POST.get('address')
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
                first_name=fname,
                last_name=address,
                )
            my_user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

    return render(request,'user/register.html')

############# Four 
def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('predict_logo')
        else:
            messages.error(request, 'Username or Password incorrect.') 
    return render(request,'user/login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')

############# five :-
def view_user(request):
    view=request.user
    if request.method == 'POST':
        view.username =  request.POST.get('username')
        view.first_name =  request.POST.get('first_name')
        view.last_name =  request.POST.get('address')
        view.email =  request.POST.get('email')
        view.save()
        messages.success(request, 'Updation successfully completed')

        return redirect('view_user')
    context={
        'view':view
    }    
    return render(request,'user_details.html',context)

############# six :-

def view_product(request,pk):
    category=Category.objects.get(pk=pk)
    product=Product.objects.filter(category=category)
    context={
        'products':product
    }
    return render(request,'view_product.html',context)

def view_prediction(request):
    user=request.user
    predict=LogoPrediction.objects.filter(user=user)
    context={
        'predict':predict
    }
    return render(request,'prediction.html',context)


################### First :- 

# model = Sequential(): Initializes a sequential model. Sequential is a linear stack of layers.

# model.add(layers.Rescaling(1./255, input_shape=(70, 70, 3))): Adds a rescaling layer to the model. This layer rescales the pixel values of the input image to be between 0 and 1.

# model.add(layers.Conv2D(70, (3, 3), activation='relu')): Adds a 2D convolutional layer with 70 filters and a ReLU activation function.

# model.add(layers.MaxPooling2D((2, 2))): Adds a max-pooling layer with a pool size of 2x2.

# model.add(layers.Conv2D(140, (3, 3), activation='relu')): Adds another 2D convolutional layer with 140 filters and a ReLU activation function.

# model.add(layers.MaxPooling2D((2, 2))): Adds another max-pooling layer with a pool size of 2x2.

# model.add(layers.Conv2D(140, (3, 3), activation='relu')): Adds another 2D convolutional layer with 140 filters and a ReLU activation function.

# model.add(layers.Flatten()): Flattens the output of the convolutional layers to feed into a densely connected layer.

# model.add(layers.Dense(70, activation='relu')): Adds a densely connected layer with 70 units and a ReLU activation function.

# model.add(layers.Dense(2)): Adds the output layer with 2 units. There is no activation function specified, which means it will be applied later during inference.

# model.compile(...): Compiles the model with the specified optimizer, loss function, and metrics for training.

# checkpoint_path = "training_1/cp.ckpt": Specifies the path where the model weights are saved.

# model.load_weights(checkpoint_path).expect_partial(): Loads the pre-trained weights into the model.

# def predict_logo(request): Defines a function named predict_logo that takes a request object as input.

# context = {}: Initializes an empty context dictionary.

# if request.method == 'POST':: Checks if the request method is POST.

# logo_image = request.FILES.get('logo_image'): Retrieves the uploaded logo image file from the request.

# img = Image.open(logo_image).resize((70, 70)): Opens the image file using PIL (Python Imaging Library) and resizes it to 70x70 pixels.

# img_array = np.asarray(img).reshape((1, 70, 70, 3)): Converts the resized image to a NumPy array and reshapes it to match the input shape expected by the model.

# results = model.predict(img_array)[0]: Uses the trained model to predict the class probabilities for the input image.

# prediction_result = "Fake" if results[0] > results[1] else "Real": Determines the predicted class based on the class probabilities.

# predict=LogoPrediction.objects.create(...): Creates a new LogoPrediction object in the database with the prediction result and the image.

# predict.save(): Saves the LogoPrediction object to the database.

# context = {'prediction': prediction_result}: Updates the context dictionary with the prediction result.

# return render(request,'logo.html',context): Renders the 'logo.html' template with the updated context and returns the result to the client.


############second:-

# def category(request):: Defines a Python function named category that takes a request object as input. In Django, view functions receive HTTP requests and return HTTP responses.

# categories = Category.objects.all(): Queries all objects of the Category model from the database using Django's Object-Relational Mapping (ORM). This line retrieves all categories stored in the database.

# context = {'categories': categories}: Creates a dictionary named context containing a key-value pair where the key is 'categories' and the value is the queryset categories obtained in the previous step. This context will be used to pass data to the template for rendering.

# return render(request, 'category.html', context): Renders a template named 'category.html' using the data in the context dictionary. The render function combines the provided template with the given context data and returns an HTTP response. This response typically contains HTML content that can be displayed in a web browser.

############# third :-

# def register(request):: Defines a view function named register that handles user registration.

# if request.method=='POST':: Checks if the HTTP request method is POST, indicating that the user has submitted a form.

# uname=request.POST.get('username'): Retrieves the value of the input field named 'username' from the submitted form data.

# fname=request.POST.get('name'): Retrieves the value of the input field named 'name' (presumably first name) from the submitted form data.

# address=request.POST.get('address'): Retrieves the value of the input field named 'address' from the submitted form data.

# email=request.POST.get('email'): Retrieves the value of the input field named 'email' from the submitted form data.

# pass1=request.POST.get('password'): Retrieves the value of the input field named 'password' from the submitted form data.

# if User.objects.filter(username=uname).exists():: Checks if a user with the provided username already exists in the database.

# messages.error(request, 'Username already exists.'): If a user with the provided username already exists, an error message is added to the Django messages framework for display.

# return render(request, 'register.html'): Renders the 'register.html' template to display the registration form again.

# else:: If the provided username is unique, proceeds with user creation.

# my_user=User.objects.create_user(...): Creates a new user object using Django's built-in user model manager create_user() method.

# my_user.save(): Saves the newly created user object to the database.

# messages.success(request, 'Registration successful. You can now log in.'): Adds a success message to the Django messages framework indicating successful registration.

# return redirect('login'): Redirects the user to the 'login' page upon successful registration.

# return render(request,'user/register.html'): Renders the 'user/register.html' template for displaying the user registration form initially.

# def category(request):: Defines a view function named category that handles category retrieval.

# categories = Category.objects.all(): Queries all category objects from the database.

# context = {'categories':categories}: Creates a context dictionary containing the retrieved categories.

# return render(request,'category.html',context): Renders the 'category.html' template with the categories passed in the context for display. 


###############  Four :-

# def login(request):: Defines a view function named login that handles user login.

# if request.method=='POST':: Checks if the HTTP request method is POST, indicating that the user has submitted a login form.

# username=request.POST.get('username'): Retrieves the value of the input field named 'username' from the submitted form data.

# pass1=request.POST.get('password'): Retrieves the value of the input field named 'password' from the submitted form data.

# user=authenticate(request,username=username,password=pass1): Authenticates the user credentials against the user database. The authenticate() function takes the request object, username, and password as parameters and returns a user object if authentication is successful, or None otherwise.

# if user is not None:: Checks if the user authentication was successful.

# auth_login(request, user): Logs in the authenticated user. The auth_login() function adds the user's ID to the session, effectively logging the user in.

# return redirect('predict_logo'): Redirects the user to the 'predict_logo' page upon successful login.

# else:: If the user authentication failed:

# messages.error(request, 'Username or Password incorrect.'): Adds an error message to the Django messages framework indicating incorrect username or password.

# return render(request,'user/login.html'): Renders the 'user/login.html' template for displaying the login form again.

# return render(request,'user/login.html'): Renders the 'user/login.html' template for displaying the login form initially.


############# five :-


# def view_user(request):: Defines a view function named view_user that handles the user details view and update functionality.

# view=request.user: Retrieves the currently logged-in user object from the request. request.user represents the user associated with the current request.

# if request.method == 'POST':: Checks if the HTTP request method is POST, indicating that the user has submitted a form to update their details.

# view.first_name = request.POST.get('first_name'): Updates the first name of the user with the value submitted in the POST request.

# view.last_name = request.POST.get('address'): Updates the last name of the user with the value submitted in the POST request. Note: It seems like there might be a typo here; 'address' might be intended to represent the last name.

# view.email = request.POST.get('email'): Updates the email address of the user with the value submitted in the POST request.

# view.save(): Saves the changes made to the user object in the database.

# messages.success(request, 'Updation successfully completed'): Adds a success message to the Django messages framework to indicate that the update was successful.

# return redirect('view_user'): Redirects the user to the 'view_user' page after successful update. This likely refreshes the page to display the updated user details.

# context={'view':view}: Creates a context dictionary containing the user object to be passed to the template for rendering.

# return render(request,'user_details.html',context): Renders the 'user_details.html' template with the user details passed in the context for display. 


######### six :- 

# def view_product(request, pk):: Defines a view function named view_product that takes two parameters: request, which represents the HTTP request made by the user, and pk, which is the primary key of the category whose products are to be displayed.

# category = Category.objects.get(pk=pk): Retrieves the category object from the database whose primary key matches the pk parameter passed to the view. This assumes that the Category model has been defined with a primary key field named 'pk'.

# product = Product.objects.filter(category=category): Retrieves all products from the Product model that belong to the category obtained in the previous step. It filters products based on the 'category' attribute, which is assumed to be a foreign key field linking each product to its category.

# context = {'products': product}: Creates a dictionary named context containing the retrieved products, which is then passed to the template for rendering. The key 'products' will be used in the template to access the list of products.

# return render(request, 'view_product.html', context): Renders the 'view_product.html' template with the products passed in the context for display. This HTML template will likely iterate over the list of products and present them in a user-friendly format.