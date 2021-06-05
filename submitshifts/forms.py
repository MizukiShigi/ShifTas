from django import forms
from django.core.exceptions import ValidationError

class SubmitShiftForm(forms.Form):

    def clean_fromtime(self):
        fromtime = self.cleaned_data.get('fromtime')
        if fromtime is not None:
            if  fromtime < 9 or fromtime > 20:
                raise forms.ValidationError('開始時間は9時~20時の間に収めてください。')
        return fromtime
    
    def clean_toime(self):
        totime = self.cleaned_data.get('totime')
        if totime is not None:
            if  totime < 10 or totime > 21:
                raise forms.ValidationError('終了時間は10時~21時の間に収めてください。')
        return totime
    
    def clean(self):
        cleaned_data = super().clean()
        fromtime = cleaned_data.get('fromtime')
        totime = cleaned_data.get('totime')
        if fromtime is not None and totime is not None:
            if fromtime > totime:
                raise forms.ValidationError('開始時間は終了時間より前にしてください。')
    
    fromtime = forms.IntegerField(required=False, validators=[clean_fromtime])
    totime = forms.IntegerField(required=False, validators=[clean_toime])