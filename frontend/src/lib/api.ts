
const API_BASE_URL = "http://127.0.0.1:8000";

export interface GenerationJob {
  job_id: string;
  prompt: string;
  status: "pending" | "processing" | "completed" | "failed";
  asset_path: string | null;
}

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function createGenerationJob(
  prompt: string
): Promise<GenerationJob> {
  const response = await fetch(
    `${API_BASE_URL}/api/prompt/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.detail || "Failed to start 3D generation"
    );
  }

  return response.json();
}

export async function getGenerationStatus(
  jobId: string
): Promise<GenerationJob> {
  const response = await fetch(
    `${API_BASE_URL}/api/prompt/status/${jobId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch generation status");
  }

  return response.json();
}

export function getModelDownloadUrl(jobId: string): string {
  return `${API_BASE_URL}/api/prompt/download/${jobId}`;
}
