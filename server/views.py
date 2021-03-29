import os 

from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import StreamingHttpResponse, HttpResponse
from server.tail import Tail
# Create your views here.

def stream_log(request, req_path=None):
    BASE_DIR = '/home/sant/Desktop/Untitled Folder 3/bstack/logquack/logs'
    file_path = os.path.join(BASE_DIR, req_path)
    
    def event_stream():
        tail = Tail(file_path)
        l = tail.follow()
        while True:
            line = next(l)
            yield line
    
    if os.path.isfile(abs_path):
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    
    return HttpResponse("<h1> not a path </h1>")


def file_router(request, req_path=None):
    BASE_DIR = '/home/sant/Desktop/Untitled Folder 3/bstack/logquack/logs'
    abs_path = os.path.join(BASE_DIR, req_path)

    if not os.path.exists(abs_path):
        return HttpResponse("<h1> does not exist</h1>")

    if os.path.isfile(abs_path):
        return HttpResponse("<h1> it worked </h1>")

    contents = os.listdir(abs_path)
    return 