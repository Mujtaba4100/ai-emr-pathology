from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.security import get_current_user, require_role

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload/")
async def upload_report(
    file: UploadFile = File(...),
    current_user = Depends(require_role("doctor", "lab_tech", "admin"))
):
    """
    Upload a pathology report
    
    Allowed: Doctor, Lab Tech, Admin
    Denied: Unauthorized users
    """
    return {
        "filename": file.filename,
        "uploaded_by": current_user.username,
        "role": current_user.role,
        "message": "File received (implementation in Phase 2)"
    }

@router.put("/report/{report_id}")
async def update_report(
    report_id: int,
    current_user = Depends(require_role("lab_tech", "admin"))
):
    """
    Modify a report result
    
    Allowed: Lab Tech, Admin
    Denied: Doctors (cannot edit results)
    """
    return {
        "report_id": report_id,
        "modified_by": current_user.username,
        "role": current_user.role,
        "message": "Report updated (implementation in Phase 2)"
    }

@router.delete("/report/{report_id}")
async def delete_report(
    report_id: int,
    current_user = Depends(require_role("admin"))
):
    """
    Delete a report
    
    Allowed: Admin only
    Denied: Doctors and Lab Techs
    """
    return {
        "report_id": report_id,
        "deleted_by": current_user.username,
        "role": current_user.role,
        "message": "Report deleted (implementation in Phase 2)"
    }

@router.get("/reports/")
async def list_reports(
    current_user = Depends(require_role("doctor", "lab_tech", "admin"))
):
    """
    List all reports accessible to user
    
    Allowed: Doctor, Lab Tech, Admin
    Doctors see only their uploaded reports
    Lab Techs and Admins see all
    """
    if current_user.role == "doctor":
        # Show only doctor's reports
        return {
            "reports": [],
            "filtered_by": "user",
            "role": current_user.role
        }
    else:
        # Show all reports
        return {
            "reports": [],
            "filtered_by": "none",
            "role": current_user.role
        }
