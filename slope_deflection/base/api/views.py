from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['POST'])
def getRoutes(request):
    routes=[
        'GET/api',
    ]
    return Response(routes)

@api_view(['POST'])
