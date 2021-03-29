import os 
import subprocess
import codecs
from subprocess import CalledProcessError

from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import StreamingHttpResponse, HttpResponse
from server.tail import Tail
# Create your views here.

def get_abs_path(req_path):
    BASE_LOG_FILE_DIR = '/home/sant/Desktop/Untitled Folder 3/bstack/logquack/logs'
    file_path = os.path.join(BASE_LOG_FILE_DIR, req_path)
    return file_path


def log_stream(request, req_path=None):
    file_path = get_abs_path(req_path)
    def event_stream():
        tail = Tail(file_path)
        l = tail.follow()
        while True:
            line = next(l)
            yield line
    
    if os.path.isfile(file_path):
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    
    return HttpResponse("<h1> not a path </h1>", 400)


def search_file(request, req_path=None):
    file_path = get_abs_path(req_path)
    search_query = request.GET.get("query")
    try:
        match = subprocess.check_output(['grep', search_query, file_path])
    except CalledProcessError:
        return HttpResponse("some error has occured", 400)
    match = codecs.decode(match, "UTF-8")
    match = match.split("\n")
    return HttpResponse('<br/>'.join(match))


def file_router(request, req_path=None):
    abs_path = get_abs_path(req_path)

    if not os.path.exists(abs_path):
        return HttpResponse("<h1> does not exist</h1>", 404)

    if os.path.isfile(abs_path):
        return log_stream(request, req_path=req_path)
    
    contents = os.listdir(abs_path)
    # import pdb; pdb.set_trace()
    

    return render(request, 'list.html', {'files': contents, 'request': request})