
# Rayvers-Kitchen-API Documentation 🚀

Welcome to the coolest API in town! Here, we take authentication and user profiles to a whole new level. Buckle up and let the fun begin!

## Token Generation 🔐

### `POST /token/`

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
  "token": "your-magical-token",
  "user_id": 42,
  "email": "your.email@example.com"
}

```

Pro Tip: Don't forget your token; it's the secret sauce to unlock the treasures!

## Logout 🚪
## POST /logout/
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
## GET /users/me/
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

## PUT /users/me/
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
## POST /users/
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
  "user_id": 99,
  "email": "new.hero@example.com",
  "token": "your-magical-token"
}


```

Congratulations! You're now part of our superhero community. Keep your token safe!


#### That's it for now, fearless explorer! If you have more quests, check our URLs for additional adventures. May your API calls be swift and your tokens never expire! 🚀✨





