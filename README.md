# Anime Watchlist Application

#### video Demo: <https://youtu.be/aImoX-gljsk>

## Overview

The Anime Watchlist Application is a web-based platform that allows users to track and manage their anime viewing experience. Users can add anime to their watchlist, update their viewing status, manage their progress, and rate the shows they've watched. This application utilizes Django for the backend and vanilla JavaScript for the frontend.

## Features

- **User Authentication**: Users can register, log in, and manage their profiles.
- **Watchlist Management**: Users can add anime to their watchlist with options to update their status (e.g., currently watching, completed).
- **Episode Tracking**: Users can track their progress by updating the current episode they are on.
- **Rating System**: Users can rate the anime they watch.
- **Anime Database**: A comprehensive database of anime with detailed descriptions, links, and genres.

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or any other supported database)
- **Machine Learning**: Scikit-learn (for any potential future enhancements related to recommendations)

## Installation

To set up the project locally, follow these steps:

### 1. **Clone the Repository**:
   ```git clone https://github.com/yourusername/anime-watchlist.git```
   ```cd anime-watchlist```

### 2. Install Dependencies: Ensure you have Python and pip installed, then run:

``` pip install -r requirements.txt ```

### 3. Run Migrations: Create the database tables:


```python manage.py migrate```

### 4. Create a Superuser (optional): If you want to access the admin panel:


```python manage.py createsuperuser```

### 5. Run the Development Server: Start the Django development server:

```python manage.py runserver```

### 6. Access the Application: Open your web browser and go to http://127.0.0.1:8000/.

## Usage
- #### Register a New Account: Navigate to the registration page to create a new user account.
- #### Log In: Use your credentials to log in to your account.
- #### Add Anime: Search for anime and add them to your watchlist.
- #### Update Status: Change the status of each anime as you watch them.
- #### Track Progress: Update the current episode you are on.
- #### Rate Anime: Provide ratings for anime you've completed.

## File Structure

/anime_watchlist

|-- /migrations

|-- /static

|-- /templates

|-- /media

|-- manage.py

|-- requirements.txt

|-- settings.py

|-- urls.py

|-- views.py

|-- models.py

|-- index.js

## Models

### User
- Extends Django's AbstractUser for custom user functionality.

## Genre
- Represents anime genres.

## Anime
- Stores details about anime, including title, description, picture URL, and genres.

## UserAnimeList
- Links users to their anime with fields for status, rating, progress, and reviews.

## Contributing
Contributions are welcome! If you want to contribute to the project, please fork the repository and submit a pull request.

1. Fork the repository
2. Create a new branch (git checkout -b feature/YourFeature)
3. Make your changes
4. Commit your changes (git commit -m 'Add some feature')
5. Push to the branch (git push origin feature/YourFeature)
6. Open a Pull Request

## Acknowledgements
[Django Documentation](https://docs.djangoproject.com/en/5.1/)
[JavaScript Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[Anime APIs](https://rapidapi.com/felixeschmittfes/api/myanimelist/playground/apiendpoint_df7df34c-2e4a-4231-a9e2-8d76c6445333)