from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def runAPI(request):
    import json
    from pic.oda import object_detection_app as oap
    api_response = {"success"}
    return Response(api_response)



# Create your views here.



def run(request):
    import sys
    sys.path.append("/home/rajath/api1/yolo/pic/")
    from pic.oda import object_detection_app as oap
    #oap()
    #os.system('python /home/ubuntu/api1/yolo/pic/oda/object_detection_app.py')

    return HttpResponse("end")
