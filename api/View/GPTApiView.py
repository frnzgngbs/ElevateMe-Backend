from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
import openai
import os

from ..Serializer.ElevatorPitchSerializer import ElevatorPitchSerializer
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
        elif self.action == 'elevator_pitch':
            return ElevatorPitchSerializer

    @action(detail=False, methods=['post'], name="Two Venn Diagram", permission_classes=[IsAuthenticated])
    def two_venn(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            field1 = serializer.validated_data.get('field1')
            field2 = serializer.validated_data.get('field2')
            filter = serializer.validated_data.get('filter')

            prompt = two_prompt(field1=field1, field2=field2, filter=filter)

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Your tasked is to understand what the user's want."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(response.choices[0].message.content)

            problem_statement = response.choices[0].message.content.split('\n')

            cleaned_problem_statement = [i for i in problem_statement if i != ""]

            filtered_response = []

            for i in cleaned_problem_statement:
                filtered_response.append(i[2:].strip())

            return Response({"response": filtered_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Three Venn Diagram")
    def three_venn(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            field1 = serializer.validated_data.get('field1')
            field2 = serializer.validated_data.get('field2')
            field3 = serializer.validated_data.get('field3')
            filter = serializer.validated_data.get('filter')

            prompt = three_prompt(field1=field1, field2=field2, field3=field3, filter=filter)

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Your tasked is to understand what the user's want."},
                    {"role": "user", "content": prompt}
                ]
            )

            problem_statement = response.choices[0].message.content.split('\n')

            cleaned_problem_statement = [i for i in problem_statement if i != ""]

            filtered_response = []

            for i in cleaned_problem_statement:
                filtered_response.append(i[2:].strip())

            # print(cleaned_problem_statement)

            return Response({"response": filtered_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # localhost:8000/api/potential_root/
    @action(detail=False, methods=['post'], name="Five Whys")
    def five_whys(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid:
            selected_problem = request.data.get('ranked_problem')


            prompt = (
                f"Generate five whys to uncover the underlying issue behind {selected_problem}. Directly give the five whys with no explanation."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Your tasked is to understand what the user's want."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(response.choices[0].message.content)

            five_whys = response.choices[0].message.content.split('\n')
            filtered_response = []
            for i in five_whys:
                filtered_response.append(i[2:].strip())
            print(filtered_response)


            return Response({"response": filtered_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Potential Root Problem")
    def potential_root(self, request):
        whys_dict = {"list_of_whys": request.data.get('list_of_whys')}
        serializer = self.get_serializer(data=whys_dict)
        if serializer.is_valid():
            list_of_whys = request.data.get('list_of_whys')
            joined_whys = ", ".join(list_of_whys)

            prompt = (
                f"Generate one potential root problem to uncover the underlying issue behind these set of why's statement: {joined_whys}. "
                f"And and this problem statement: {request.data.get('selected_statement')}."
                "I want you uncover potential issues based on the context given. Take note, I am only asking for a one potential root problem. Do not put any indicator that it is the potential root problem as I know that the responses are all potential root problem."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "PLEASE READ THE USERS PROMPT AND DO WHAT IT IS SAYING."                     },
                    {"role": "user", "content": prompt}
                ]
            )

            root_problem = response.choices[0].message.content.split('\n')
            return Response({"root": root_problem}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], name="Five How Might We")
    def five_hmws(self, request):
        root_problem = request.data.get('root_problem')
        serializer = self.get_serializer(data={'root_problem': root_problem})

        if serializer.is_valid:
            selected_statement = request.data.get('selected_statement')
            list_of_whys = ", ".join(list(request.data.get('list_of_whys')))

            prompt = (
                f"Based on these contexts: {root_problem}, the first problem statement: {selected_statement}, and a set of whys statement: {list_of_whys}. Only generate five how might we statements and do not include any unnecessary things."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "PLEASE READ THE USERS PROMPT AND DO WHAT IT IS SAYING."
                     },
                    {"role": "user", "content": prompt}
                ]
            )

            five_hmws = response.choices[0].message.content.split('\n')
            print(five_hmws)
            filtered_response = []

            for item in five_hmws:
                if item.strip() == "":
                    continue
                filtered_response.append(item[3:])

            # print(filtered_response)

            return Response({"five_hmws": filtered_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name="Elevator Pitch", permission_classes=[AllowAny])
    def elevator_pitch(self, request):
        elevator_dict = {'list_of_hmws': request.data['list_of_hmws']}
        # print(request.data)
        serializer = self.get_serializer(data=elevator_dict)

        list_of_whys = ", ".join(list(request.data.get("list_of_whys")))
        # print(list_of_whys)

        serializer.is_valid(raise_exception=True)
        list_of_hmws = request.data.get('list_of_hmws')
        root_problem = request.data.get('root_problem')


        joined_hmws = ", ".join(list_of_hmws)

        print(joined_hmws)

        prompt = (
            f"I want you to generate an elevator pitch following the format and be providing the information below. Take note to follow this format.\n"
            "FOR: [the target consumer]\n"
            "WHO: [specific needs, requirements, demands, criteria],\n"
            "WE PROVIDE: [solution or description],\n"
            "THAT: [gives specific benefits/value to clients]\n"
            "UNLIKE: [the competition],\n"
            "WHO: [provide a solution, features, functions, benefits]\n"
            "OUR SOLUTION: [better approach, solution, functions, benefits, technology],\n"
            "THAT: [offers a better customer experience]. Please answer all the words that are capitalized."
            "For every keywords answered, it should only be spaced 1 time only so I can have a proper string manipulation."
            f"Now I will be giving you all of the context that you need starting with the problem statement:  {request.data.get('problem_statement')},"
            f"followed by the list of whys: {list_of_whys}, followed by the root potential problem: {root_problem}, and lastly, the"
            f"How might wes (HMWs): {joined_hmws}. All context are given."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Strictly follow what the user want and do not ignore even a small detail on the user's prompt."
                 },
                {"role": "user", "content": prompt}
            ]
        )

        # print(response.choices[0].message.content)

        gpt_response = response.choices[0].message.content.split('\n')

        print(gpt_response)

        returning_response = []
        for keyword in gpt_response:
            if keyword == "":
                continue
            index = keyword.index(':')
            returning_response.append(keyword[index+1:].strip())

        return Response({'elevator_pitch': returning_response})


def three_prompt(**kwargs):
    print(kwargs)
    if kwargs.get('filter') is None:
        return f"Generate 5 problem statements given these scopes: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}. Strictly give the problem statement directly, not solutions."
    else:
        return f"Generate 5 problem statements given these scopes: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}. Take note of this specification {kwargs.get('filter')}. Strictly give the problem statement directly, not solutions."

def two_prompt(**kwargs):
    if kwargs.get('filter') is None:
        return f"Generate 5 problem statements given these scopes: {kwargs.get('field1')}, {kwargs.get('field2')}. Strictly give the problem statement directly, not solutions."
    else:
        return f"Generate 5 problem statements given these scopes: {kwargs.get('field1')}, {kwargs.get('field2')}.  Take note of this  specification {kwargs.get('filter')}. Strictly give the problem statement directly, not solutions."
