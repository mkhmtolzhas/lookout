from fastapi import APIRouter, Depends, HTTPException
from src.schemas.analysis_result_schema import AnalysisResultCreate, AnalysisResultUpdate, AnalysisResultResponse
from src.schemas.responses.general_response import GeneralResponse
from src.usecases.analysis_result_usecase import AnalysisResultUseCase, get_analysis_result_use_case
from src.api.http.dependencies import security
from typing import List


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", dependencies=[Depends(
        security.access_token_required)],
    response_model=GeneralResponse[AnalysisResultResponse])
async def create_analysis_result(
    analysis_result: AnalysisResultCreate,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> AnalysisResultResponse:
    """
    Create a new analysis result.
    """
    try:
        new_analysis_result = await use_case.create_analysis_result(analysis_result)
        if not new_analysis_result:
            raise HTTPException(status_code=400, detail="Analysis result creation failed")
        return GeneralResponse[AnalysisResultResponse](
            status="success",
            message="Analysis result created successfully",
            data=new_analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/{analysis_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[AnalysisResultResponse])
async def get_analysis_result(
    analysis_id: int,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> AnalysisResultResponse:
    """
    Retrieve an analysis result by ID.
    """
    try:
        analysis_result = await use_case.get_analysis_result(analysis_id)
        if not analysis_result:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        return GeneralResponse[AnalysisResultResponse](
            status="success",
            message="Analysis result retrieved successfully",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{analysis_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[AnalysisResultResponse])
async def update_analysis_result(
    analysis_id: int,
    analysis_result: AnalysisResultUpdate,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> AnalysisResultResponse:
    """
    Update an existing analysis result.
    """
    try:
        updated_analysis_result = await use_case.update_analysis_result(analysis_id, analysis_result)
        if not updated_analysis_result:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        return GeneralResponse[AnalysisResultResponse](
            status="success",
            message="Analysis result updated successfully",
            data=updated_analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{analysis_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[bool])
async def delete_analysis_result(
    analysis_id: int,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> bool:
    """
    Delete an analysis result by ID.
    """
    try:
        deleted = await use_case.delete_analysis_result(analysis_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        return GeneralResponse[bool](
            status="success",
            message="Analysis result deleted successfully",
            data=deleted
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[AnalysisResultResponse]])
async def list_analysis_results(
    page: int = 1,
    limit: int = 10,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> List[AnalysisResultResponse]:
    """
    List analysis results with pagination.
    """
    try:
        analysis_results = await use_case.list_analysis_results(page, limit)
        return GeneralResponse[List[AnalysisResultResponse]](
            status="success",
            message="Analysis results retrieved successfully",
            data=analysis_results
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/videos/{video_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[AnalysisResultResponse]])
async def get_analysis_results_by_video_id(
    video_id: int,
    use_case: AnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> AnalysisResultResponse:
    """
    Retrieve analysis results by video ID.
    """
    try:
        analysis_result = await use_case.get_analysis_results_by_fields(video_id=video_id)
        if not analysis_result:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        return GeneralResponse[List[AnalysisResultResponse]](
            status="success",
            message="Analysis result retrieved successfully",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))