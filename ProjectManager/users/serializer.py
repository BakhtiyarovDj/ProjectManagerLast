from rest_framework import serializers
from .models import *
from announcements.models import Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name','last_name','role','created_at','updated_at','deleted_at')
        read_only_fields = ['url','created_at','updated_at','deleted_at']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class TeamSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta: 
        model = Team 
        fields = ['id','title','user','created_at','updated_at','deleted_at']
        read_only_fields = ['created_at','updated_at','deleted_at']


class SubTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTeam
        fields = ['id','url','announcement','status','team','developers','created_at','updated_at','deleted_at']
        read_only_fields = ['created_at','updated_at','deleted_at']

    # def validate(self, data):
    #     team = data.get('team', None)
    #     announcement = data.get('announcement')
    #     developers = data.get('developers', None)

    #     if SubTeam.objects.filter(announcement=announcement, deleted_at__isnull = True).exists():
    #         raise serializers.ValidationError({"error_message":"Tanlangan loyihani boshqalar bajarayapti"})

    #     for ids in developers:
    #         if str(ids.team.id) != str(team.id):
    #             raise serializers.ValidationError({"error_message":"Ushbu dasturchi(lar) tanlangan jamoaga tegishli emas"})

    #     return data

    

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id','url','fish','team','position','image','created_at','updated_at','deleted_at')
        read_only_fields = ['created_at','updated_at','deleted_at']
    
    
class DevelopersFromTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = Developer
        fields = ('id','url','fish','team','position','image','created_at','updated_at','deleted_at')
        read_only_fields = ['created_at','updated_at','deleted_at']


class EmploymentSerializer(serializers.ModelSerializer):
    team = TeamSerializer
    class Meta:
        model = Employment
        fields = ('id','team','status')


class VacanciesSerializer(serializers.ModelSerializer):
    team = TeamSerializer
    class Meta:
        model = Vacancies
        fields = ('id','team','position','description','created_at','deleted_at')
        read_only_fields = ['created_at','deleted_at']
