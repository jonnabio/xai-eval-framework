"""
Experiment runs endpoints.

Provides access to experiment results:
- List all runs with filtering and pagination
- Get single run by ID
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from datetime import datetime
import logging

from src.api.models.schemas import Run, RunsResponse, RunResponse
from src.api.services.data_loader import load_experiments_with_filters, load_all_experiments
from src.api.services.transformer import transform_experiment_to_run
from src.api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/runs",
    response_model=RunsResponse,
    summary="List Experiment Runs",
    description="Get all experiment runs with optional filtering and pagination",
    tags=["Runs"]
)
async def get_runs(
    dataset: Optional[str] = Query(
        None,
        description="Filter by dataset (e.g., 'AdultIncome', 'CIFAR-10')"
    ),
    method: Optional[str] = Query(
        None,
        description="Filter by XAI method (e.g., 'LIME', 'SHAP')"
    ),
    model_type: Optional[str] = Query(
        None,
        description="Filter by model type (e.g., 'classical', 'cnn')"
    ),
    model_name: Optional[str] = Query(
        None,
        description="Filter by model name (e.g., 'random_forest')"
    ),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description=f"Number of results to return (max: {settings.MAX_PAGE_SIZE})"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of results to skip for pagination"
    )
):
    """
    List all experiment runs with optional filtering and pagination.
    
    Filters can be combined. For example:
    - /api/runs?dataset=AdultIncome&method=LIME
    - /api/runs?model_type=classical&limit=10
    
    Args:
        dataset: Filter by dataset name
        method: Filter by XAI method
        model_type: Filter by model type
        model_name: Filter by model name
        limit: Number of results to return
        offset: Pagination offset
    
    Returns:
        RunsResponse with data, pagination info, and metadata
    """
    logger.info(f"GET /api/runs - Filters: dataset={dataset}, method={method}, "
               f"model_type={model_type}, model_name={model_name}, "
               f"limit={limit}, offset={offset}")
    
    try:
        # Build filters dict (only include non-None values)
        filters = {}
        if dataset:
            filters["dataset"] = dataset
        if method:
            filters["method"] = method
        if model_type:
            filters["model_type"] = model_type
        if model_name:
            filters["model_name"] = model_name
        
        # Load experiments with filters
        experiments = load_experiments_with_filters(**filters)
        logger.info(f"Found {len(experiments)} experiments matching filters")
        
        # Transform to Run models
        runs: List[Run] = []
        failed_count = 0
        
        for exp_data in experiments:
            try:
                run = transform_experiment_to_run(exp_data)
                runs.append(run)
            except Exception as e:
                logger.warning(f"Failed to transform experiment: {e}")
                failed_count += 1
        
        if failed_count > 0:
            logger.warning(f"Failed to transform {failed_count} experiments")
        
        # Calculate pagination
        total = len(runs)
        start = offset
        end = min(offset + limit, total)
        
        # Apply pagination
        paginated_runs = runs[start:end]
        
        # Build pagination metadata
        pagination = {
            "total": total,
            "limit": limit,
            "offset": offset,
            "returned": len(paginated_runs),
            "hasNext": end < total,
            "hasPrev": offset > 0
        }
        
        # Build response
        response = RunsResponse(
            data=paginated_runs,
            pagination=pagination,
            metadata={
                "version": settings.API_VERSION,
                "timestamp": datetime.now().isoformat(),
                "filters_applied": filters
            }
        )
        
        logger.info(f"Returning {len(paginated_runs)} runs "
                   f"(total: {total}, offset: {offset})")
        
        return response
    
    except Exception as e:
        logger.error(f"Error getting runs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading runs: {str(e)}"
        )

@router.get(
    "/runs/{run_id}",
    response_model=RunResponse,
    summary="Get Single Run",
    description="Get detailed information about a specific run",
    tags=["Runs"],
    responses={
        200: {
            "description": "Run found and returned",
            "model": RunResponse
        },
        404: {
            "description": "Run not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Run not found: adult_rf_lime_a3b2c1",
                        "timestamp": "2024-01-15T10:30:00"
                    }
                }
            }
        }
    }
)
async def get_run(run_id: str):
    """
    Get detailed information about a specific run.
    
    Args:
        run_id: Unique run identifier (from Run.id field)
    
    Returns:
        RunResponse with single Run data
    
    Raises:
        HTTPException 404: If run with given ID not found
    """
    logger.info(f"GET /api/runs/{run_id}")
    
    try:
        experiments = load_all_experiments()
        logger.info(f"Searching {len(experiments)} experiments for ID: {run_id}")
        
        # Transform and find matching run
        for exp_data in experiments:
            try:
                run = transform_experiment_to_run(exp_data)
                if run.id == run_id:
                    logger.info(f"Found run: {run_id}")
                    return RunResponse(
                        data=run,
                        metadata={
                            "version": settings.API_VERSION,
                            "timestamp": datetime.now().isoformat()
                        }
                    )
            except Exception as e:
                logger.warning(f"Failed to transform experiment: {e}")
                continue
        
        # Run not found
        logger.warning(f"Run not found: {run_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error getting run {run_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading run: {str(e)}"
        )
