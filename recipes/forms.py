from django import forms
from .models import Recipe, Comment

class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["id", "title", "ingredients", "instructions", "recipe_pic"]
        exclude = []

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["id", "content"]
        exclude = []
