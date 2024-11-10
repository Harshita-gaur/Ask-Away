from django.db import models
# from django.contrib.auth.models import User

class NameModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='%(class)s_created_by', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)

    class Meta:
        abstract = True

class CategoryFAQ(TimeStampedModel, NameModel):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    FAQ_count=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.category

class TagFAQ(TimeStampedModel, NameModel):
    id = models.AutoField(primary_key=True)
    Tags = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.Tags

class FAQ(TimeStampedModel, NameModel):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category= models.ForeignKey(CategoryFAQ, related_name='faqs', on_delete=models.CASCADE)
    Tags = models.ManyToManyField(TagFAQ, related_name='tags', blank=True)
    def __str__(self):
        return self.question

class Feedback(TimeStampedModel, NameModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')]) 
    comment = models.TextField(blank=True, null=True) 
    is_helpful = models.BooleanField(default=True)
    faq = models.ForeignKey(FAQ, related_name='feedback',on_delete=models.CASCADE) 
    def __str__(self):
        return f"Feedback by {self.user} for {self.faq.question} :{'Helpful' if self.is_helpful else 'Not Helpful'} ;Rating : {self.rating} ; Comment:{self.comment}"

