from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User,Team,Developer,SubTeam 
from .serializer import *
from .permissions import *
from django.contrib.auth import authenticate 
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [IsProjectManager]


class TeamCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    def get_queryset(self):
        return Team.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsProjectManager]

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_at = timezone.now().strftime('%d-%m-%Y %H:%M')
        instance.save()
        return super().update(request, *args, **kwargs)

class TeamWithUserIDView(generics.ListAPIView):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamSerializer
    def get_queryset(self):
        user_id = self.kwargs['pk']
        self.queryset = self.queryset.filter(user=user_id,deleted_at__isnull=True)
        return self.queryset
    permission_classes = [IsAuthenticated]

@csrf_exempt
def create_team_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role','captain')
            team_title = data.get('title')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            if not username or not password or not team_title:
                return JsonResponse({'message': 'Maydonlarni to`ldiring'}, status=200)
            if Team.objects.filter(title=team_title, deleted_at__isnull=True).exists():
                return JsonResponse({'message': "Ushbu kiritilgan jamoa nomi allaqachon band bo'lgan"}, status=200)


            user = User.objects.create_user(username=username, password=password, role=role, first_name=first_name,last_name=last_name)
            user.created_at = timezone.now().strftime('%d-%m-%Y %H:%M')
            user.updated_at = timezone.now().strftime('%d-%m-%Y %H:%M')
            user.save()
            # Create team
            team = Team.objects.create(title=team_title, user=user)
            team.created_at = timezone.now().strftime('%d-%m-%Y %H:%M')
            team.updated_at = timezone.now().strftime('%d-%m-%Y %H:%M')
            team.save()

            return JsonResponse({'message': 'Team and user created successfully','team':team}, status=200)
        except Exception as e:
            if 'username' in str(e):
                return JsonResponse({'message': "Ushbu kiritilgan username allaqachon band bo'lgan"}, status=200)



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated]

class SubTeamCreateAPIView(generics.ListCreateAPIView):
    queryset = SubTeam.objects.all()
    
    serializer_class = SubTeamSerializer
    def get_queryset(self):
        return SubTeam.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]

class SubTeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTeam.objects.all()
    serializer_class = SubTeamSerializer
    permission_classes = [IsAuthenticated]

class SubTeamWithTeamView(generics.ListAPIView):
    serializer_class = SubTeamSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        team = Team.objects.get(pk=id,deleted_at__isnull=True)
        return SubTeam.objects.filter(team=team,deleted_at__isnull=True)

    permission_classes = [IsCaptain]
    
class DeveloperCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DeveloperSerializer 
    def get_queryset(self):
        return Developer.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]

class DeveloperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer 
    permission_classes = [IsAuthenticated]

class DevelopersFromTeamAPIView(generics.ListAPIView):
    serializer_class = DevelopersFromTeamSerializer 
    def get_queryset(self):
        id = self.kwargs['pk']
        teamtitle = self.kwargs['teamtitle']
        team = Team.objects.get(pk=id,title=teamtitle,deleted_at__isnull=True)
        return Developer.objects.filter(team=team,deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]

class LoginView(generics.ListAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'message': 'true', 'role': f'{user.role}', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "false"}, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class GetTeamFromUserIDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            team = Team.objects.get(user=user)
            serializer = TeamSerializer(team)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status":"good"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"status":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        
    
class EmploymentAPIView(generics.ListCreateAPIView):
    queryset = Employment.objects.all()
    permission_classes = []
    serializer_class = EmploymentSerializer     
        
class EmploymentChangeAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employment.objects.all()
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        employment = get_object_or_404(Employment, team=pk)
        employment.status = request.data.get('status')
        employment.save()
        print(employment.status)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
        

class VacanciesAPIView(generics.ListCreateAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer
    permission_classes = [IsAuthenticated]

class VacanciesDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer 
    permission_classes = [IsAuthenticated]
    