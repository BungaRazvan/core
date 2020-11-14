import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View

class CMSView(View):

    def post(self, request):

        headers = request.headers

        if headers.get("Content-Type") != "application/json":
            return HttpResponseBadRequest()

        try:
            args = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("Invalid Body")

        data: dict = self.execute(**args)

        return JsonResponse(data)
