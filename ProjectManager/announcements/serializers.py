from rest_framework import serializers
from .models import Announcement, Document, WorkRequest
from datetime import timedelta
from users.models import *


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'file',
            'file2',
            'file3',
            'deleted_at',
        ]
        read_only_fields = [
            "id",
            'deleted_at',
        ]

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        return document





class AnnouncementSerializer(serializers.ModelSerializer):
    formatted_datetime = serializers.SerializerMethodField()
    document = DocumentSerializer()
    assigned_to_team = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id',
            'url',
            'person',
            'tashkilot_nomi',
            'address',
            'phone',
            'name_of_employer',
            'project_name',
            'deadline',
            'cost',
            'description',
            'assigned_to_team',
            'assigned_to',
            'document',
            'formatted_datetime',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = [
            "id",
            'assigned_to',
            'document',
            'formatted_datetime',
            'updated_at',
            'deleted_at',
        ]
    

    def get_formatted_datetime(self, obj):
    # Assuming you want to format the deadline field and add 5 hours
        adjusted_datetime = obj.created_at + timedelta(hours=5)
        return adjusted_datetime.strftime('%d-%m-%Y %H:%M')
    
    def create(self, validated_data):
        document_data = validated_data.pop('document')
        document = Document.objects.create(**document_data)
        announcement = Announcement.objects.create(document=document, **validated_data)
        return announcement
    
    def update(self, instance, validated_data):
        document_data = validated_data.pop('document', None)
        
        if document_data:
            document = instance.document
            for attr, value in document_data.items():
                setattr(document, attr, value)
            document.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    
    def get_assigned_to_team(self, obj):
        user = obj.assigned_to
        if user:
            team = Team.objects.filter(user=user).first()
            if team:
                return team.title
        return None



class AnnouncementForCaptainSerializer(serializers.ModelSerializer):
    formatted_datetime = serializers.SerializerMethodField()
    document = DocumentSerializer()
    class Meta:
        model = Announcement
        fields = [
            'id',
            'project_name',
            'deadline',
            'cost',
            'description',
            'assigned_to',
            'document',
            'formatted_datetime',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = [
            "id",
            'assigned_to',
            'document',
            'formatted_datetime',
            'updated_at',
            'deleted_at',
        ]


    def get_formatted_datetime(self, obj):
    # Assuming you want to format the deadline field and add 5 hours
            adjusted_datetime = obj.created_at + timedelta(hours=5)
            return adjusted_datetime.strftime('%d-%m-%Y %H:%M')


class WorkRequestSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()    
    announcement = AnnouncementSerializer()
    
    class Meta:
        model = WorkRequest
        fields = [
            'id',
            'url',
            'announcement',
            'requester',
            'deadline',
            'cost',
            'description',
            'status',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
    def get_created_at(self, obj):
        adjusted_datetime = obj.created_at + timedelta(hours=5)
        return adjusted_datetime.strftime('%d-%m-%Y %H:%M')


class WorkRequestSerializerWithOutAnn(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()    
    
    class Meta:
        model = WorkRequest
        fields = [
            'id',
            'url',
            'announcement',
            'requester',
            'deadline',
            'cost',
            'description',
            'status',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
    def get_created_at(self, obj):
        adjusted_datetime = obj.created_at + timedelta(hours=5)
        return adjusted_datetime.strftime('%d-%m-%Y %H:%M')
