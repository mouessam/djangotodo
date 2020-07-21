from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from todolist.models import TodoList
from todolist.serializers import UserSerializer, TodoListSerializer
from rest_framework.response import Response


@swagger_auto_schema(
    method='POST',
    responses={
        '201': "User Created",
        '400': "Bad Request"
    },
    operation_id='Create User',
    request_body=UserSerializer,
    operation_description='This end point create user'
)
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "user create successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListView(viewsets.ViewSet,
                   generics.GenericAPIView,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    serializer_class = TodoListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = TodoList.objects.all()

    def list(self, request, **kwargs):
        queryset = TodoList.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'owner': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None, **kwargs):
        instance = get_object_or_404(TodoList, id=pk)
        if instance.owner.id == request.user.id:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        instance = get_object_or_404(TodoList, id=pk)
        if instance.owner.id == request.user.id:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
