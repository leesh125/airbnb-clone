from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)  # view에서 사용하기 위해
        return review
