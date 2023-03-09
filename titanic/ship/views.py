from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import string
from .models import Operator, ShipName
from .fileHandle import handle_uploaded_file, create_file_index, enter_log, prepare_outbound_manifest
from .forms import UploadFileForm
import json
from .algorithm import algorithm as alg


loadListValues = []
unloadListValues = []
# Create your views here.
def index(request):    
    return render(request, 'ship/index.html')

def logout(request, shipid):    
    try:
        backUrl  = "ship:" + request.POST['go_back'];
        operator  = (request.POST['op_first'] + " " + request.POST['op_last']).lower()
        logText = string.capwords(operator) + " signs in" 
        userid = Operator.objects.get(operator_text=operator).id
    except (KeyError, Operator.DoesNotExist):
        if operator.replace(" ", "") != "":
            user = Operator(operator_text=operator)
            user.save()
            userid = get_object_or_404(Operator, operator_text=operator).id
            enter_log(logText)
            return HttpResponseRedirect(reverse(backUrl, args=(userid, shipid)))
        else:
            return render(request, 'ship/index.html', {
                'error_message': "Operator name cannot be empty",
            })
    else:
        enter_log(logText)
        return HttpResponseRedirect(reverse(backUrl, args=(userid, shipid)))
    
def logoutAnimate(request, shipid):    
    try:
        operator  = (request.POST['op_first'] + " " + request.POST['op_last']).lower()
        logText = string.capwords(operator) + " signs in" 
        print(operator)
        userid = Operator.objects.get(operator_text=operator).id
    except (KeyError, Operator.DoesNotExist):
        if operator.replace(" ", "") != "":
            user = Operator(operator_text=operator)
            user.save()
            userid = get_object_or_404(Operator, operator_text=operator).id
            enter_log(logText)
            
            return JsonResponse({"op_id":userid}, safe=False)
        else:
            return render(request, 'ship/index.html', {
                'error_message': "Operator name cannot be empty",
            })
    else:
        enter_log(logText)

        return JsonResponse({"op_id":userid}, safe=False)

def login(request):
    try:
        operator  = (request.POST['op_first'] + " " + request.POST['op_last']).lower()
        logText = string.capwords(operator) + " signs in" 
        userid = Operator.objects.get(operator_text=operator).id
    except (KeyError, Operator.DoesNotExist):
        if operator.replace(" ", "") != "":
            user = Operator(operator_text=operator)
            user.save()
            userid = get_object_or_404(Operator, operator_text=operator).id
            enter_log(logText)
            return HttpResponseRedirect(reverse('ship:manifest', args=(userid,)))
        else:
            return render(request, 'ship/index.html', {
                'error_message': "Operator name cannot be empty",
            })
    else:
        enter_log(logText)
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
                logText = "Manifest file for the ship \"" + shipName + "\" has been uploaded" 
                enter_log(logText)
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

def animate(request, userid, shipid):
    pathToManifest = "ship/files/manifest.txt";
    loadVals = []
    unloadVals = []
    loadWeights = {}
    isBalance = True
    
    if request.method == 'POST':
        isBalance = False
        loadVals = request.POST['load_list']
        unloadVals = request.POST['unload_list']
        loadWeights = request.POST['load_weights']
        
        
        loadListValues = loadVals.split('./.')
        unloadListValues = unloadVals.split('./.')
        unloadCoordinates = []
        print(loadListValues, unloadListValues)
        for unloadValue in unloadListValues:
            values = unloadValue.split(',')
            unloadCoordinates.append((int(values[0]), int(values[1])))

        if loadListValues == ['']:
            loadListValues = []
            
        actionSequence = alg.load_unload(pathToManifest, loadListValues, unloadCoordinates)
    else:
        actionSequence = alg.balance(pathToManifest)
        
    newActionSequence = []
    
    for actionsList in actionSequence:
        newList = []
        
        for item in actionsList:
            if type(item) == tuple:
                newList.append(list(item))
            else:
                newList.append(item)
                
        newActionSequence.append(newList)

    containers, containerNames = create_file_index()
    operator = string.capwords(get_object_or_404(Operator, id=userid).operator_text)
    shipName = string.capwords(get_object_or_404(ShipName, id=shipid).ship_name)
    context = {'operator_name': operator,
               'userid': userid,
               'ship_name': shipName,
               'shipid': shipid,
               'containers': containers,
               'containerNames': containerNames,
               'action_sequence':newActionSequence,
               'loads': loadVals,
               'unloads': unloadVals,
               'isBalance': isBalance,
               'remainingTime': alg.get_full_time_set(actionSequence),
               'loadWeights': loadWeights
            }


    return render(request, 'ship/animate.html', context)

def log(request, userid):    
    logText = request.POST.get('logEntry')

    enter_log(logText)

    return JsonResponse(logText, safe=False)

def finalize(request, shipid):    
    if request.method == 'POST':
        finalList = json.loads(request.POST['finalList'])["containers"]

    prepare_outbound_manifest(finalList)
    
    return JsonResponse("success", safe=False)