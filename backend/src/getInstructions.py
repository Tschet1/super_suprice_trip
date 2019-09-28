import backend.src.directions
import time
from collections import namedtuple
from django.http import JsonResponse

def Instruction(type=None, instruction=None):
    return {
        'type': type,
        'instruction': instruction
    }

def getInstructions(request):
    request.GET.get('start', 0)
    request.GET.get('end', 0)
    request.GET.get('id', 0)


    #TODO: load information according to id
    location_start_end = "zug"
    location_thing = "zürich"
    time_start = round(time.time())
    time_back = time_start + 5*3600

    instructions = []

    # way there
    res = backend.src.directions.get_route_from_to(location_start_end, location_thing, departure_time=time_start)
    for step in res['routes'][0]['legs'][0]['steps']:
        instructions.append(Instruction(type='travel', instruction=step))

    # actual thing
    instructions.append(Instruction(type='visit', instruction='Visit the thing'))

    # way back
    res = backend.src.directions.get_route_from_to(location_thing, location_start_end, departure_time=time_back)
    for step in res['routes'][0]['legs'][0]['steps']:
        instructions.append(Instruction(type='travel', instruction=step))

    return JsonResponse(instructions, safe=False)

if __name__ == '__main__':
    res = getInstructions(1)
    print(res)