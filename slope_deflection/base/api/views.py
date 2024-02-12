from rest_framework.decorators import api_view
from rest_framework.response import Response
from . utils import beam_analysis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@api_view(['POST'])
@csrf_exempt
def calculate_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            spans_data = data.get('spans', [])
            number_of_supports = int(data.get('number_of_supports', 0))
            number_of_internal_joints = int(data.get('number_of_internal_joints', 0))

            # Call beam_analysis function to calculate coordinates
            coordinates,shearforce = beam_analysis(number_of_supports, number_of_internal_joints, spans_data)

            return JsonResponse({'coordinates': coordinates,'shearforce': shearforce})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
