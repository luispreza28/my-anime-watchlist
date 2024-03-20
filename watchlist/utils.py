from .models import UserAnimeList, Anime, User, Genre 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


X_RAPIDAPI_KEY = 'a91c7434eemsh0a1161df1519403p1f2fe2jsnf218290f6e7d'
X_RAPIDAPI_HOST = 'myanimelist.p.rapidapi.com'

headers = {
    "X-RapidAPI-Key": X_RAPIDAPI_KEY,
    "X-RapidAPI-Host": X_RAPIDAPI_HOST
  }

def get_user_anime_list_by_status(user, status):
  if status == 'all':
    return UserAnimeList.objects.filter(user=user)
  else:
    return UserAnimeList.objects.filter(user=user, status=status)

def get_status_count(user, status):
  return UserAnimeList.objects.filter(user=user, status=status).count()

def get_paginated_data(anime_list, items_per_page, request):
  paginator = Paginator(anime_list, items_per_page)
  page = request.GET.get('page')

  try:
    paginated_data = paginator.page(page)
  except PageNotAnInteger:
    paginated_data = paginator.page(1)
  except EmptyPage:
    paginated_data = paginator.page(paginator.num_pages)

  return paginated_data

def get_recommended_anime(user):
  # Grab all animes
  all_animes = Anime.objects.all()
  
  # TF-IDF vectorization for genres
  genre_names = [genre.name for genre in Genre.objects.all()]
  genre_vectorizer = TfidfVectorizer().fit(genre_names)
  genre_matrix = genre_vectorizer.transform(genre_names).toarray()
  
  # User Profile creation
  user_ratings = UserAnimeList.objects.filter(user=user, rating__isnull=False)
  user_genres = [anime.anime.genre.all() for anime in user_ratings]

  # Transform each genre and compute the sum
  user_genre_matrix = sum(genre_vectorizer.transform([genre.name]).toarray() for genres in user_genres for genre in genres)
  
  # Calculate Cosine Similarity
  try:
    cosine_similarities = cosine_similarity(user_genre_matrix, genre_matrix)
  except:
    return False
  top_anime_indices = cosine_similarities.flatten().argsort()[::-1]

  recommended_animes = []

  # Grab users watchlist
  users_watchlist = UserAnimeList.objects.filter(user=user)
  users_watchlist_anime_titles = [anime.anime.title for anime in users_watchlist]

  # Filter out anime that are already in users watchlist
  for i in top_anime_indices:
    anime = all_animes[int(i)]
    if anime.title not in users_watchlist_anime_titles:
      recommended_animes.append(anime)

  return recommended_animes

# function for searching an anime and getting informatoin
def fetch_detailed_anime_data(anime_id, request):
  try:
    get_anime_url = f"https://myanimelist.p.rapidapi.com/anime/{anime_id}"

    response = requests.get(get_anime_url, headers=headers)
    response.raise_for_status()

    return response.json()
  except requests.exceptions.RequestException as e:
        # Handle the exception 
        print(f"Error fetching detailed anime data: {str(e)}")
        return None

# Add animes to database
def add_anime_to_database(response, request):
  if response.status_code == 200 and response.headers.get('Content-Type', ''):
    
    anime_data = response.json()
    
    for anime_entry in anime_data:
      anime_title = anime_entry['title']
      
      anime_id = anime_entry.get("myanimelist_id")
      
      detailed_anime_data = fetch_detailed_anime_data(anime_id, request)
      
      if detailed_anime_data:
        # Extract genres from detailed_anime_data
        
        genre_data = detailed_anime_data.get('information', {}).get('genres', [])
        genres_list = []
        
        for genre in genre_data:
        
          genre_name = genre.get('name')
        
          genre, created = Genre.objects.get_or_create(name=genre_name)        
        
          genres_list.append(genre)
    
        if not Anime.objects.filter(title=anime_title).exists():
          
          anime_entry = Anime.objects.create(
            myanimelist_id = anime_entry['myanimelist_id'],
            picture_url = anime_entry['picture_url'],
            myanimelist_url = anime_entry['myanimelist_url'],
            title = anime_entry['title_ov'],
            description = detailed_anime_data.get('synopsis', '')
          )
    
          anime_entry.genre.set(genres_list)
    
          anime_entry.save()
          print("Added anime Successfully:", anime_entry)
        else:
          print("Anime already exists in anime database:", anime_entry)
          return HttpResponse("anime already exists")
      else:
        print("Detailed anime data is empty:", detailed_anime_data)
    print("Finished adding animes to Anime data base:", anime_data)
    return 
  else:
    print("Error in fetching anime data from API", status=response.status)
    return

def make_api_request(url):
  return requests.get(url, headers=headers)

def validate_user(request):
  username = request.POST.get('username')
  password = request.POST.get('password')
  user = authenticate(request, username=username, password=password)

  if user is not None:
    login(request, user)
    return True

def register_user(request):
  # grab username
  username = request.POST.get("username")

  # grab email
  email = request.POST.get("email")

  # grab password
  password = request.POST.get("password")

  #grab confirmation 
  confirmation = request.POST.get("confirmation")
  
  # check if password matches confirmation
  if password != confirmation:
    # return user back to register form if password doesnt match with confirmation
    return False
  try:
    # register user
    user = User.objects.create_user(username, email, password)
    user.save()

  except IntegrityError:
    return render(request, 'watchlist/register.html', {
      "message": "Username already exists. Try again."
    })
    
  return user    

def is_ajax_request(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def generate_ajax_response(paginated_data):
  return {
    'anime_data': paginated_data.object_list,
    'has_next': paginated_data.has_next(),
    'has_previous': paginated_data.has_previous(),
    'page_number': paginated_data.number,
    'num_pages': paginated_data.paginator.num_pages,
  }

def handle_api_error():
  return HttpResponseServerError("Error in fetching anime data from the API")

def search_anime(anime_name):
  url = "https://myanimelist.p.rapidapi.com/v2/anime/search"

  results = 10
  score = 0
  
  querystring = {"q": anime_name, "n": results, "score": score}
  
  response = requests.get(url, headers=headers, params=querystring)
  
  if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
    return response.json()
  else:
    return None
  
def render_search_page(request, userAnimeListData, paginated_data, user_id):
  return render(request, 'watchlist/search.html', {
    "userAnimeListData": userAnimeListData,
    "paginated_data": paginated_data,
    "user_id": user_id
  })

def get_genre(genre_data):
  genres_list = []
  for genre_info in genre_data:
    genre_name = genre_info.get('name')
    genre, _ = Genre.objects.get_or_create(name=genre_name)
    genres_list.append(genre)
  return genres_list

def get_url(category, top=True):
  if top:
    return f"https://myanimelist.p.rapidapi.com/anime/top/{category}"
  else:
    return f"https://myanimelist.p.rapidapi.com/anime/{category}"
  
def convert_status(status):
  if status.find('_'):
    return status.replace('_', '-')
  return status