from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..Model.VennDiagramModel import TwoVennDiagram, ThreeVennDiagram
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
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # TODO: Uncomment below if naa nay authentication
            serializer.save(self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: Uncomment below if naa nay authentication. As of now, kani lang sa for temporary

    def get_queryset(self):
        return TwoVennProblemStatementModel.objects.filter(user=self.request.user)


class ThreeVennProblemStatementView(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = ThreeVennProblemStatementModel.objects.all()
    serializer_class = ThreeProblemStatementSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)

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
