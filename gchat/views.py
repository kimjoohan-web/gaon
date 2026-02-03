from django.contrib.auth.decorators import login_required
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from django.http import Http404
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from gchat.models import Message as gmessage , ChatRoom as chatroom

from gchat.serializers import MessageSerializer

# Create your views here.
@login_required(login_url='common:login')
def index(request):
    return render(request, 'gchat/index.html')

@login_required(login_url='common:login')
def room(request, room_name):
    # MessageListView.as_view()(request, roomname=room_name)

    return render(request, 'gchat/room.html', {
        'room_name': room_name,
        'email': request.user.email if request.user.is_authenticated else '',   
    })

class MessageListView(generics.ListAPIView):
    # 이 뷰에서 사용할 시리얼라이저를 지정합니다.
    serializer_class = MessageSerializer

    # GET 요청에 대한 쿼리셋을 정의하는 메소드입니다.
    def get_queryset(self):
        # URL 파라미터에서 'room_id' 값을 가져옵니다.
        roomname = self.kwargs.get('roomname', None)

        
        # room_id가 제공되지 않았을 경우 에러 메시지와 함께 400 상태 코드 응답을 반환합니다.
        if not roomname:
            content = {'detail': 'roomname 파라미터가 필요합니다.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        room_id = get_room_id_from_name(roomname)

        # room_id에 해당하는 메시지 객체들을 쿼리셋으로 가져옵니다.
        queryset = gmessage.objects.filter(room_id=room_id).order_by('timestamp')
        
        # 해당 room_id의 메시지가 존재하지 않을 경우 404 Not Found 예외를 발생시킵니다.
        if not queryset.exists():
            raise Http404('해당 room_id로 메시지를 찾을 수 없습니다.')

        # 쿼리셋을 반환합니다.
        return queryset
    
def get_room_id_from_name(room_name):
    try:
        room = chatroom.objects.get(name=room_name)
        return room.id
    except chatroom.DoesNotExist:
        raise Http404('해당 room_name으로 채팅방을 찾을 수 없습니다.')      