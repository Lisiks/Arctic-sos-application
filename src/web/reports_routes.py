from fastapi import APIRouter, Depends, Path
from fastapi import Response
from typing import Annotated, Optional
from uuid import uuid4
import asyncio

from ..database.repositories import ReportsRepository
from ..excel_buffer_manager import ExcelBuferManager

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{report_id}")
async def get_report(
    repo: Annotated[ReportsRepository, Depends(ReportsRepository)],
    report_id: Annotated[int, Path(ge=1, le=5)]
):
    match report_id:
        case 1: 
            report_data = await repo.message_per_type_report()
            report_buffer = await asyncio.to_thread(ExcelBuferManager.make_message_per_type_report, report_data)
        case 2: 
            report_data = await repo.avg_reaction_time_report()
            report_buffer = await asyncio.to_thread(ExcelBuferManager.make_avg_reaction_time_report, report_data)
        case 3: 
            report_data = await repo.lie_acts_count_report()
            report_buffer = await asyncio.to_thread(ExcelBuferManager.make_acts_count_report, report_data)
        case 4: 
            report_data = await repo.lefesaving_device_ready_count_report()
            report_buffer = await asyncio.to_thread(ExcelBuferManager.make_devices_ready_count_report, report_data)
        case _: 
            report_data = await repo.messages_per_seasons_query()
            report_buffer = await asyncio.to_thread(ExcelBuferManager.make_message_per_seasons_report, report_data)

    filename = f"report_{uuid4()}.xlsx"
    return Response(
        content=report_buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


    
