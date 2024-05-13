from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import openai


# Create your views here.
class GPTApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        task = request.data.get('task')

        if task == "problem_statement":
            return self.problem_statement(request)


    def problem_statement(self, request):
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

    def five_whys(self, request):
        pass

    def five_hmws(self, request):
        pass

    def potential_root(self,request):
        pass

    def elevator_pitch(self, request):
        pass
