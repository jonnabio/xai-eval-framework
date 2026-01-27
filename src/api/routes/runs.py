"""
Experiment runs endpoints.

Provides access to experiment results:
- List all runs with filtering and pagination
- Get single run by ID
"""

from fastapi import APIRouter, HTTPException, Query, status, Request
from typing import Optional, List
from datetime import datetime
import logging
from src.api.limiter import limiter

from src.api.models.schemas import (
    Run, RunsResponse, RunResponse,
    ExperimentResultResponse, InstancesResponse
)
from src.api.services.data_loader import (
    load_experiments_with_filters, load_all_experiments,
    get_experiment_result, get_instances_paginated
)
from src.api.services.transformer import transform_experiment_to_run
from src.api.config import settings
from src.api.utils.pagination import paginate_list

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/runs",
    response_model=RunsResponse,
    summary="List Experiment Runs",
    description="Get all experiment runs with optional filtering and pagination",
    tags=["Runs"]
)
@limiter.limit("100/minute")
async def get_runs(
    request: Request,
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
        
        # Load experiments with filters (using generator)
        from src.api.services.data_loader import iter_experiments_with_filters
        experiments_iter = iter_experiments_with_filters(**filters)
        logger.info(f"Scanning experiments matching filters...")
        
        # Transform to Run models on the fly
        runs: List[Run] = []
        failed_count = 0
        total_scanned = 0
        
        for exp_data in experiments_iter:
            total_scanned += 1
            try:
                run = transform_experiment_to_run(exp_data)
                runs.append(run)
            except Exception as e:
                # logger.warning(f"Failed to transform experiment: {e}")
                failed_count += 1
        
        if failed_count > 0:
            logger.warning(f"Failed to transform {failed_count} experiments out of {total_scanned}")
        
        # Apply pagination
        paginated_runs, pagination = paginate_list(runs, offset, limit)
        
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
                   f"(total: {pagination['total']}, offset: {offset})")
        
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
@limiter.limit("50/minute")
async def get_run(request: Request, run_id: str):
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


@router.get(
    "/runs/{run_id}/details",
    response_model=ExperimentResultResponse,
    summary="Get Detailed Results",
    description="Get complete experiment results including aggregated metrics and metadata",
    tags=["Runs"]
)
async def get_run_details(run_id: str):
    """
    Get detailed breakdown of experiment results.
    """
    try:
        result = get_experiment_result(run_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Run not found: {run_id}"
            )
            
        return ExperimentResultResponse(
            data=result,
            metadata={
                "version": settings.API_VERSION,
                "timestamp": datetime.now().isoformat()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting detailed results for {run_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading details: {str(e)}"
        )


@router.get(
    "/runs/{run_id}/instances",
    response_model=InstancesResponse,
    summary="Get Instance Evaluations",
    description="Get paginated list of instance-level evaluations",
    tags=["Runs"]
)
async def get_run_instances(
    run_id: str,
    limit: int = Query(
        settings.RESULTS_DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.RESULTS_MAX_INSTANCES_PER_REQUEST,
        description=f"Number of instances (max: {settings.RESULTS_MAX_INSTANCES_PER_REQUEST})"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of instances to skip"
    )
):
    """
    Get paginated instance evaluations.
    """
    try:
        # Verify run exists first (optional, but good for 404)
        # get_instances_paginated returns empty list if run not found, 
        # but we might want explicit 404.
        # But for efficiency, we just call the service. 
        # Service returns tuple (List, total). If total is 0, it might mean empty or not found.
        # To be strict, check existence.
        
        # Check existence efficiently?
        # get_experiment_result is cached.
        result = get_experiment_result(run_id)
        if not result:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Run not found: {run_id}"
            )
        
        instances, pagination = get_instances_paginated(run_id, offset, limit)
        
        return InstancesResponse(
            data=instances,
            pagination=pagination,
            metadata={
                "version": settings.API_VERSION,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting instances for {run_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading instances: {str(e)}"
        )
