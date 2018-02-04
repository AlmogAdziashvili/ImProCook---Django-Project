from django.db import models
from django.utils.timezone import now


class Recipe(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user_pk         = models.IntegerField()
    title           = models.CharField(max_length=64)
    ingredients     = models.TextField()
    instructions    = models.TextField()
    recipe_pic      = models.ImageField()
    approved        = models.BooleanField(default=False)
    create_time     = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.title) + " by " + str(self.user_pk)

    def __unicode__(self):
        return str(self.title) + " by " + str(self.user_pk)

class Like(models.Model):
    id          = models.BigAutoField(primary_key=True)
    recipe_pk   = models.IntegerField()
    user_pk     = models.IntegerField()
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user_pk) + " likes " + str(self.recipe_pk)

    def __unicode__(self):
        return str(self.user_pk) + " likes " + str(self.recipe_pk)

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_pk = models.IntegerField()
    user_pk = models.IntegerField()
    content = models.TextField()
    create_time = models.DateTimeField(default=now)
