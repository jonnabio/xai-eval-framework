# Production Monitoring and Maintenance Guide

## 🏥 Health Checks

### Backend API
The API provides a dedicated health check endpoint:

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.2.0",
  "environment": "production"
}
```

**Monitoring Strategy:**
- Configure your deployment platform (e.g., Railway) to ping this endpoint every 60 seconds.
- Alert on any non-200 status code.

## 📝 Logging & Error Tracking

### Application Logs
- **Location**: stdout/stderr (Standard Container Logs)
- **Format**: Structured JSON logging (via `structlog` or standard python logging if configured).
- **Levels**:
  - `INFO`: Access logs, experiment start/finish.
  - `ERROR`: Uncaught exceptions, API validation errors.
  - `WARNING`: Deprecated features, non-critical data issues.

### Log Retention
- **Development**: Logs are transient.
- **Production**: Use a log aggregator (e.g., Railway Logs, Datadog) to retain logs for at least 14 days.

## 💾 Backup Procedures

### Data Persistence
Experiment results are stored in the filesystem under `experiments/<experiment_id>/results/`.

**Recommended Backup Strategy:**
1.  **Daily Snapshot**:
    ```bash
    tar -czf backup_experiments_$(date +%Y%m%d).tar.gz experiments/
    ```
2.  **Offsite Storage**: Upload the snapshot to S3 or Google Drive.
3.  **Git Storage**: The repository itself contains configuration and code. Ensure `main` is always pushed to GitHub.

## 🔧 Maintenance Schedule

| Frequency | Task | Description |
| :--- | :--- | :--- |
| **Weekly** | Dependency Audit | Run `pip audit` to check for security vulnerabilities. |
| **Weekly** | Log Review | Check for recurring warnings or silent failures in logs. |
| **Monthly** | Backup Verification | Restore a backup to a temporary environment to verify integrity. |
| **Quarterly** | Dependency Update | underlying libraries (FastAPI, Scikit-learn) update. |

## 🚨 Incident Response Plan

### Severity Levels
- **Sev-1 (Critical)**: API down, data loss risk. -> *Immediate Action*
- **Sev-2 (High)**: High error rate (>5%), specific endpoints failing. -> *Fix within 24h*
- **Sev-3 (Medium)**: Visual bugs, slow performance. -> *Fix in next sprint*

### Response Steps
1.  **Acknowledge**: Confirm receipt of alert.
2.  **Triaging**: Check `/docs` (Swagger) and logs.
3.  **Rollback**: If caused by a recent deployment, revert to previous Docker tag.
    ```bash
    # Example Railway CLI
    railway rollback
    ```
4.  **Fix**: Apply hotfix to `main`, tag `vX.X.X-hotfix`, deploy.
5.  **Post-Mortem**: Document root cause in `docs/incidents/`.
