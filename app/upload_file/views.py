import json
import time
import zipfile
from io import BytesIO

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadZipFileForm

# Create your views here.


def handle_zip_upload(zip_file):
    # クライアントから送信されたzipファイルをメモリ上に一時的に保存する
    buffer = BytesIO(zip_file.read())

    # zipファイルを解凍して、JSONファイルを取得する
    with zipfile.ZipFile(buffer, "r") as zip_ref:
        # zipファイル内の全てのファイルを取得する
        files = zip_ref.namelist()
        print(f"files in zip: ", files)
        # JSONファイルを読み込んで、内容を取得する
        for file in files:
            # アップロードしたファイルに対してなにか重い処理：sleepで代用
            time.sleep(1)

    # 一時的に保存したzipファイルを削除する
    zip_file.close()
    default_storage.delete(zip_file.name)


def upload_zip_file(request):
    if request.method == "POST":
        form = UploadZipFileForm(request.POST, request.FILES)

        if form.is_valid():
            # クライアントから送信されたzipファイルを取得する
            print("zip uploaded.")
            zip_file = request.FILES["zip_file"]

            # handle_zip_upload()を呼び出して、zipファイルを処理する
            handle_zip_upload(zip_file)

            # 処理が完了したら、リダイレクトなど適切なレスポンスを返す
            return render(request, "upload_file/success.html")
    else:
        form = UploadZipFileForm()
    # GETリクエストの場合は、ファイルアップロードのフォームを表示する
    print("get@@@@@@")
    return render(request, "upload_file/upload.html", {"form": form})
