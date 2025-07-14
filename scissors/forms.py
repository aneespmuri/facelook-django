from django import forms
from .models import DateTimeSlots


class BulkCreateSlotsForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'class': 'form-control'})
    )
    end_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(choices=DateTimeSlots.choice_fields, widget=forms.Select(attrs={'class': 'form-control'}))