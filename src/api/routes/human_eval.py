"""
Human evaluation endpoints for annotation system.

Provides:
- Sample retrieval for annotators
- Annotation submission
- Progress tracking
- Admin statistics and export
"""

from fastapi import APIRouter, HTTPException, Query, status, Response, Request, Depends
from typing import Optional
from datetime import datetime
import logging
from src.api.limiter import limiter
from src.api.dependencies import get_current_admin

from src.api.models.schemas import (
    HumanEvalSamplesResponse,
    HumanAnnotationSubmission,
    AnnotationSubmissionResponse,
    ProgressResponse,
    AdminStatsResponse,
    AdminAnnotationsResponse
)
from src.api.services import human_eval_service as service
from src.api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# =============================================================================
# ANNOTATOR ENDPOINTS
# =============================================================================

@router.get(
    "/samples",
    response_model=HumanEvalSamplesResponse,
    summary="Get Samples for Annotation",
    description="Retrieve samples assigned to an annotator for human evaluation",
    tags=["Human Evaluation"]
)
@limiter.limit("20/minute")
async def get_samples(
    request: Request,
    annotator_id: Optional[str] = Query(
        None,
        description="Filter by annotator ID. If not provided, returns all samples."
    ),
    include_completed: bool = Query(
        False,
        description="Include already-annotated samples"
    )
):
    """
    Get samples for annotation.

    - If annotator_id provided: Returns only samples assigned to that annotator
    - If include_completed=False: Excludes samples already annotated by this annotator
    - Samples DO NOT include LLM scores (blind evaluation)
    """
    logger.info(f"GET /human-eval/samples - annotator={annotator_id}, include_completed={include_completed}")

    try:
        if annotator_id:
            samples = service.get_samples_for_annotator(annotator_id, include_completed)
            annotator = annotator_id
        else:
            samples = service.get_all_samples()
            annotator = "all"

        # Get completion stats
        if annotator_id:
            completed = len(service.get_completed_sample_ids(annotator_id))
        else:
            completed = len(service.get_all_completed_samples())
        
        # Calculate pending properly
        total = len(samples) # This is filtered length
        # But for metadata we might want global stats
        
        metadata = {
            "version": settings.API_VERSION,
            "timestamp": datetime.now().isoformat(),
            "annotator": annotator,
            "total_returned": len(samples),
            "completed_count": completed
        }

        return HumanEvalSamplesResponse(
            data=samples,
            metadata=metadata
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting samples: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading samples: {str(e)}"
        )

@router.post(
    "/annotations",
    response_model=AnnotationSubmissionResponse,
    summary="Submit Annotation",
    description="Submit a human annotation for a sample",
    tags=["Human Evaluation"]
)
@limiter.limit("10/minute")
async def submit_annotation(request: Request, submission: HumanAnnotationSubmission):
    """
    Submit an annotation.

    - Validates sample_id exists
    - Prevents duplicate submissions (idempotent)
    - Saves to filesystem with atomic write
    - Updates progress metadata
    """
    logger.info(f"POST /human-eval/annotations - sample={submission.sample_id}, annotator={submission.annotator_id}")

    try:
        success, annotation_id, message = service.save_annotation(submission)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )

        # Get updated progress
        progress = service.get_annotator_progress(submission.annotator_id)

        return AnnotationSubmissionResponse(
            status="success",
            annotation_id=annotation_id,
            message=message,
            progress={
                "completed": progress.completed,
                "remaining": progress.pending
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting annotation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving annotation: {str(e)}"
        )

@router.get(
    "/progress",
    response_model=ProgressResponse,
    summary="Get Progress",
    description="Get annotation progress for an annotator",
    tags=["Human Evaluation"]
)
@limiter.limit("60/minute")
async def get_progress(
    request: Request,
    annotator_id: str = Query(..., description="Annotator ID")
):
    """
    Get progress statistics for an annotator.

    Returns:
    - Total assigned samples
    - Completed count
    - Pending count
    - Completion rate
    - Average time per annotation
    """
    logger.info(f"GET /human-eval/progress - annotator={annotator_id}")

    try:
        progress = service.get_annotator_progress(annotator_id)

        return ProgressResponse(
            data=progress,
            metadata={
                "version": settings.API_VERSION,
                "timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        logger.error(f"Error getting progress: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading progress: {str(e)}"
        )

# =============================================================================
# ADMIN ENDPOINTS (Protected)
# =============================================================================

@router.get(
    "/admin/stats",
    response_model=AdminStatsResponse,
    summary="Get Admin Statistics",
    description="Get overall annotation statistics (admin only)",
    tags=["Human Evaluation - Admin"],
    dependencies=[Depends(get_current_admin)]
)
@limiter.limit("20/minute")
async def get_admin_stats(request: Request):
    """
    Get system-wide statistics.

    Includes:
    - Total samples and annotators
    - Overall completion rate
    - Per-annotator breakdown
    - Per-experiment breakdown
    """
    logger.info("GET /human-eval/admin/stats")

    try:
        stats = service.get_admin_stats()

        return AdminStatsResponse(
            data=stats,
            metadata={
                "version": settings.API_VERSION,
                "timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        logger.error(f"Error getting admin stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading statistics: {str(e)}"
        )

@router.get(
    "/admin/annotations",
    summary="Export All Annotations",
    description="Export all annotations with LLM scores for analysis (admin only)",
    tags=["Human Evaluation - Admin"],
    dependencies=[Depends(get_current_admin)]
)
@limiter.limit("10/minute")
async def get_all_annotations(
    request: Request,
    format: str = Query("json", description="Export format: 'json' or 'csv'")
):
    """
    Export all annotations.

    - format=json: Returns JSON array with human + LLM scores
    - format=csv: Returns CSV file for Excel/analysis

    Used for Cohen's kappa analysis.
    """
    logger.info(f"GET /human-eval/admin/annotations - format={format}")

    try:
        if format.lower() == "csv":
            csv_data = service.export_annotations_csv()
            return Response(
                content=csv_data,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=annotations_{datetime.now().strftime('%Y%m%d')}.csv"
                }
            )
        else:
            # JSON format
            data = service.get_all_annotations_with_llm_scores()

            return AdminAnnotationsResponse(
                data=data,
                metadata={
                    "version": settings.API_VERSION,
                    "timestamp": datetime.now().isoformat(),
                    "total_annotations": len(data),
                    "format": "json"
                }
            )

    except Exception as e:
        logger.error(f"Error exporting annotations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting annotations: {str(e)}"
        )
