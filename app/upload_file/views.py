import json
import time
import zipfile
from io import BytesIO

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadZipFileForm

# Create your views here.


def get_file_list(zip_file):
    # クライアントから送信されたzipファイルをメモリ上に一時的に保存する
    buffer = BytesIO(zip_file.read())

    # zipファイルを解凍して、JSONファイルを取得する
    with zipfile.ZipFile(buffer, "r") as zip_ref:
        # zipファイル内の全てのファイルを取得する
        files = zip_ref.namelist()
    return files


@shared_task(bind=True)
def handle_zip_upload(self, file_list):
    print(type(self))
    # 進行状況の初期化
    progress_recorder = ProgressRecorder(self)

    total_files = len(file_list)
    # 進行状況の初期化
    progress_recorder.set_progress(0, total_files)
    print("total files: ", total_files)

    # ファイルを読み込んで、内容を取得する
    result = 0
    for idx, file in enumerate(file_list):
        # 重い処理
        print(f"Processing {file}")
        time.sleep(0.4)
        # 進行状況を更新
        print(f"Done!")
        result += 1

        progress_recorder.set_progress(idx + 1, total_files, description=f"処理中...({idx+1}/{total_files})")
    # return "File upload success!"


def upload_zip_file(request):
    if request.method == "POST":
        form = UploadZipFileForm(request.POST, request.FILES)

        if form.is_valid():
            # クライアントから送信されたzipファイルを取得する
            print("zip uploaded.")
            zip_file = request.FILES["zip_file"]
            file_list = get_file_list(zip_file)

            # handle_zip_upload()を呼び出して、zipファイルを処理する
            result = handle_zip_upload.delay(file_list)

            # zip削除
            zip_file.close()
            default_storage.delete(zip_file.name)
            print(type(result), result)
            # 処理が完了したら、リダイレクトなど適切なレスポンスを返す
            return render(request, "upload_file/upload.html", context={"form": form, "task_id": result.task_id})
    else:
        form = UploadZipFileForm()
    # GETリクエストの場合は、ファイルアップロードのフォームを表示する
    print("get@@@@@@")
    return render(request, "upload_file/upload.html", {"form": form})
