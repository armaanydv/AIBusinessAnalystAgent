# AIBA Zero-Cost Deployment & Student Portfolio Guide

This guide explains how to containerize, test, and host the **AIBA (AI Business Analyst Agent)** platform **100% free of charge**, making it ready for resumes, portfolio demos, and technical interviews.

---

## Architecture Overview

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        FREE PRODUCTION STACK                           │
├───────────────────────────────────┬────────────────────────────────────┤
│         FRONTEND HOSTING          │          BACKEND HOSTING           │
│         Platform: Vercel          │   Platform: Hugging Face Spaces    │
│        Cost: $0.00 / month        │        Cost: $0.00 / month         │
│         RAM / CPU: Edge CDN       │       RAM / CPU: 16 GB RAM         │
│   Build: React 19 + Vite + Nginx  │   Container: Dockerfile (FastAPI)  │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## Path 1: Local Containerization with Docker Compose

To test the entire stack locally before cloud deployment, run both the backend and frontend in Docker:

### 1. Requirements
* Docker Desktop installed and running.

### 2. Launch with One Command
From the project root (`AIBAagent`):
```bash
docker compose up --build
```

### 3. Verification
* **Frontend**: Open `http://localhost:5173`
* **Backend API**: Open `http://localhost:8000/docs`
* **Volumes**:
  * `aiba_documents_data`: Persists your indexed PDFs, FAISS indices, and metadata across restarts.
  * `aiba_model_cache_data`: Caches downloaded Hugging Face models so they are never redownloaded.

---

## Path 2: Free 24/7 Cloud Hosting (Hugging Face + Vercel)

This setup costs **$0.00** and gives you a live public link for your resume.

### Step 1: Deploy Backend to Hugging Face Spaces (16 GB RAM Free)

1. Create a free account at [huggingface.co](https://huggingface.co/).
2. Click **New Space** (`https://huggingface.co/new-space`).
3. Fill in:
   * **Space name**: `aiba-backend`
   * **License**: `mit` or `apache-2.0`
   * **SDK**: Select **Docker** -> **Blank**.
   * **Space Hardware**: Choose **CPU basic (2 vCPU · 16 GB RAM · Free)**.
4. Clone your new Space repository to a temporary folder or upload files directly:
   * Copy `backend/Dockerfile`
   * Copy `backend/requirements.txt`
   * Copy `backend/app` directory
5. Add a `README.md` in the Space root with this YAML header:
   ```yaml
   ---
   title: AIBA RAG Backend API
   emoji: 📊
   colorFrom: blue
   colorTo: indigo
   sdk: docker
   app_port: 7860
   ---
   ```
6. In your Hugging Face Space **Settings** -> **Variables and secrets**:
   * Add secret `GROQ_API_KEY`: `<your-groq-key>`
   * Add secret `GEMINI_API_KEY`: `<your-gemini-key>` (optional)
   * Add secret `PORT`: `7860`
7. Click **Build Space**. Once built, Hugging Face provides your public API URL:
   `https://<your-username>-aiba-backend.hf.space`

---

### Step 2: Deploy Frontend to Vercel (100% Free Edge CDN)

1. Push your repository to **GitHub**.
2. Go to [vercel.com](https://vercel.com/) and sign in with GitHub.
3. Click **Add New Project** and select your `AIBAagent` repository.
4. Configure the build settings:
   * **Framework Preset**: `Vite`
   * **Root Directory**: Click edit and choose `frontend`.
   * **Build Command**: `npm run build`
   * **Output Directory**: `dist`
5. In **Environment Variables**, add:
   * `VITE_API_BASE_URL`: `https://<your-username>-aiba-backend.hf.space` (or your backend URL)
6. Click **Deploy**. In under 60 seconds, your frontend is live at:
   `https://your-project.vercel.app`

*Note: The included `frontend/vercel.json` automatically handles client-side routing so refreshing `/chat` or `/dashboard` does not cause 404 errors.*

---

## Path 3: GitHub Student Developer Pack ($200 DigitalOcean Credits)

If you are a student with a college or `.edu` email address:

1. Apply at [education.github.com/pack](https://education.github.com/pack).
2. Once approved (usually takes 24–48 hours), claim the **DigitalOcean $200 promo code**.
3. Create a **4 GB RAM Droplet** (Docker One-Click image) on DigitalOcean for ~$24/month. With $200 credits, this runs for **8+ months completely free**.
4. Clone your repo onto the droplet and run:
   ```bash
   docker compose up -d
   ```

---

## Path 4: Demo-On-Demand via Cloudflare Tunnel (Zero Cloud Cost)

If you have an interview and want the interviewer to test your local laptop's backend without hosting it in the cloud:

1. Install Cloudflare `cloudflared` (or `ngrok`):
   ```powershell
   winget install Cloudflare.cloudflared
   ```
2. Start your backend locally:
   ```powershell
   uvicorn app.main:app --reload
   ```
3. Expose port 8000 via a secure tunnel:
   ```powershell
   cloudflared tunnel --url http://localhost:8000
   ```
4. Cloudflare outputs a temporary public HTTPS link (e.g. `https://random-subdomain.trycloudflare.com`).
5. Open your deployed Vercel frontend, navigate to **Settings**, and paste this URL into the **Backend API Endpoint** input. The frontend connects to your local machine instantly!

---

## Testing Your Implementation

Before publishing, verify your backend tests pass:
```bash
pytest tests/test_api.py -v
```
