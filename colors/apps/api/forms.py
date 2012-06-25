from django import forms

class UploadFilesForm(forms.Form):
    file  = forms.FileField()
    #target_image_id = forms.IntegerField()

    def clean_file(self):
        data = self.cleaned_data["file"]
        
        if data.content_type not in ['image/jpeg', 'image/png']:
            raise forms.ValidationError('Invalid file extension.')

        # Max: 5MB
        if data._size > (1024 * 1024 * 5):
            raise forms.ValidationError('Invalid file size.')

