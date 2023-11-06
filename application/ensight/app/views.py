from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import SearchForm
from .models import *
from django.http import JsonResponse
from .serializers import*
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth import get_user_model
class HomeView(TemplateView):
    template_name = 'app/home.html'


@api_view(['POST'])
def header_search(request):
    if request.method == 'POST':
        search_query = request.data.get('content')
        print("Search Query: ", search_query)
        movie_results =  Movie.objects.filter(Q(title__icontains=search_query))
        movie_serializer = MovieSerializer(movie_results, many=True)
     
        review_results =  Review.objects.filter(
            Q(title__icontains=search_query) |  # Search by title (case-insensitive)
            Q(text__icontains=search_query) |   # Search by text (case-insensitive)
            Q(author__username__icontains=search_query)  # Search by author's username (case-insensitive)
            # You can add more criteria based on your needs
        )
    
        reviews_serializer = ReviewSerializer(review_results, many=True)
      
        users_results = Profile.objects.filter(Q(user__username__icontains=search_query))
    
        user_serializer = ProfileSerializer(users_results,many=True)
   
        data = {
            'movies': movie_serializer.data,
            'reviews': reviews_serializer.data,
            'users': user_serializer.data,
        }
     
        return Response(data)

#this fetch call returns all movies that contain whatever the user searched in the title
@api_view(['POST'])
def search_movies(request):
    if request.method == 'POST':
        search_query = request.data.get('content')  # Get the search query from the request data
        print(f"Search Query: {search_query}")

        # Search for movies that match the query in their title or description
        search_results = Movie.objects.filter(Q(title__icontains=search_query))

        print (search_results[0].poster_path)
        # Serialize the search results
        serializer = MovieSerializer(search_results, many=True)

        return Response(serializer.data)

@api_view(['POST'])
def search_users(request):
    if request.method == 'POST':
        search_query = request.data.get('content')
        print(f"Search Query: {search_query}")
        users = Profile.objects.filter(
            Q(user__username__icontains=search_query))
        
        serializer = ProfileSerializer(users,many=True)
        user_profiles = [
            {
                'username': user.user.username,
             }
             for user in users
        ]
        return Response(serializer.data)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=400)

#This allows users to create a list with whatever movies they want
@api_view(['POST'])
def create_movie_list(request):
    if request.method == 'POST':
        serializer = CreateMovieListSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new movie list
            movie_list=serializer.save()
            movie_ids = request.data.get('movie_ids',[])
            for movie_id in movie_ids:
                movie = Movie.objects.get(pk=movie_id)
                MovieListThrough.objects.create(movie=movie, movie_list=movie_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#fetch username, user's bio and user's privacy status
#def getUserInfo(request):
    

#get's user's list(all of it). STILL NEEDS WORK because it doesn't know which user it is
def get_all_user_list(request):
    movie_list = MovieList.objects.all()
    serializer = MovieListSerializer(movie_list, many=True)
    return JsonResponse(serializer.data, safe=False)

#fetches first movie
@api_view(['POST'])
def fetch_movies(request):
    filter = request.data.get('filter')
    index = request.data['amount']
    
    movies=[]
    if filter == 'highest_rated':
        movies = Movie.objects.order_by('-rating_average')[:index]
        serializer = MovieSerializer(movies, many=True)
    # movie_data = []
    # for movie in movies:
    #     movie_data.append({
    #         'title': movie.title,
    #         'rating_average': movie.rating_average,
    #         # Add other movie details you want to include
    #     })
    
    return Response(serializer.data)





def home(request):
    movie_list = Movie.objects.order_by('-release_date')[:10]
    return render(request, 'app/home.html', {'movie_list': movie_list})

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_type = form.cleaned_data['search_type']
            
            if search_type == 'movie':
                results = Movie.objects.filter(title__icontains=query)
            elif search_type == 'user':
                results = Review.objects.filter(author__username__icontains=query)
            
            return render(request, 'app/home.html', {'results': results, 'search_type':search_type, 'form': form})
    else:
        form = SearchForm()
    
    return render(request, 'app/home.html', {'form': form})