from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
import openai
import os

from ..Serializer.FiveWhySerializer import FiveWhySerializer
from ..Serializer.FiveHmwSerializer import FiveHmwSerializer
from ..Serializer.PotentialRootSerializer import PotentialRootSerializer
from ..Serializer.VennSerializer import TwoVennSerializer, ThreeVennSerializer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class GPTApiView(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'three_venn':
            return ThreeVennSerializer
        elif self.action == 'two_venn':
            return TwoVennSerializer
        elif self.action == 'potential_root':
            return PotentialRootSerializer
        elif self.action == 'five_whys':
            return FiveWhySerializer
        elif self.action == 'five_hmws':
            return FiveHmwSerializer

    @action(detail=False, methods=['post'], name="Two Venn Diagram", permission_classes=[IsAuthenticated])
    def two_venn(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            field1 = serializer.validated_data.get('field1')
            field2 = serializer.validated_data.get('field2')
            field_filter = serializer.validated_data.get('filter_field')

            prompt = two_prompt(field1=field1, field2=field2, field_filter=field_filter)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Disregard if the question is out of the context and seems like nonsense to you. Also,"
                                "in generating responses, you should give it directly without explanation."
                                "Only generate problem statement."},
                    {"role": "user", "content": prompt}
                ]
            )

            problem_statement = response.choices[0].message.content.split('\n')

            cleaned_problem_statement = []

            for i in problem_statement:
                cleaned_problem_statement.append(i[2:].strip())


            return Response({"response": cleaned_problem_statement}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Three Venn Diagram")
    def three_venn(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            field1 = serializer.validated_data.get('field1')
            field2 = serializer.validated_data.get('field2')
            field3 = serializer.validated_data.get('field3')
            field_filter = serializer.validated_data.get('filter_field')

            prompt = three_prompt(field1=field1, field2=field2, field3=field3, field_filter=field_filter)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Disregard if the question is out of the context and seems like nonsense to you. Also,"
                                "in generating responses, you should give it directly without explanation."
                                "Only generate problem statements."},
                    {"role": "user", "content": prompt}
                ]
            )

            problem_statement = response.choices[0].message.content.split('\n')

            cleaned_problem_statement = []
            for i in problem_statement:
                cleaned_problem_statement.append(i[2:].strip())

            # print(cleaned_problem_statement)

            return Response({"response": cleaned_problem_statement}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # localhost:8000/api/potential_root/
    @action(detail=False, methods=['post'], name="Potential Root Problem")
    def potential_root(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            list_of_whys = request.data.get('list_of_whys')
            joined_whys = ", ".join(list_of_whys)

            prompt = (
                f"Generate potential root problem to uncover the underlying issue behind {joined_whys}. "
                "Make it relevant to the list of whys and understandable."
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Disregard if the question is out of the context and seems like nonsense to you. Also,"
                                "in generating responses, you should give it directly without explanation."
                     },
                    {"role": "user", "content": prompt}
                ]
            )

            root_problem = response.choices[0].message.content.split('\n')
            return Response({"response": root_problem}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Five Whys")
    def five_whys(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid:
            selected_problem = request.data.get('ranked_problem')


            prompt = (
                f"Generate five whys to uncover the underlying issue behind {selected_problem}. "
                "Make it relevant to the selected problem and understandable. Also,"
                "in generating responses, you should give it directly without explanation."
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Disregard if the question is out of the context and seems like nonsense to you. Also,"
                                "in generating responses, you should give it directly without explanation."
                     },
                    {"role": "user", "content": prompt}
                ]
            )

            five_whys = response.choices[0].message.content.split('\n')
            return Response({"response": five_whys}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], name="Five How Might We")
    def five_hmws(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid:
            root_problem = request.data.get('root_problem')

            prompt = (
                f"Generate five How Might We (HMW) given the root potential problem: {root_problem}. "
                "Make it relevant to the root problem and understandable. Also,"
                "in generating responses, you should give it directly without explanation."
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Disregard if the question is out of the context and seems like nonsense to you. Also,"
                                "in generating responses, you should give it directly without explanation."
                     },
                    {"role": "user", "content": prompt}
                ]
            )

            five_hmws = response.choices[0].message.content.split('\n')
            return Response({"response": five_hmws}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Elevator Pitch")
    def elevator_pitch(self, request):
        pass

def three_prompt(**kwargs):
    if kwargs.get('field_filter') is not None:
        return f"Generate 5 problem statements given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}."
    else:
        return f"Generate 5 problem statements given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}. Apply filter: {kwargs.get('field_filter')}."

def two_prompt(**kwargs):
    if kwargs.get('field_filter') is not None:
        return f"Generate 5 problem statements given these 2 fields: {kwargs.get('field1')}, {kwargs.get('field2')}."
    else:
        return f"Generate 5 problem statements given these 2 fields: {kwargs.get('field1')}, {kwargs.get('field2')}. Apply filter: {kwargs.get('field_filter')}. "
