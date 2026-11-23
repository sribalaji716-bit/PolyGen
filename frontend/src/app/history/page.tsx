
"use client";

import { useCallback, useEffect, useState } from "react";

interface GenerationJob {
  job_id: string;
  prompt: string;
  status: "pending" | "processing" | "completed" | "failed";
  asset_path: string | null;
}

const API_URL = "http://127.0.0.1:8000";

export default function HistoryPage() {
  const [jobs, setJobs] = useState<GenerationJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);

  const limit = 10;

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/prompt/history?limit=${limit}&offset=${offset}`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch generation history");
      }

      const data: GenerationJob[] = await response.json();

      setJobs(data);
      setHasMore(data.length === limit);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }, [offset]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const statusStyle: Record<string, string> = {
    pending: "bg-yellow-500/10 text-yellow-400",
    processing: "bg-blue-500/10 text-blue-400",
    completed: "bg-green-500/10 text-green-400",
    failed: "bg-red-500/10 text-red-400",
  };

  return (
    <main className="min-h-screen bg-[#090d18] px-6 py-10 text-white md:px-12">
      <div className="mx-auto max-w-6xl">

        <div className="mb-10 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="mb-2 text-sm font-semibold text-violet-400">
              POLYGEN WORKSPACE
            </p>
            <h1 className="text-3xl font-bold">
              Generation History
            </h1>
            <p className="mt-2 text-sm text-gray-400">
              Track your previous 3D generation requests.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={fetchHistory}
              disabled={loading}
              className="rounded-xl border border-white/10 px-4 py-3 text-sm text-gray-300 hover:bg-white/5 disabled:opacity-50"
            >
              {loading ? "Refreshing..." : "Refresh"}
            </button>

            <a
              href="/"
              className="rounded-xl bg-violet-600 px-4 py-3 text-sm font-semibold hover:bg-violet-500"
            >
              Create Asset
            </a>
          </div>
        </div>

        <div className="mb-6 grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-[#111827] p-5">
            <p className="text-sm text-gray-400">Jobs on this page</p>
            <p className="mt-2 text-3xl font-bold">{jobs.length}</p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-[#111827] p-5">
            <p className="text-sm text-gray-400">Completed</p>
            <p className="mt-2 text-3xl font-bold text-green-400">
              {jobs.filter((job) => job.status === "completed").length}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-[#111827] p-5">
            <p className="text-sm text-gray-400">Failed</p>
            <p className="mt-2 text-3xl font-bold text-red-400">
              {jobs.filter((job) => job.status === "failed").length}
            </p>
          </div>
        </div>

        <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#111827]">
          <div className="border-b border-white/10 p-5">
            <h2 className="font-semibold">Previous Generations</h2>
          </div>

          {loading ? (
            <div className="p-10 text-center text-gray-400">
              Loading generation history...
            </div>
          ) : error ? (
            <div className="p-10 text-center text-red-400">
              {error}
              <button
                onClick={fetchHistory}
                className="ml-3 text-violet-400 underline"
              >
                Retry
              </button>
            </div>
          ) : jobs.length === 0 ? (
            <div className="p-10 text-center">
              <p className="text-gray-300">No generation history found.</p>
              <p className="mt-2 text-sm text-gray-500">
                Your generation requests will appear here.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-white/[0.03] text-gray-400">
                  <tr>
                    <th className="p-4">Prompt</th>
                    <th className="p-4">Job ID</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Asset</th>
                  </tr>
                </thead>

                <tbody>
                  {jobs.map((job) => (
                    <tr
                      key={job.job_id}
                      className="border-t border-white/5"
                    >
                      <td className="max-w-xs p-4 text-gray-200">
                        {job.prompt}
                      </td>

                      <td className="p-4 font-mono text-xs text-gray-500">
                        {job.job_id.slice(0, 8)}...
                      </td>

                      <td className="p-4">
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${
                            statusStyle[job.status]
                          }`}
                        >
                          {job.status}
                        </span>
                      </td>

                      <td className="p-4 text-xs text-gray-400">
                        {job.asset_path ? "Generated" : "Not available"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button
            disabled={offset === 0 || loading}
            onClick={() => setOffset((previous) => Math.max(0, previous - limit))}
            className="rounded-xl border border-white/10 px-5 py-3 text-sm disabled:opacity-30"
          >
            Previous
          </button>

          <span className="text-sm text-gray-500">
            Page {Math.floor(offset / limit) + 1}
          </span>

          <button
            disabled={!hasMore || loading}
            onClick={() => setOffset((previous) => previous + limit)}
            className="rounded-xl border border-white/10 px-5 py-3 text-sm disabled:opacity-30"
          >
            Next
          </button>
        </div>

      </div>
    </main>
  );
}
