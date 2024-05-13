from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
import openai
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# Create your views here.
class GPTApiView(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def problem_statement(self, request):
        field1 = request.data.get('field1')
        field2 = request.data.get('field2')
        field3 = request.data.get('field3')
        field4_filter = request.data.get('filter')

        if filter is not None:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}s, {field3}."
        else:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}, {field3}. Apply filter: {field4_filter}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                            "Only generate problem statement."},
                {"role": "user", "content": prompt}]
        )

        content_list = response.choices[0].message.content.split('\n')

        return Response({"response": content_list}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def five_whys(self, request):
        selected_problem = request.data.get('ranked_problem')

        prompt = (
            f"Generate five whys to uncover the underlying issue behind "
            f"{selected_problem}. Make it relevant to the {selected_problem} and understandable.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                 },
                {"role": "user", "content": prompt}
            ]
        )

        print(response)

        return None

    def five_hmws(self, request):
        pass

    def potential_root(self, request):
        pass

    def elevator_pitch(self, request):
        pass
