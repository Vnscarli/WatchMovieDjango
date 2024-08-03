from django.contrib.auth.models import User
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamingPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test132")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.platform = models.StreamingPlatform.objects.create( name="Test Platform",
                                                                about= "Testing creating",
                                                                website= "https://www.django-rest-framework.org/")
        
    def test_streamingplatform_create(self):
        data = {
            "name": "Test Platform",
            "about" : "Testing creating",
            "website": "https://www.django-rest-framework.org/"
        }
        response=self.client.post(reverse('streamingplatform-list'),  data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamingplatform_list(self):
        response = self.client.get(reverse('streamingplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamingplatform_detail(self):
        response = self.client.get(reverse('streamingplatform-detail', args=(self.platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class MovieTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="test", password="test132")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.platform = models.StreamingPlatform.objects.create( name="Test Platform",
                                                                about= "Testing creating",
                                                                website= "https://www.django-rest-framework.org/")
        
        self.movie = models.Movie.objects.create(name= "TestMovie",
                                                description= "Testing Movie",
                                                active= True,
                                                ageRestriction= 12,
                                                genre= "Testing",
                                                platform= self.platform)
    
    def test_movie_create(self):
        data = {
            "name": "TestMovie",
            "description": "Testing Movie",
            "active": True,
            "ageRestriction": 12,
            "genre": "Testing",
            "platform": self.platform
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_movie_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_movie_detail(self):
        response = self.client.get(reverse('movie-detail', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Movie.objects.get().name, 'TestMovie')
        

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="test", password="test132")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.platform = models.StreamingPlatform.objects.create( name="Test Platform",
                                                                about= "Testing creating",
                                                                website= "https://www.django-rest-framework.org/")
        
        self.movie = models.Movie.objects.create(name= "TestMovie",
                                                description= "Testing Movie",
                                                active= True,
                                                ageRestriction= 12,
                                                genre= "Testing",
                                                platform= self.platform)
        self.movie2 = models.Movie.objects.create(name= "TestMovie2",
                                                description= "Testing Movie Again",
                                                active= True,
                                                ageRestriction= 14,
                                                genre= "Testing Again",
                                                platform= self.platform)
        
        self.review = models.Review.objects.create(editor=self.user,
                                                   rating = 7,
                                                   movies = self.movie) 
        
    def test_review_create(self):
        data = {
            "editor": self.user,
            "rating": 4,
            "movies": self.movie2
        }
        
        response = self.client.post(reverse('reviews-create', args=(self.movie2.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    
        
        response = self.client.post(reverse('reviews-create', args=(self.movie2.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_review_create_unauth(self):
        data = {
            "editor": self.user,
            "rating": 4,
            "movies": self.movie2
        }
        
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('reviews-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
    
    def test_review_update(self):
        data = {
            "editor": self.user,
            "rating": 5,
            "movies": self.movie
        }
        response = self.client.put(reverse('reviews-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('reviews-list', args= (self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_detail(self):
        response = self.client.get(reverse('reviews-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response=self.client.get('/watchlist/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)