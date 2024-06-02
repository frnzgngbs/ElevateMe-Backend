from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..Model.VennDiagramModel import TwoVennDiagramModel, ThreeVennDiagramModel
from ..Serializer.ProblemStatementSerializer import TwoVennProblemStatementSerializer, \
    ThreeProblemStatementSerializer

from ..Model.ProblemStatementModel import TwoVennProblemStatementModel, ThreeVennProblemStatementModel


class TwoVennProblemStatementView(mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TwoVennProblemStatementModel.objects.all()
    serializer_class = TwoVennProblemStatementSerializer

    def get_queryset(self):
        return TwoVennProblemStatementModel.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Saved Problem Statement"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):

        # Retrieve the instance of a TwoVennProblemStatementModel by using get_object method. Internally it has a look up field
        instance = self.get_object()


        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreeVennProblemStatementView(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ThreeVennProblemStatementModel.objects.all()
    serializer_class = ThreeProblemStatementSerializer

    def get_queryset(self):
        return ThreeVennProblemStatementModel.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Saved Problem Statement"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        # Since we set partial as true, we are not required to have all the datas needed.
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

