from fastapi import APIRouter, Depends, HTTPException
from src.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse
from src.schemas.responses.general_response import GeneralResponse
from src.usecases.payment_usecase import PaymentUseCase, get_payment_use_case
from src.api.http.dependencies import security
from typing import List


router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/", dependencies=[Depends(
        security.access_token_required)], 
        response_model=GeneralResponse[PaymentResponse])
async def create_payment(
    payment: PaymentCreate,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> PaymentResponse:
    """
    Create a new payment.
    """
    try:
        new_payment = await use_case.create_payment(payment)
        if not new_payment:
            raise HTTPException(status_code=400, detail="Payment creation failed")
        return GeneralResponse[PaymentResponse](
            status="success",
            message="Payment created successfully",
            data=new_payment
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{payment_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[PaymentResponse])
async def get_payment(
    payment_id: int,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> PaymentResponse:
    """
    Retrieve a payment by ID.
    """
    try:
        payment = await use_case.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return GeneralResponse[PaymentResponse](
            status="success",
            message="Payment retrieved successfully",
            data=payment
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{payment_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[PaymentResponse])
async def update_payment(
    payment_id: int,
    payment: PaymentUpdate,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> PaymentResponse:
    """
    Update an existing payment.
    """
    try:
        updated_payment = await use_case.update_payment(payment_id, payment)
        if not updated_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return GeneralResponse[PaymentResponse](
            status="success",
            message="Payment updated successfully",
            data=updated_payment
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{payment_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[bool])
async def delete_payment(
    payment_id: int,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> bool:
    """
    Delete a payment by ID.
    """
    try:
        deleted = await use_case.delete_payment(payment_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Payment not found")
        return GeneralResponse[bool](
            status="success",
            message="Payment deleted successfully",
            data=deleted
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[PaymentResponse]])
async def list_payments(
    page: int = 1,
    limit: int = 10,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> list[PaymentResponse]:
    """
    List payments with pagination.
    """
    try:
        payments = await use_case.list_payments(page=page, limit=limit)
        return GeneralResponse[List[PaymentResponse]](
            status="success",
            message="Payments retrieved successfully",
            data=payments
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/users/{user_id}", dependencies=[Depends(security.access_token_required)], response_model=GeneralResponse[List[PaymentResponse]])
async def get_payments_by_fields(
    user_id: int,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
) -> PaymentResponse:
    """
    Retrieve payments by user ID.
    """
    try:
        payment = await use_case.get_payments_by_fields(user_id=user_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return GeneralResponse[List[PaymentResponse]](
            status="success",
            message="Payment retrieved successfully",
            data=payment
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
