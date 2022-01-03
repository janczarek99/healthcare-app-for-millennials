from http import HTTPStatus

from fastapi import APIRouter, Response


router = APIRouter(tags=["Healthcheck"])


@router.get("/healthcheck")
def healthcheck():
    return Response(status_code=HTTPStatus.OK)
