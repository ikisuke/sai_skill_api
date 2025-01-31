import json
import datetime
from typing import Optional
import time

from rest_framework import views, status, permissions
from rest_framework.response import Response

from .openai_apis import get_career_vector
from .DB_operator import insert_career, exist_career, update_career
from .calculators import get_skill_similarity, similarities_to_scores
from .apps import SKILL_IDS, SKILL_VECTORS


def record_career(
        started_at: datetime.datetime,
        finished_at: datetime.datetime,
        input_text: str,
        address: str,
        career_id: Optional[int] = None
) -> int:
    career_vector = get_career_vector(input_text)

    term = finished_at - started_at
    # 1年を1ポイントとしてスケーリング
    scaling_point = term.days / 365

    skill_similarities = get_skill_similarity(SKILL_VECTORS, career_vector)
    skill_scores = similarities_to_scores(skill_similarities, scaling_point)

    start = time.time()
    if career_id is None:
        current_career_id = insert_career(
            career_vector=career_vector,
            skill_ids=SKILL_IDS,
            skill_scores=skill_scores,
            finished_at=finished_at,
            started_at=started_at,
            input_text=input_text,
            address=address
        )
    else:
        current_career_id = update_career(
            career_vector=career_vector,
            skill_ids=SKILL_IDS,
            skill_scores=skill_scores,
            finished_at=finished_at,
            started_at=started_at,
            input_text=input_text,
            address=address,
            career_id=career_id
        )

    return current_career_id


class SkillElementPostView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            body = json.loads(request.body)
            started_at = datetime.datetime.strptime(body["started_at"], "%Y-%m")
            finished_at = datetime.datetime.strptime(body["finished_at"], "%Y-%m")
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            address = body["address"]
            if not isinstance(address, str):
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_career_id = record_career(
            started_at,
            finished_at,
            input_text,
            address
        )

        context = {
            "status": 200,
            "career_id": current_career_id
        }

        return Response(context, status=status.HTTP_200_OK)


class SkillElementPutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def put(self, request, career_id=None):
        try:
            body = json.loads(request.body)
            started_at = datetime.datetime.strptime(body["started_at"], "%Y-%m")
            finished_at = datetime.datetime.strptime(body["finished_at"], "%Y-%m")
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            address = body["address"]
            if not isinstance(address, str):
                raise ValueError()
            if exist_career(career_id) is False:
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_career_id = record_career(
            started_at,
            finished_at,
            input_text,
            address,
            career_id
        )

        context = {
            "status": 200,
            "career_id": current_career_id
        }

        return Response(context, status=status.HTTP_200_OK)
