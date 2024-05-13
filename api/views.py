from rest_framework.response import Response
from rest_framework.views import APIView
import openai


# Create your views here.
class GPTApiView(APIView):

    def post(self, request):
        field1 = request.data.get('field1')
        field2 = request.data.get('field2')
        field3 = request.data.get('field3')
        filter = request.data.get('filter')


        openai.api_key = "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"

        if filter is not None:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}s, {field3}."
        else:
            prompt = f"Generate 5 problem statement given these 3 fields: {field1}, {field2}, {field3}. Apply filter: {filter}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Disregard if any of the fields seems like a nonsense to you. Also,"
                                              "in generating responses, you should give it directly without explanation."
                                              "Only generate problem statement."},
                {"role": "user", "content": prompt}]
        )

        content_list = response.choices[0].message.content.split('\n')

        return Response({"response": content_list})
