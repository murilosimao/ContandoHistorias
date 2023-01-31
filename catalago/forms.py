from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Review

class AvaliarReviewForm( forms.Form ):

  status = forms.ChoiceField(choices=Review.ReviewStatus.choices, required=True, help_text="Status da review")

  def __init__(self, *args, **kwargs ):
    super().__init__( *args, **kwargs )
    self.helper = FormHelper(self)
    self.helper.add_input(Submit('submit', 'Salvar Avaliação', css_class='btn-primary'))








 