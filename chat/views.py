from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import ChatMessage
from .serializers import MessageSerializer

@api_view(['GET'])
def messages(request):
    messages = ChatMessage.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def message(request, pk):
    message = ChatMessage.objects.get(id=pk)
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def messageCreate(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def messageUpdate(request, pk):
    message = ChatMessage.objects.get(id=pk)
    serializer = MessageSerializer(instance=message, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def messageDelete(request, pk):
    message = ChatMessage.objects.get(id=pk)
    message.delete()
    return Response("Item successfully deleted")