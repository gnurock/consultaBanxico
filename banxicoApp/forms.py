from django import forms

class DateForm(forms.Form):
    fecha_ini = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    fecha_fin = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("fecha_ini")
        end_date = cleaned_data.get("fecha_fin")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")