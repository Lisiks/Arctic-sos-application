from fastapi import APIRouter, Depends, Path
from fastapi import Response
from typing import Annotated, Optional
from uuid import uuid4


from ..services import RepotsService
from ..utils import auth
from ..models.users_models import UserJWTModel

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{report_id}")
async def get_report(
    service: Annotated[RepotsService, Depends(RepotsService)],
    user_data: Annotated[UserJWTModel, Depends(auth)],
    report_id: Annotated[int, Path(ge=1, le=5)]
):
    match report_id:
        case 1: 
            buffer = await service.create_message_per_type_report(user_data)
        case 2: 
            buffer = await service.create_creaction_avg_report(user_data)
        case 3: 
            buffer = await service.create_lie_acts_percent_report(user_data)
        case 4: 
            buffer = await service.create_lifesaving_devices_ready_count_report(user_data)
        case _: 
            buffer = await service.create_message_per_season_report(user_data)

    filename = f"report_{uuid4()}.xlsx"
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


    
