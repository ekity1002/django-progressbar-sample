from django.urls import include, path

from .views import upload_zip_file

app_name = "upload_file"  # アプリ名を指定する

urlpatterns = [path("", upload_zip_file, name="upload")]
