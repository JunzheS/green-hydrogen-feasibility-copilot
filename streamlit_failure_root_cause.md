# Streamlit Cloud Deployment Failure — Root Cause Analysis

**Date:** 2026-06-09
**Commit:** `a36c9b4`

---

## Error Observed

```
Health check failed.
Expected: localhost:8501
Observed: Uvicorn server started on 0.0.0.0:8502
Error: Get "http://localhost:8501/healthz": connect: connection refused
```

---

## Root Cause

| Factor | Detail |
|--------|--------|
| **File** | `.streamlit/config.toml` |
| **Line** | `port = 8502` |
| **Why it was there** | Set during local development to avoid port conflicts when port 8501 was already in use |
| **Why it broke deployment** | Streamlit Cloud health-checks port **8501** by default. The config file explicitly set the server to start on **8502**, causing the health check to fail against the wrong port. |

The error message "Uvicorn server started on 0.0.0.0:8502" is Streamlit Cloud's internal detection message — there is no actual Uvicorn code in the project. The port mismatch caused Streamlit Cloud to report that a "Uvicorn server" was running on the wrong port instead of the expected Streamlit server on port 8501.

---

## Fix Applied

| Before | After |
|--------|-------|
| `[server]` | `[server]` |
| `headless = true` | `headless = true` |
| `port = 8502` | *(removed)* |

### What unchanged

```
[theme]
primaryColor = "#2E7D32"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1F8E9"
textColor = "#1B5E20"
font = "sans serif"

[client]
showSidebarNavigation = true
```

---

## Why the Fix Works

| Context | Behavior |
|---------|----------|
| **Local development** | Without a port override, Streamlit uses the first available port (8501, or next available). |
| **Streamlit Cloud** | Streamlit Cloud automatically overrides the port. But if an explicit port is set, it may conflict with Cloud's health-check system. |

---

## Commit

```
a36c9b4 — fix(streamlit): cloud deployment compatibility
Remove explicit port = 8502 from .streamlit/config.toml
```

Pushed to `main` on https://github.com/JunzheS/green-hydrogen-feasibility-copilot.

---

## Expected Result After Redeploy

1. Streamlit starts on the default port (8501)
2. Streamlit Cloud health check succeeds against `localhost:8501/healthz`
3. Application becomes accessible at the Streamlit Cloud URL

---

## Verification

After the fix is deployed, go to [share.streamlit.io](https://share.streamlit.io), select the app, and click **"Reboot"** (or redeploy). The deployment should now complete successfully.
