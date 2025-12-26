# Backend Deployment Guide (Render)

## 🚀 Quick Deployment with Blueprints

The easiest way to deploy the API is using the included `render.yaml` Blueprint.

1.  **Log in to Render**: Go to [dashboard.render.com](https://dashboard.render.com/).
2.  **Create New Blueprint**:
    *   Click the **New +** button.
    *   Select **Blueprint**.
3.  **Connect Repository**:
    *   Select your `xai-eval-framework` repository.
    *   Render will detect the `render.yaml` file.
4.  **Deploy**:
    *   Click **Apply**.
    *   Render will build the Docker image and deploy the service.

## 🔗 Connecting the Frontend

Once the backend is live:
1.  Copy the backend URL (e.g., `https://xai-eval-framework-xyz.onrender.com`).
2.  Go to your **Frontend (xai-benchmark)** project on Render.
3.  Go to **Environment**.
4.  Update/Add `NEXT_PUBLIC_API_URL` with your new backend URL.
    *   **Important**: Do NOT include a trailing slash.
    *   Example: `https://xai-eval-framework-xyz.onrender.com`
5.  Trigger a manual deploy of the frontend (or push a small change) to pick up the new variable.

## 🛠 Manual Setup (Alternative)

If you prefer manual setup:
1.  Create **New Web Service**.
2.  Connect `xai-eval-framework`.
3.  Select **Docker** runtime.
4.  Set Environment Variables:
    *   `API_HOST`: `0.0.0.0`
    *   `API_PORT`: `8000`
    *   `PORT`: `8000`
