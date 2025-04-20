from fastapi import APIRouter, Depends, HTTPException
from src.schemas.logs_schema import LogsCreate, LogsUpdate, LogsResponse
from src.schemas.responses.general_response import GeneralResponse
from src.usecases.logs_usecase import LogsUseCase, get_logs_use_case
from src.api.http.dependencies import security
from typing import List


router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[LogsResponse])
async def create_log(
    log: LogsCreate,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[LogsResponse]:
    """
    Create a new log entry.
    """
    try:
        new_log = await use_case.create_log(log)
        if not new_log:
            raise HTTPException(status_code=400, detail="Log creation failed")
        return GeneralResponse[LogsResponse](
            status="success",
            message="Log created successfully",
            data=new_log
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{log_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[LogsResponse])
async def get_log(
    log_id: int,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[LogsResponse]:
    """
    Retrieve a log entry by ID.
    """
    try:
        log = await use_case.get_log(log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        return GeneralResponse[LogsResponse](
            status="success",
            message="Log retrieved successfully",
            data=log
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{log_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[LogsResponse])
async def update_log(
    log_id: int,
    log: LogsUpdate,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[LogsResponse]:
    """
    Update an existing log entry.
    """
    try:
        updated_log = await use_case.update_log(log_id, log)
        if not updated_log:
            raise HTTPException(status_code=404, detail="Log not found")
        return GeneralResponse[LogsResponse](
            status="success",
            message="Log updated successfully",
            data=updated_log
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{log_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[None])
async def delete_log(
    log_id: int,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[None]:
    """
    Delete a log entry by ID.
    """
    try:
        deleted = await use_case.delete_log(log_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Log not found")
        return GeneralResponse[None](
            status="success",
            message="Log deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[LogsResponse]])
async def list_logs(
    page: int = 1,
    limit: int = 10,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[List[LogsResponse]]:
    """
    List logs with pagination.
    """
    try:
        logs = await use_case.list_logs(page, limit)
        return GeneralResponse[List[LogsResponse]](
            status="success",
            message="Logs retrieved successfully",
            data=logs
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/users/{user_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[LogsResponse]])
async def get_logs_by_fields(
    user_id: int,
    use_case: LogsUseCase = Depends(get_logs_use_case),
) -> GeneralResponse[LogsResponse]:
    """
    Retrieve logs by specific fields.
    """
    try:
        log = await use_case.get_logs_by_fields(user_id=user_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        return GeneralResponse[List[LogsResponse]](
            status="success",
            message="Log retrieved successfully",
            data=log
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
