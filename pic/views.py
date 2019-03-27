from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def runAPI(request):
    if request.method=='POST':
        import json
        from pic.oda import object_detection_app as oap
        from pic.oda import img
        received_json_data = json.loads(request.body.decode("utf-8"))
        #oap.run(received_json_data['pic'])
        enc_image=img.send()
        api_response={"success"}
    else:
        api_response={"failure"}
    return Response(api_response)

# Create your views here.

@api_view(['POST'])
def sample_view(request):
    import json
    if request.method=='POST':
        json_data = json.loads(request.body.decode("utf-8"))
        print(json_data['pic'])
        api_response={"successful"}
        return Response(api_response)

def run(request):
    import sys
    sys.path.append("/home/rajath/api1/yolo/pic/")
    from pic.oda import object_detection_app as oap
    #oap()
    #os.system('python /home/ubuntu/api1/yolo/pic/oda/object_detection_app.py')
    return HttpResponse("end")
