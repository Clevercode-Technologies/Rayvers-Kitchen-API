
# Rayvers-Kitchen-API Documentation 🚀

Welcome to the coolest API in town! Here, we take authentication and user profiles to a whole new level. Buckle up and let the fun begin!

## Token Generation 🔐

### `POST /auth/token/`

Generate a magic token to access our wonderland. Send your email and password to get the golden key.

**Request:**
```json
{
  "email": "your.email@example.com",
  "password": "supersecret"
}


```

### Response:

```json

{
  "user_id": 99,
  "email": "new.hero@example.com",
  "token": "your-magical-token"
}


```


## Logout 🚪
## POST /auth/logout/
Time to say goodbye. Use this endpoint to log out gracefully and secure the castle.
### Request:
{}  # No need for any payload, just hit the endpoint.


### Response:
```json
{
  "detail": "Logged out successfully."
}
```
Farewell, brave adventurer! Your session has ended.

## User Profile 🧑‍🚀
## GET /auth/users/me/
Retrieve your superhero profile details. Only for the chosen ones with a valid token.

### Response:

```json
{
  "email": "your.email@example.com",
  "name": "Captain Awesome",
  "date_of_birth": "1990-01-01",
  "is_superuser": true,
  "is_staff": false,
  "is_active": true,
  "profile_picture": "https://your.avatar.com",
  "bio": "Saving the world, one API call at a time."
}
```

## PUT /auth/users/me/
Update your superhero profile. Because even superheroes need a makeover!

Request:

```json
{
  "name": "New Hero Name",
  "date_of_birth": "1995-05-05",
  "bio": "A mysterious hero with a touch of humor."
}
```
### Response:

```json

{
  "email": "your.email@example.com",
  "name": "New Hero Name",
  "date_of_birth": "1995-05-05",
  "is_superuser": true,
  "is_staff": false,
  "is_active": true,
  "profile_picture": "https://your.avatar.com",
  "bio": "A mysterious hero with a touch of humor."
}
```

# Create New User 🦸‍♂️
## POST /auth/users/
Join the league of extraordinary individuals. Create your account and become a hero!

### Request:

```json
{
  "email": "new.hero@example.com",
  "password": "strongpassword"
}

```

### Response:
```json

{
  "message": "A verification code has been sent to talk2james@gmail.com.",
  "user_id": 5,
  "email": "talk2james@gmail.com",
  "role": "customer"
}

```

Pro Tip: Don't forget your token; it's the secret sauce to unlock the treasures!


## Verify User
POST /auth/users/verify/
A code will be send the user's email
The user_id must be sent along the code

```json
{
  "code": 4432,
  "user_id": 4
}
```

If the user's email is correct:
```json
{
  "message": "Account has been verified successfully. Proceed to login."
}
```

If user decides to apply for another verification code,
they can use this endpoint
### POST /auth/users/verify/resend-code/
```json

  {
    "user_id": 2
  }

```

### The Response

```json
{"message": "Code was resent to your email"}
```

### Error Handling
In case of an error, any of the following format is sent back to user

```json
{"message": "Code was resent to your email"}
{"message": "Encountered an issue sending email. Retry!"}
{"message": "Invalid user id. User does not exist."}
```

If the code is incorrect, you'll get a variety of responses:

```json
{
  "message": "User code is invalid"
}
{
  "message": "User does not exist."
}

```

## Reset Password
This is the endpoint for the forget password functionality

## POST /auth/users/reset/password/

```json
{
  "email": "john@doe.com"
}

```
### Response
```json
  {"message": "Code was sent to your email", "user_id": 2}
```
After the reset password endpoint is sent, the user can still use the resend-code endpoint to receive another code


### Error Handling
In case of an error, any of the following format is sent back to user FOR INCORRECT USER ID or EMAIL was not sent successfully.


```json
{"message": "User with email does not exist"} - 
{"message": "Encountered an issue sending email. Retry!", "user_id": 3}
```


## Reset Password with Code
### POST /auth/users/reset/password/code/

Here, we require a valid user_id, verification code, password and re_password fields to reset the password

```json

    {
      "user_id": 3,
      "code": 1238,
      "password": "newpassword",
      "re_password": "newpassword"
    }

```


### Error Handling
In case of an error, any of the following format is sent back to user.


```json
{"message": "Please enter the code sent to your mail."} 
{"message": "Unidentified user. Please send the user_id in payload."}
{"password": ["Password is required"]}
{"password": ["Password Confirmation is required"]}
{
"password": ["Please enter your password for both fields: password and re_password"]
}
{"password": ["Passwords must be valid strings"]}
{"password": ["Passwords do not match"]}
{"message": "User does not exist"}
{"message": "Code is incorrect"}
{"message": "Password was reset successfully."}
```




#### That's it for now, fearless explorer! If you have more quests, check our URLs for additional adventures. May your API calls be swift and your tokens never expire! 🚀✨


## Create Driver
In order to create driver you must provide `email` and `password`.
Note that only restaurants and admins have the permissions to create drivers.
You must have the authorization token in the header when attempting to create a driver.

If the authenticated user is not a restaurant or admin, `invalid token` response will be raised.
### Endpoint: /auth/drivers/  POST
```json
  {
    "email": "dummy@gmail.com",
    "password": "newpassword",
    "vehicle_image": "<FileData>",
    "vehicle_color": "red",
    "vehicle_description": "This is the vehicle description",
    "vehicle_number": "HGF203JS",
    "available": true
  }
```
After driver has been created, a verification code will be sent to the provided email
### Response
```json
{
  "message": "A verification code has been sent to dummy@gmail.com.",
  "user_id": 13,
  "driver_id": "qEBMwSQE",
  "role": "logistics"
}
```
### You can use the /auth/users/verify/ Endpoint to verify driver
```json
{
  "code": 2377,
  "user_id": 13
}
```

## Login the driver
After the driver has been verified, he can log in with his`driver_id` and `password`.
### Endpoint: /auth/drivers/token/ POST

```json
{
  "driver_id": "qEBMwSQE",
  "password": "newpassword"
}
```

#### Response -- Success

```json
{
  "token": "3be550010c177b16209c9aabe9a28717d46870a3",
  "user_id": 13,
  "driver_id": "qEBMwSQE"
}

```




## Create Restaurant
In order to create restaurant you must provide email and password

Note that only admins have the permissions to create restaurants.
You must have the authorization token in the header when attempting to create a restaurant.

If the authenticated user is not an admin, `invalid token` response will be raised.
### Endpoint: /auth/restaurants/  POST
```json
  {
    "email": "dummy@gmail.com",
    "password": "newpassword",
    "name": "Reyvers Restaurant",
    "description": "Best restaurant out there",
    "address": "Ijebu"
  }
```

After restaurant has been created, a verification code will be sent to the provided email

### Response
```json
{
  "message": "A verification code has been sent to dummy@gmail.com.",
  "user_id": 13,
  "kitchen_id": "qEBMwSQE",
  "role": "chef"
}
```
### You can use the /auth/users/verify/ Endpoint to verify restaurant
```json
{
  "code": 2377,
  "user_id": 13
}
```

## Login the restaurant
After the restaurant has been verified, he can log in with his`kitchen_id` and `password`.
### Endpoint: /auth/restaurants/token/ POST

```json
{
  "kitchen_id": "qEBMwSQE",
  "password": "newpassword"
}
```

#### Response -- Success

```json
{
  "token": "3be550010c177b16209c9aabe9a28717d46870a3",
  "user_id": 13,
  "kitchen_id": "qEBMwSQE"
}

```

## Change User Password
In order to change users password, the user token must be provided in the Authorization header.
## Endpoint /auth/users/change/password/ POST
### Payload
```json
  {
    "old_password": "myoldpassword",
    "new_password": "mynewestpassword",
    "confirm_new_password": "mynewestpassword"
  }

```

### Successful Response:

```json
  {"message": "Password was successfully updated."}
```

The following response will be received if an error occured:

```json
  {"password": ["old_password, new_password and confirm_new_password fields are required."]}
  {"password": ["Passwords do not match."]}
  {"password": ["Invalid user credentials. User does not exist."]}
  {"password": ["New password must be different from the previous passwords. "]}
  {"password": ["Old Password entered is incorrect"]}
  {"message": "Password was successfully updated."}
```
Some other password validation error will also occur when user password does not meet the validation score.

## Change User Driver and Kitchen IDs
In order to change users password, the user token must be provided in the Authorization header.
This endpoint changes the Ids for both kitchen and driver ids.
It can also change the username of the customer
## Endpoint /auth/users/change/username/

### Payload
```json
  {
    "username": "james"
  }

```
### Successful Response:

```json
  {"message": "Username was successfully updated."}
```

The following response will be received if an error occured:
```json
{"username": ["username field is required."]}
{"username": ["A user with username already exists. "]}
{"username": ["User does not exist."]}
```


## Get and Update Restaurant Profile information
To get restaurant info, you need to provide a valid token in the authorization header.
And you must ensure that user is a restaurant/kitchen. If it's not a restaurant you will receive a permission denied message.

Note that this view is for the logged in restaurant user is updating its data.
This user can also update profile information like profile picture and others
with this endpoint: `/auth/users/me/`. Remember this enpoint is used to retrieve and modify profile data.
### Endpoint /auth/restaurants/me/ GET

No payload required for a GET request.
### Endpoint /auth/restaurants/me/ PUT
Payload should look like this:
```json
{
  "name": "Reyvers Kitchen",
  "image": "<FileData>",
  "address": "1234 Sunny str. Ijebu",
  "rating": "3",
  "description": "This is the description"
}
```

Do not add kitchen_id here. This endpoint is for changing kitchen details, not changing kitchen_id.
To change kitchen_id, use the previous endpoint given: `/auth/users/change/username/`.

The following response will be received if an error occured:
```json
{"message": "User was not found"}
{"message": "User must be a chef. Permission denied."}
{"message":"You are not allowed to update kitchen id via this route"}
```

Some other error responses will also occur if the user data do not meet the validation score.


## Get and Update Driver Profile information
To get driver info, you need to provide a valid token in the authorization header.
And you must ensure that user is a driver/logistics. If it's not a driver you will receive a permission denied message.

Note that this view is for the logged in driver user is updating its data.
This user can also update profile information like profile picture and others
with this endpoint: `/auth/users/me/`. Remember this enpoint is used to retrieve and modify profile data.
### Endpoint /auth/drivers/me/ GET

No payload required for a GET request.
### Endpoint /auth/drivers/me/ PUT
Payload should look like this:
```json
{
  "vehicle_color": "Gold",
  "vehicle_description": "Vehicle Description",
  "vehicle_number": "GLU23HS",
  "available": true
}
```

Do not add kitchen_id here. This endpoint is for changing kitchen details, not changing kitchen_id.
To change kitchen_id, use the previous endpoint given: `/auth/users/change/username/`.

The following response will be received if an error occured:
```json
{"message": "User was not found"}
{"message": "User must be a chef. Permission denied."}
{"message":"You are not allowed to update kitchen id via this route"}
```

Some other error responses will also occur if the user data do not meet the validation score.


# List of Restaurants and Dishes
For all endpoints, the client must make request with a valid token in the Authorization header.

## Restaurants
### /api/restaurants/ GET
The above enpoint retrieves the list of restaurants and their information for all users to see.
The only constraint here is that users are only able to access it with their token in the `Authorization` header. If no token is found in the Authorization request header, a  `Authentication credentials were not provided` response  will be raised or a `Invalid token` response if the token in the header is invalid. The JSON object returned from this request as response is as follow:

```json

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Kada Plaza",
            "description": "This is Kada Plaza",
            "ratings": "0.0",
            "image": null,
            "address": "ReyversKitchen's Kitchen Address"
        },
        {
            "id": 1,
            "name": "ReyversKitchen",
            "description": "This is ReyversKitchen",
            "ratings": "3.0",
            "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/restaurant/Screen_Shot_2024-01-24_at_3.16.15_PM_hyvbl7",
            "address": "ReyversKitchen's Kitchen Address"
        }
    ]
}

```
The response above `count` represents the number of items in the list or array data structure. 
The `next` indicate the endpoint for the next set of items; `prev` does quite the opposite.


### /api/restaurants/<id>/ GET
The above endpoint is used to retrieve the detail view of any given restaurant in the database.
The response below will be given if the request was successful:

```json
{
    "id": 1,
    "name": "",
    "image": null,
    "description": "",
    "ratings": "0.0",
    "address": "",
    "dishes": [
        {
            "id": 2,
            "name": "Fried Rice",
            "description": "This is my favorite dish abeg.",
            "price": "300.00",
            "restaurant": 1,
            "ratings": "4.0",
            "favourite": [
                2
            ],
            "restaurant_details": {
                "name": "",
                "ratings": 0.0
            },
            "get_category": {
                "id": 2,
                "name": "english meals",
                "image": "/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
            },
            "images": [
                {
                    "id": 1,
                    "file": "/media/dishes/wiz_C06uxkq.png",
                    "label": "image 1"
                },
                {
                    "id": 2,
                    "file": "/media/dishes/wiz_RG5bfCI.png",
                    "label": "Image 2"
                }
            ],
            "category": 1
        },
        {
            "id": 1,
            "name": "Jollof Rice",
            "description": "This is the best food you have ever tasted",
            "price": "400.00",
            "restaurant": 1,
            "ratings": "5.0",
            "favourite": [],
            "restaurant_details": {
                "name": "",
                "ratings": 0.0
            },
            "get_category": {
                "id": 1,
                "name": "english meals",
                "image": "/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
            },
            "images": [
                {
                    "id": 1,
                    "file": "/media/dishes/wiz_C06uxkq.png",
                    "label": "image 1"
                },
                {
                    "id": 2,
                    "file": "/media/dishes/wiz_RG5bfCI.png",
                    "label": "Image 2"
                }
            ],
            "category": 1
        }
    ]
}

```





## Dishes

### /api/dishes/ GET, POST

The dishes endpoint retrieves all the dishes or food items in the database:

The client should expect a response like when making a GET request:

```json
  {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "name": "Swallow fufu",
            "description": "This is the description",
            "price": "3000.00",
            "restaurant": 1,
            "ratings": "0.0",
            "favourite": [],
            "restaurant_details": {
                "name": "",
                "ratings": 0.0
            },
            "get_category": {
                "id": 3,
                "name": "english meals",
                "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
            },
            "images": [
                {
                    "id": 3,
                    "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
                    "label": ""
                }
            ],
            "category": 1
        },
        {
            "id": 2,
            "name": "Fried Rice",
            "description": "This is my favorite dish abeg.",
            "price": "300.00",
            "restaurant": 1,
            "ratings": "4.0",
            "favourite": [
                2
            ],
            "restaurant_details": {
                "name": "",
                "ratings": 0.0
            },
            "get_category": {
                "id": 2,
                "name": "english meals",
                "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
            },
            "images": [
                {
                    "id": 1,
                    "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
                    "label": "image 1"
                },
                {
                    "id": 2,
                    "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
                    "label": "Image 2"
                }
            ],
            "category": 1
        },
        {
            "id": 1,
            "name": "Jollof Rice",
            "description": "This is the best food you have ever tasted",
            "price": "400.00",
            "restaurant": 1,
            "ratings": "5.0",
            "favourite": [],
            "restaurant_details": {
                "name": "",
                "ratings": 0.0
            },
            "get_category": {
                "id": 1,
                "name": "english meals",
                "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
            },
            "images": [
                {
                    "id": 1,
                    "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
                    "label": "image 1"
                },
                {
                    "id": 2,
                    "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
                    "label": "Image 2"
                }
            ],
            "category": 1
        },
        
        ...
    ]
}

```


For a POST request, you can decide to use a formData to send your request with the following body parameters `name`, `images`, `description`, `price`, `restaurant`, `category` and payload:

```json
{
  "name": "Jollof Rice",
  "description": "This is the best food you have ever tasted",
  "price": 4000,
  "restaurant": 1,
  "category": 1,
  "images": "[ListOfImages base64]" 
}
```
The `images` field is best handled using formData. But you can use it in other ways based on your use case.

### /api/dishes/<id>/ GET

The `id` parameter is used to get a specific dish. If a non-existent id is not provided, a 404 NOT FOUND response would be received by the client. In order to avoid this the right id must be given.


The expected response gotten will be as follows:


```json

{
    "id": 3,
    "name": "Swallow fufu",
    "description": "This is the description",
    "price": "3000.00",
    "restaurant": 1,
    "ratings": "0.0",
    "favourite": [],
    "_ingredients": [
        "onions",
        "carrot",
        "green peas"
    ],
    "restaurant_details": {
        "name": "",
        "ratings": 0.0
    },
    "get_category": {
        "id": 3,
        "name": "english meals",
        "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
    },
    "images": [
        {
            "id": 3,
            "file": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png",
            "label": ""
        }
    ],
    "category": 1
}

```
### /api/dishes/<id>/ GET, PUT, DELETE
Get request retrieves a single item by `id`.
The delete and the put requests are used for updating or permanently deleting the dish item.

The PUT request has a payload similar to that of the POST request, altghough you must ensure that
that every request ends in a slash (/).

# Categories
## /api/categories/ GET, POST
For Categories, the above endpoint can be used to likewise perform POST and GET operations.
The endpoint retrieves all the category data in the database. It also creates new categories with unique names. This depends on the method used in the request, whether a GET or POST request.

The Payload the client should expect to receive from a GET request is as follows:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "english meals",
            "image": "https://res.cloudinary.com/dqevhwn0e/image/upload/v1/media/category/Screen_Shot_2024-01-24_at_3.14.41_PM.png"
        }
    ]
}

```

Here, every category returns a paginated response of `id`, `name` and `image` in the payload.

Post request, on the other hand, does a different thing. It creates a new `category` with the following payload:

```json
  {
    "name": "traditional dishes",
    "image": "<FileData base64>"
  }

```
After being created, the response will contain the payload created.



## /api/categories/<id>/ GET, PUT, DELETE
The GET request will retrieve a single item based on the id provided as parameter.

The delete and the put requests are used for updating or permanently deleting categories.
The delete request does not need any payload, only the `id` parameters is received by the backend service and act upon. 

The PUT request, on the other hand requires a payload, same as the POST request.



