from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..Serializer.ProblemStatementSerializer import TwoVennProblemStatementSerializer, \
    ThreeProblemStatementSerializer

from ..Model.ProblemStatementModel import TwoVennProblemStatementModel, ThreeVennProblemStatementModel


class TwoVennProblemStatementView(mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = TwoVennProblemStatementModel.objects.all()
    serializer_class = TwoVennProblemStatementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            problem_statement = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThreeVennProblemStatementView(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = ThreeVennProblemStatementModel.objects.all()
    serializer_class = ThreeProblemStatementSerializer