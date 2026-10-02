from fastapi import APIRouter

from .crews_routes import router as crew_router
from .help_messages_routes import router as hm_router
from .lie_act_routes import router as la_router
from .lifesaving_devices_routes import router as ld_router
from .operation_act_routes import router as oa_router
from .react_plans_routes import router as rp_router
from .html_routes import router as html_router

router = APIRouter()


router.include_router(crew_router)
router.include_router(hm_router)
router.include_router(la_router)
router.include_router(ld_router)
router.include_router(oa_router)
router.include_router(rp_router)
router.include_router(html_router)

__all__ = [
    "router"
]