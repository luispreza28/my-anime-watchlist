from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json
from django.http import JsonResponse, HttpResponseServerError
from .models import User, UserAnimeList, Anime
import logging
from .utils import get_user_anime_list_by_status, get_status_count, get_paginated_data, get_recommended_anime, add_anime_to_database, fetch_detailed_anime_data, make_api_request, validate_user, register_user,is_ajax_request,generate_ajax_response,handle_api_error,search_anime, render_search_page,get_genre,convert_status,get_url
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


X_RAPIDAPI_KEY = 'a91c7434eemsh0a1161df1519403p1f2fe2jsnf218290f6e7d'
X_RAPIDAPI_HOST = 'myanimelist.p.rapidapi.com'


# Create your views here.
@login_required
def index_views(request):
  user = request.user
  if request.method == "GET":
    items_per_page = 4

    recommended_animes = get_recommended_anime(user)
    if (recommended_animes):
      paginated_data = get_paginated_data(recommended_animes, items_per_page, request)
      print(paginated_data)
    else:
      paginated_data = None

    return render(request, "watchlist/index.html",{
      "user": user,
      "paginated_data": paginated_data,
    })

@csrf_protect
def login_views(request):
  if request.method == 'POST':
    user = validate_user(request)

    # check if user is valid
    if user:
      return HttpResponseRedirect(reverse('index'))
    
    else:
      return render(request, 'watchlist/login.html', {
        "message": "Invalid username and/or password."
      })
    
  else:
    return render(request, 'watchlist/login.html')
  
def logout_views(request):
  # logout user
  logout(request)
  return render(request, 'watchlist/login.html')

def register_views(request):
  if request.method == 'POST':
    user = register_user(request)
    
    if not user:
      # return user back to register form if password doesnt match with confirmation
      return render(request, 'watchlist/register.html', {
        "message": "passwords did not match. Try again."
      })
    
    # login user
    login(request, user)
    return HttpResponseRedirect(reverse('index'))
  
  else:
    return render(request, 'watchlist/register.html')


def fetch_anime_views(request, user_id):
  if request.method == 'GET':
    # get users anime list
    users_list = UserAnimeList.objects.filter(user=request.user)

    # create user anime list data
    userAnimeListData = [{'anime': anime, 'status': anime.status, "myanimelist_id": anime.anime.myanimelist_id} for anime in users_list]

    anime_name = request.GET.get('anime-name', '')
    
    search_results = search_anime(anime_name)
    

    if search_results:
      paginated_data = get_paginated_data(search_results, 5, request)

      if is_ajax_request(request):
        return generate_ajax_response(paginated_data)
      else:
        return render_search_page(request, userAnimeListData, paginated_data, user_id)
    else:
      return handle_api_error()

def search_views(request):
  if request.method == 'GET':
    # get users anime list
    usersList = UserAnimeList.objects.filter(user=request.user)

    # get user id
    user_id = request.user.id

    # create user anime list data
    userAnimeListData = [{'anime': anime, 'status': anime.status, "myanimelist_id": anime.anime.myanimelist_id} for anime in usersList]

    return render(request, 'watchlist/search.html', {
      "userAnimeListData": userAnimeListData,
      "user_id": user_id,
    })
  
def profile_views(request, user_id):
  if request.method == 'GET':
    user = request.user

    currently_watching_count = get_status_count(user, "currently_watching")
    completed_count = get_status_count(user, "completed")
    on_hold_count = get_status_count(user, "on_hold")
    dropped_count = get_status_count(user, "dropped")
    plan_to_watch_count = get_status_count(user, "plan_to_watch")

    return render(request, 'watchlist/profile.html', {
      "user": user,
      "currently_watching_count": currently_watching_count,
      "completed_count": completed_count,
      "on_hold_count": on_hold_count,
      "dropped_count": dropped_count,
      "plan_to_watch_count": plan_to_watch_count,
    })
  
# Handles every type of watchlist
def watchlist_views(request, user_id, status=None):
  if request.method == 'GET':
    STATUS_CHOICES = UserAnimeList.STATUS_CHOICES
    user = request.user

    if status is None:
      users_list = get_user_anime_list_by_status(user, 'all')
    else:
      users_list = get_user_anime_list_by_status(user, status)
      status = convert_status(status)
      
    items_per_page = 4
    paginated_data = get_paginated_data(users_list, items_per_page, request)

    return render(request, f'watchlist/{status}.html' if status else 'watchlist/all-anime-watchlist.html', {
      'user': user,
      'paginated_data': paginated_data,
      'users_list': users_list,
      'STATUS_CHOICES': STATUS_CHOICES,
    })
  elif request.method == 'POST':
    data = json.loads(request.body)
    user_id = data.get('user_id')
    anime_id = data.get('anime_id')
    user = User.objects.get(pk=user_id)
    anime = Anime.objects.get(myanimelist_id=anime_id)
    action = data.get('action')

    if action == "episode":
      current_episode = data.get('progress')
      UserAnimeList.objects.filter(user=user, anime=anime).update(progress=current_episode)
      return JsonResponse({"message": f"Successfully updated current episode. Anime: {anime}, User: {user}, Current Episode: {current_episode}"})
    
    elif action == "rating":
      new_rating = data.get('rating')
      UserAnimeList.objects.filter(user=user, anime=anime).update(rating=new_rating)
      return JsonResponse({"message": f"Successfully updated rating: {new_rating} for anime: {anime}"})
  else:
    return HttpResponseBadRequest("Invalid request method")
  
# add anime to watchlist view
def add_anime_views(request, user_id):
  if request.method == 'POST':
    data = json.loads(request.body)

    # Extract data from request
    anime_id = data.get('my_anime_list_id')
    anime_title = data.get("title")
    anime_description = data.get("description")
    anime_url = data.get("my_anime_list_url")
    anime_picture_url = data.get("picture_url")
    anime_genre = data.get('genre')

    # Retrieve or create anime entry
    anime_entry, created = Anime.objects.get_or_create(
      title = anime_title,
      defaults={
        'myanimelist_id': anime_id,
        'description': anime_description,
        'myanimelist_url': anime_url,
        'picture_url': anime_picture_url,
      }
    )

    if created:
      # Fetch detailed anime data if newly created
      detailed_anime_data = fetch_detailed_anime_data(anime_id, request)
      genre_data = detailed_anime_data.get('information', {}).get('genres', [])

      # Create or rerieve genre objects
      genres_list = get_genre(genre_data)
      
      # Set genres for the anime entry
      anime_entry.genre.set(genres_list)
    
    # Check if the anime is already in the user's watchlist
    if UserAnimeList.objects.filter(user_id=user_id, anime=anime_entry).exists():
      return JsonResponse({'message': 'Anime already in watchlist'})
    
    # Add anime to users watchlist
    new_watchlist = UserAnimeList.objects.create(
      user_id=user_id,
      anime=anime_entry,
      status='plan_to_watch',
      progress=1,
      myanimelist_id=anime_id,
    )
    
    return JsonResponse({'message': 'Anime added to watchlist successfully'})
      
# remove anime from users watchlist
def remove_anime_views(request, anime_title):
  if request.method == "POST":
    data = json.loads(request.body)
    anime_title = data.get('anime_title')
    user = request.user

    try:
      anime = Anime.objects.get(title=anime_title)
      user_watchlist = UserAnimeList.objects.get(user=user,anime=anime)
      user_watchlist.delete()
      return JsonResponse({'message': 'Anime removed from watchlist successfully'})
    except Anime.DoesNotExist:
      return JsonResponse({'message': 'Anime not found'}, status=404)
    except UserAnimeList.DoesNotExist:
      return JsonResponse({'message': 'Anime not found in watchlist'}, status=404)
    except Exception as e:
      logging.error(f"Error removing anime: {str(e)}")
      return HttpResponseServerError('Internal Server Error', status=500)
  
def get_anime_views(request, anime_id):
  if request.method == 'GET':
    try:
      anime = Anime.objects.get(myanimelist_id=anime_id)
      anime_data = {
        'title': anime.title,
        'description': anime.description,
        'my_anime_list_url': anime.myanimelist_url,
        'picture_url': anime.picture_url,
        'myanimelist_id': anime.myanimelist_id,
        "genre": list(anime.genre.values_list('name', flat=True)),
      }
      response_data = {
        'success': True,
        'anime': anime_data,
      }
      return JsonResponse(response_data)
    
    except Anime.DoesNotExist:
      anime_response = fetch_detailed_anime_data(anime_id, request)
      anime_title = anime_response.get('title_ov')
      anime_description = anime_response.get('synopsis', '')
      genre_data = anime_response.get('information', {}).get('genres', [])
      picture_url = anime_response.get('picture_url', '')
      myanimelist_url = anime_response.get('information', {}).get('premiered',[{}][0].get('url', ''))
      genres_list = get_genre(genre_data)
      try:
        anime_entry = Anime.objects.create(
          myanimelist_id=anime_id,
          picture_url=picture_url,
          myanimelist_url=myanimelist_url,
          title=anime_title,
          description=anime_description,
        )
        anime_entry.genre.set(genres_list)
        anime_data = {
          "title": anime_entry.title,
          "description": anime_entry.description,
          "my_anime_list_url": anime_entry.myanimelist_url,
          "picture_url": anime_entry.picture_url,
          "myanimelist_id": anime_entry.myanimelist_id,
          "genre": list(anime_entry.genre.values_list('name', flat=True)),
        }
        response_data = {
          "success": True,
          "anime": anime_data,
        }
        return JsonResponse(response_data)
      except Exception as e:
        logging.error(f"Error creating anime entry: {str(e)}")
        return JsonResponse({"success": False, "message": "An error occurred while creating anime entry"}, status=500)
    except Exception as e:
      logging.error(f"Error fetching anime: {str(e)}")
      return JsonResponse({"success": False, "message": "An error occurred while fetching anime"}, status=500)

def change_status_views(request, user_id):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      status = data.get('select_status')
      anime_id = data.get('anime_id')
      user = get_object_or_404(User, pk=user_id)
      anime = get_object_or_404(Anime, myanimelist_id=anime_id)

      # Update the status in the database
      UserAnimeList.objects.filter(user=user, anime=anime).update(status=status)
      return JsonResponse({"message": "Successfully updated anime status"})
    
    except User.DoesNotExists:
      return JsonResponse({"message": "User not found"}, status=404)
    except Anime.DoesNotExist:
      return JsonResponse({"message": "Anime not found"}, status=404)
    except Exception as e:
      logging.error(f"Error updating status: {str(e)}")
      return JsonResponse({"message": "Error updating status"}, status=500)
  else:
    return JsonResponse({"message": "Invalid request method"}, status=400)

def every_anime_views(request):
  if request.method == "GET":

    every_anime = Anime.objects.all()

    user_id = request.user.id
    
    items_per_page = 4

    paginated_data = get_paginated_data(every_anime, items_per_page, request)

    return render(request,"watchlist/every-anime.html", {
      "every_anime": every_anime,
      "paginated_data": paginated_data,
      "user_id": user_id,
    })
  
# Populate Anime list with more animes
def populate_views(request, category, top):
  if request.method == 'GET':
    url = get_url(category, top)
    response = make_api_request(url)
    add_anime_to_database(response, request)
  else:
    return HttpResponseBadRequest("Invalid request method")
