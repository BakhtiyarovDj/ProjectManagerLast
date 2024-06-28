from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
from django.utils import timezone
import phonenumbers
from phonenumbers import NumberParseException
from rest_framework import serializers

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='documents')
    file2 = models.FileField(upload_to='documents', null=True)
    file3 = models.FileField(upload_to='documents', null=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now()
    #     self.save()



class Announcement(models.Model):
    person = models.CharField(max_length=50, choices=[('jismoniy', 'Jismoniy shaxs'), ('yuiridik', 'Yuridik shaxs')],null=True)#
    project_name = models.CharField(max_length=100)
    deadline = models.DateField()
    cost = models.IntegerField()
    tashkilot_nomi = models.CharField(max_length=50) #
    address = models.CharField(max_length=100,null=True)#
    description = models.CharField(max_length=700)#
    phone = models.CharField(max_length=15, help_text='+998 bilan kiriting!!!')#
    name_of_employer = models.CharField(max_length=30)#
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to={'deleted_at': None}, null=True, blank=True, related_name='assignments')
    document = models.OneToOneField(Document, on_delete=models.PROTECT, limit_choices_to={'deleted_at' : None})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.project_name


    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now()
    #     self.document.delete()
    #     self.save()


    def clean(self):
        try:
            parsed_number = phonenumbers.parse(self.phone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError({'error_massage' : "Invalid phone number"})
        except NumberParseException:
            raise serializers.ValidationError({'error_massage' : "Invalid phone number format"})


    def save(self, *args, **kwargs):
        self.clean()  # This will call the clean method
        super().save(*args, **kwargs)



    # def update(self, *args, **kwargs):
    #     self.updated_at = datetime.now().strftime('%d-%m-%Y %H:%M')
    #     self.save()

    # def delete(self, *args, **kwargs):
    #     self.deleted_at = datetime.now().strftime('%d-%m-%Y %H:%M')
    #     self.save()


class WorkRequest(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, limit_choices_to={'assigned_to' : None, 'deleted_at': None}, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_requests')
    status = models.CharField(max_length=50, choices=[('refused', 'Rad Etilgan'), ('pending', 'Kutilyapti'), ('accepted', 'Qabul qilingan')], default='pending')
    deadline = models.DateField()
    cost = models.IntegerField()
    description = models.CharField(max_length=700)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    # class Meta:
    #     unique_together = ('announcement', 'requester')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'accepted':
            announcement = self.announcement
            announcement.assigned_to = self.requester
            announcement.save()
            WorkRequest.objects.filter(announcement=self.announcement).exclude(id=self.id).update(status='refused')

    def __str__(self):
        return f'Request by {self.requester.username} for {self.announcement.project_name}'

    
    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now()
    #     self.save()
