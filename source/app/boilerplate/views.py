from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from source.app.boilerplate.schemas import (
    BoilerplateApiResponse,
    BoilerplateId,
    BoilerplatePage,
    BoilerplatePagination,
    BoilerplateRequest,
    BoilerplateUpdateRequest,
)
from source.app.boilerplate.services import (
    create_boilerplate,
    delete_boilerplate,
    get_boilerplate,
    list_boilerplate,
    update_boilerplate,
)
from source.core.database import get_db
from source.core.schemas import ExceptionModel

boilerplate_router = APIRouter(prefix="/boilerplate")


@boilerplate_router.post(
    "/",
    response_model=BoilerplateApiResponse,
    responses={
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    status_code=status.HTTP_201_CREATED,
    tags=["boilerplate"],
)
async def boilerplate_create(
    boilerplate: BoilerplateRequest, db: AsyncIOMotorDatabase = Depends(get_db)
) -> dict:
    if created_boilerplate := await create_boilerplate(boilerplate=boilerplate, db=db):
        return created_boilerplate
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Boilerplate '{boilerplate.email}' already exists",
    )


@boilerplate_router.get(
    "/{boilerplate_id}",
    response_model=BoilerplateApiResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["boilerplate"],
)
async def boilerplate_get(
    request: BoilerplateId = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    if boilerplate := await get_boilerplate(
        boilerplate_id=request.boilerplate_id, db=db
    ):
        return boilerplate
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Boilerplate '{request.boilerplate_id}' not found",
    )


@boilerplate_router.patch(
    "/{boilerplate_id}",
    response_model=BoilerplateApiResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    tags=["boilerplate"],
)
async def boilerplate_update(
    payload: BoilerplateUpdateRequest,
    request: BoilerplateId = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    if await get_boilerplate(boilerplate_id=request.boilerplate_id, db=db):
        if updated_boilerplate := await update_boilerplate(
            boilerplate_id=request.boilerplate_id, boilerplate=payload, db=db
        ):
            return updated_boilerplate
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Boilerplate '{payload.email}' already exists",
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Boilerplate '{request.boilerplate_id}' not found",
    )


@boilerplate_router.delete(
    "/{boilerplate_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["boilerplate"],
)
async def boilerplate_delete(
    request: BoilerplateId = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> None:
    if not await delete_boilerplate(boilerplate_id=request.boilerplate_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Boilerplate '{request.boilerplate_id}' not found",
        )


@boilerplate_router.get(
    "/",
    response_model=BoilerplatePage,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
    tags=["boilerplate"],
)
async def boilerplate_list(
    pagination: BoilerplatePagination = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> BoilerplatePage:
    return await list_boilerplate(
        page=pagination.page,
        size=pagination.size,
        sort=pagination.sort,
        order=pagination.order,
        db=db,
    )
