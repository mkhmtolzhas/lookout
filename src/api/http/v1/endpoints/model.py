from authx import TokenPayload
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from src.schemas.model_schema import ModelResultSchema, ModelSchema
from src.schemas.responses.general_response import GeneralResponse
from src.usecases.model_usecase import ModelUseCase, get_model_use_case
from src.usecases.user_usecase import UserUseCase, get_user_use_case
from src.api.http.dependencies import security


router = APIRouter(prefix="/model", tags=["model"])

@router.post("/analyze", response_model=GeneralResponse[ModelSchema])
async def analyze_video(
    file: UploadFile = File(...),
    model_use_case: ModelUseCase = Depends(get_model_use_case),
    user_use_case: UserUseCase = Depends(get_user_use_case),
    token_payload: TokenPayload = Depends(security.access_token_required),
) -> GeneralResponse[ModelSchema]:
    """
    Analyze a video file and return the result.
    """
    user = await user_use_case.get_user_by_fields(email=token_payload.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"Received file: {file.filename}")

    file_name = f"{user.email}/{file.filename}"
    result = await model_use_case.analyze_video(user_id=user.id, file=file.file, file_name=file_name)

    return GeneralResponse[ModelSchema](
        status="success",
        message="Video analysis started successfully",
        data=result
    )


@router.post("/analyze/url", response_model=GeneralResponse[ModelSchema])
async def analyze_video_url(
    video_url: str,
    model_use_case: ModelUseCase = Depends(get_model_use_case),
    user_use_case: UserUseCase = Depends(get_user_use_case),
    token_payload: TokenPayload = Depends(security.access_token_required),
) -> GeneralResponse[ModelSchema]:
    """
    Analyze a video URL and return the result.
    """
    user = await user_use_case.get_user_by_fields(email=token_payload.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await model_use_case.analyze_video(user_id=user.id, file=video_url, file_name=video_url)

    return GeneralResponse[ModelSchema](
        status="success",
        message="Video analysis started successfully",
        data=result
    )

@router.get("/result/{task_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[ModelSchema])
async def get_result(
    task_id: str,
    use_case: ModelUseCase = Depends(get_model_use_case),
) -> GeneralResponse[ModelResultSchema]:
    """
    Retrieve the analysis result for a given task ID.
    """
    try:
        result = await use_case.get_result(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return GeneralResponse[ModelSchema](
            status="success",
            message="Result retrieved successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
