from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
    def get_best(self):
        profiles = self.all()[:5]
        return [p.user for p in profiles]
class QuestionManager(models.Manager):
    def get_hot(self):
        return self.all()[:10]
    def get_new(self):
        return self.order_by("-created_at")
    def get_by_tag(self, tag):
        #tags = Tag.objects.filter(name=tag)
        return self.filter(tag__name=tag)
class AnswerManager(models.Manager):
    def get_new(self, question_id):
        return self.filter(question=question_id).order_by("created_at")[:11]
class LikeManager(models.Manager):
    def get_new(self, question_id):
        return self.filter(question=question_id).order_by("created_at")
class TagManager(models.Manager):
    def get_best(self):
        return self.order_by("rating")[:10]
    def get_tags(self, question):
        return self.filter(question__id=question)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    objects = ProfileManager()
class Tag(models.Model):
    name = models.CharField(max_length=30)
    rating = models.IntegerField(default=0)
    objects = TagManager()
    def __str__(self):
        return self.name
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [("l", "like"), ("d", "dislike")]
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    objects = LikeManager()
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    like = models.ManyToManyField(Like, blank=True)
    objects = QuestionManager()
    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like = models.ManyToManyField(Like, blank=True)
    objects = AnswerManager()
    def __str__(self):
        return self.text





