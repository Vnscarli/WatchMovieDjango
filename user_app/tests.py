from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "test132",
            "password2": "test132"
        }
        response=self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="test", 
                                           password="test132")
        
    def test_login(self):
        data ={
            "username": "test",
            "password": "test132"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)