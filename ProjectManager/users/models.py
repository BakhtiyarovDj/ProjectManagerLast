from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.dispatch import receiver
from django.utils import timezone

class User(AbstractUser,PermissionsMixin):
    role = models.CharField(max_length=20,default="captain", choices=[('project_manager', 'Loyiha sardori'),('captain', 'Jamoa sardori')])
    created_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    updated_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    deleted_at = models.CharField(max_length=20,null=True)
    
    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now().strftime('%d-%m-%Y %H:%M')
    #     self.username = timezone.now().strftime('%d-%m-%Y %H:%M')
    #     self.save()
    
    def __str__(self):
        return self.first_name +' '+ self.last_name
    

class Team(models.Model):
    class Meta:
        ordering = ["-id"]
    title = models.CharField(max_length=50)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    created_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    updated_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    deleted_at = models.CharField(max_length=20,null=True)

    
    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now().strftime('%d-%m-%Y %H:%M')
    #     self.save()

    def __str__(self):
        return self.title



class Developer(models.Model):
    fish = models.CharField(max_length=100)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    position = models.CharField(
        max_length=30,
        null=True,
        choices=[
            ('frontend', 'FrontEnd'),
            ('backend', 'BackEnd'),
            ('designer', 'Designer')
        ]
    )
    image = models.ImageField(upload_to='documents',  null=True)
    created_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    updated_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    deleted_at = models.CharField(max_length=20,null=True)

    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now().strftime('%d-%m-%Y %H:%M')
    #     self.save() 
    def update(self, *args, **kwargs):
        self.updated_at = timezone.now().strftime('%d-%m-%Y %H:%M')
        self.save()


    def __str__(self):
        return str(self.fish)
    
class SubTeam(models.Model):
    announcement = models.ForeignKey("announcements.Announcement",on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE) 
    developers = models.ManyToManyField("Developer") 
    status = models.CharField(max_length=50, choices=[('refused', 'Rad Etilgan'), ('pending', 'Jarayonda'), ('accepted', 'Qabul qilingan')], default='pending')
    created_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    updated_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    deleted_at = models.CharField(max_length=20,null=True)
    
    # def delete(self, *args, **kwargs):
    #     self.deleted_at = timezone.now().strftime('%d-%m-%Y %H:%M')
    #     self.save()
    def update(self, *args, **kwargs):
        self.updated_at = timezone.now().strftime('%d-%m-%Y %H:%M')
        self.save()

    def __str__(self):
        return self.announcement.project_name


class Employment(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE) 
    status = models.CharField(max_length=50, choices=[('busy', 'Band'), ('free', 'Bosh')], default='free')
    

class Vacancies(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE) 
    position = models.CharField(max_length=30,null=True)
    description = models.CharField(max_length=400,null=True)
    created_at = models.CharField(max_length=20,default=timezone.now().strftime('%d-%m-%Y %H:%M'))
    deleted_at = models.CharField(max_length=20,null=True)
