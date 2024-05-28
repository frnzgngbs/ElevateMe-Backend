from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..Model.VennDiagramModel import TwoVennDiagram, ThreeVennDiagram
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

    def create(self, request, *args, **kwargs):
        statements = request.data.pop("statement")

        results = []
        errors = []

        for statement in statements:
            item_data = request.data.copy()
            item_data['statement'] = statement
            item_data['user'] = request.user.pk

            serializer = self.get_serializer(data=item_data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                results.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(results, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return TwoVennProblemStatementModel.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        print(instance)
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
                                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ThreeVennProblemStatementModel.objects.all()
    serializer_class = ThreeProblemStatementSerializer

    def create(self, request, *args, **kwargs):

        statements = request.data.pop("statement")

        results = []
        errors = []

        for statement in statements:
            item_data = request.data.copy()
            item_data['statement'] = statement
            item_data['user'] = request.user.pk

            serializer = self.get_serializer(data=item_data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                results.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(results, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        return ThreeVennProblemStatementModel.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

