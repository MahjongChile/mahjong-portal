from django import forms

from tournament.models import Tournament


class UploadResultsForm(forms.Form):
    csv_file = forms.FileField()


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name_ru', 'name_en', 'slug', 'start_date', 'end_date',
                  'registration_description_ru', 'registration_description_en']
