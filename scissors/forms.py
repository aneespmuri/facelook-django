from datetime import datetime

from django import forms
from .models import DateTimeSlots


class BulkCreateSlotsForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'class': 'form-control', 'placeholder': '04:00 PM'})
    )
    end_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'class': 'form-control', 'placeholder': '04:00 PM'}, )
    )
    status = forms.ChoiceField(choices=DateTimeSlots.choice_fields,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DateTimeSlots
        fields = ('start_date', 'end_date', 'start_time', 'end_time', 'status')

    def clean_start_time(self):
        val = self.cleaned_data['start_time']
        if isinstance(val, str):  # Just in case
            return datetime.strptime(val, '%I:%M %p').time()
        return val

    def clean_end_time(self):
        val = self.cleaned_data['end_time']
        if isinstance(val, str):
            return datetime.strptime(val, '%I:%M %p').time()
        return val
