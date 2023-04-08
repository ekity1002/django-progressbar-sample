from django import forms


class UploadZipFileForm(forms.Form):
    zip_file = forms.FileField(
        label="",
        widget=forms.ClearableFileInput(attrs={"accept": "application/zip"}),
    )
