import json
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate(request):
    # TODO is this right?
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # get apikey and return it
            user = form.get_user()
            api_key = user.api_key.key
            response = HttpResponse(json.dumps({'api_key': api_key}), content_type='application/javascript; charset=utf8', )
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return HttpResponse(json.dumps({'error': 'unauthorized'}), content_type='application/javascript; charset=utf8', status=401)
    else:
        return HttpResponse(json.dumps({'error': 'unauthorized'}), content_type='application/javascript; charset=utf8', status=401)
