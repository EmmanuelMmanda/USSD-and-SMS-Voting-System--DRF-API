from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class Voter(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    university_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    has_vote = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='voter')

    def __str__(self):
        return f"{self.user} ({self.university_id})"
    
    def create_token(self):
        token = Token.objects.create(user=self.user)
        return token.key

    class Meta:
        verbose_name = "Voter"
        verbose_name_plural = "Voters"


class Election(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    voters = models.ManyToManyField(Voter, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Election"
        verbose_name_plural = "Elections"


class Position(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.election.title})"

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"


class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    manifesto = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    unique_together = ('first_name', 'last_name', 'position')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    time_cast = models.DateTimeField(default=timezone.now)
    vote_value = models.IntegerField(default=1, editable=False)

    UNIQUE_TOGETHER = ('voter', 'Position', 'candidate')

    class Meta:
        unique_together = ('voter','Position', 'candidate')

    def __str__(self):
        return f"{self.voter} voted for {self.candidate}"
    
class Results(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    vote_percentage = models.FloatField(default=0.0)
    unique_together = ('election', 'position', 'candidate')

    def __str__(self):
        return f"{self.candidate} ({self.position})"

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

class Settings(models.Model):
    language = models.CharField(max_length=100, default='EN')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    unique_together = ('key', 'user') 

    