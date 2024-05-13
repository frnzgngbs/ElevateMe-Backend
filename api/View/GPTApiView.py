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

    @action(dmethods=['post'])
    def problem_statement(self, request):
        field1 = request.data.get('field1')
        field2 = request.data.get('field2')
        field3 = request.data.get('field3')
        field4_filter = request.data.get('filter')

        if filter is not None:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}s, {field3}."
        else:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}, {field3}. Apply filter: {field4_filter}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Disregard if any of the fields seems like a nonsense to you. Also,"
                                                  "in generating responses, you should give it directly without explanation."
                                                  "Only generate problem statement."},
                    {"role": "user", "content": prompt}]
            )
        except openai.OpenAIError as err:
            raise ValueError("AI Model problem in Problem statement feature.")


        content_list = response.choices[0].message.content.split('\n')

        return Response({"response": content_list}, status=status.HTTP_200_OK)

    @action(methods=['post'])
    def five_whys(self, request):


    def five_hmws(self, request):
        pass

    def potential_root(self,request):
        pass

    def elevator_pitch(self, request):
        pass
