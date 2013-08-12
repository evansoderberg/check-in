from check_in.models import Entry
from check_in.serializers import EntrySerializer
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import httplib
import json

class CheckinList(APIView):

    def get(self, request, format=None):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EntrySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_data_from_ip(ip):
    conn = httplib.HTTPConnection("freegeoip.net")
    conn.request("GET", "/json/%s" % ip)
    res = conn.getresponse()
    res_text = res.read()
    data = json.loads(res_text)
    parsed = {}
    parsed['city'] = data['city']
    parsed['lat'] = data['latitude']
    parsed['lon'] = data['longitude']
    return parsed

def add_entry(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse(status=400)
        # get the ip from the request
        ip = str(request.META['HTTP_X_FORWARDED_FOR'])
        data['ip'] = ip
        parsed = get_data_from_ip(ip)
        data['city'] = parsed['city']
        data['lat'] = parsed['lat']
        data['lon'] = parsed['lon']
        
        try:
            serializer = EntrySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
        except:
            return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=405)


class CheckinDetail(APIView):

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        entry = self.get_object(pk)
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        entry = self.get_object(pk)
        serializer = EntrySerializer(entry, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# def add_entry(request):
#     errors = {'error': 'email previously registered'}
#     if request.method == 'POST':
#         try:
#             city = request.POST.get('city')
#         except:
#             errors[error] = "city error"
#             return HttpResponse(errors, status=403)
#         try:
#             description = request.POST.get('description')
#         except:
#             errors[error] = "description error"
#             return HttpResponse(errors, status=403)
#         try:
#             ip = str(request.META['HTTP_X_FORWARDED_FOR'])
#         except:
#             errors[error] = "ip error"
#             return HttpResponse(errors, status=403)
#         try:
#             new_entry = Entry(city=city, description=description, ip=ip)
#             new_entry.save()
#             return HttpResponse(errors, status=200)
#         except:
#             errors[error] = "save error"
#             return HttpResponse(status=403)
#     else:
#         return HttpResponse(status=405)

def index(request):
    entries = Entry.objects.order_by('-created')
    ip = request.META['HTTP_X_FORWARDED_FOR']
    context = {'entries': entries, 'ip': ip}
    response = render_to_response('index.html', context, context_instance=RequestContext(request))
    return response
