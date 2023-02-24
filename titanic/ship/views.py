from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import string
from .models import Operator, ShipName
from .fileHandle import handle_uploaded_file, create_file_index
from .forms import UploadFileForm

# Create your views here.
def index(request):    
    return render(request, 'ship/index.html')


def login(request):
    try:
       operator  = (request.POST['op_first'] + " " + request.POST['op_last']).lower()
       userid = Operator.objects.get(operator_text=operator).id
    except (KeyError, Operator.DoesNotExist):
        if operator.replace(" ", "") != "":
            user = Operator(operator_text=operator)
            user.save()
            userid = get_object_or_404(Operator, operator_text=operator).id
            return HttpResponseRedirect(reverse('ship:manifest', args=(userid,)))
        else:
            return render(request, 'ship/index.html', {
                'error_message': "Operator name cannot be empty",
            })
    else:
        return HttpResponseRedirect(reverse('ship:manifest', args=(userid,)))
    
def manifest(request, userid):
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    context = {'operator_name': operator,
               'userid': userid}

    return render(request, 'ship/manifest.html', context)

def upload(request, userid):
    if request.method == 'POST':
        uploadedFile = request.FILES.get('manifest', {})
        if uploadedFile != {}:
            handle_uploaded_file(request.FILES['manifest'])
            
            try:
                shipName  = request.POST['ship_name'].lower()
                print(shipName)
                shipid = ShipName.objects.get(ship_name=shipName).id
            except (KeyError, ShipName.DoesNotExist):
                if shipName != "":
                    ship = ShipName(ship_name=shipName)
                    ship.save()
                    shipid = get_object_or_404(ShipName, ship_name=shipName).id
                    
                    return HttpResponseRedirect(reverse('ship:transaction', args=(userid, shipid)))
                else:
                    return render(request, 'ship/manifest.html', {
                        'error_message': "Ship name cannot be empty",
                    })
            
            return HttpResponseRedirect(reverse('ship:transaction', args=(userid, shipid)))
    else:
        form = UploadFileForm()
        return render(request, 'ship/manifest.html', {'form': form})

def transaction(request, userid, shipid):
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    shipName = string.capwords(get_object_or_404(ShipName, id=shipid).ship_name)
    context = {'operator_name': operator,
               'userid': userid,
               'ship_name': shipName,
               'shipid': shipid,
            }

    return render(request, 'ship/transaction.html', context)

def load(request, userid, shipid): 
    containers, containerNames = create_file_index()
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    shipName = string.capwords(get_object_or_404(ShipName, id=shipid).ship_name)
    context = {'operator_name': operator,
               'userid': userid,
               'ship_name': shipName,
               'shipid': shipid,
               'containers': containers,
               'containerNames': containerNames,
            }

    return render(request, 'ship/load.html', context)

def unload(request, userid, shipid): ## NEEDS FIX!!!!!
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    shipName = string.capwords(get_object_or_404(ShipName, id=shipid).ship_name)
    context = {'operator_name': operator,
               'userid': userid,
               'ship_name': shipName,
               'shipid': shipid,
            }

    return render(request, 'ship/load.html', context)

def balance(request, userid, shipid): ## NEEDS FIX!!!!!
    
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    shipName = string.capwords(get_object_or_404(ShipName, id=shipid).ship_name)
    context = {'operator_name': operator,
               'userid': userid,
               'ship_name': shipName,
               'shipid': shipid,
            }

    return render(request, 'ship/load.html', context)