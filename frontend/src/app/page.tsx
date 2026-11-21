
"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");

  return (
    <main className="min-h-screen bg-[#090d18] text-white">
      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="hidden w-64 shrink-0 border-r border-white/10 bg-[#0d1322] p-6 lg:flex lg:flex-col">
          <div className="mb-12 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-600 text-xl font-bold">
              P
            </div>
            <div>
              <h1 className="text-xl font-bold">PolyGen</h1>
              <p className="text-xs text-gray-500">AI 3D Workspace</p>
            </div>
          </div>

          <p className="mb-4 text-xs font-semibold uppercase tracking-widest text-gray-500">
            Workspace
          </p>

          <nav className="space-y-2">
            <div className="rounded-xl bg-violet-600/15 px-4 py-3 text-sm font-medium text-violet-300">
              ✦ Create Asset
            </div>
            <div className="rounded-xl px-4 py-3 text-sm text-gray-400">
              ◈ My Assets
            </div>
            <div className="rounded-xl px-4 py-3 text-sm text-gray-400">
              ◷ Generation History
            </div>
          </nav>

          <div className="mt-auto rounded-xl border border-white/10 bg-white/[0.03] p-4">
            <p className="text-sm font-semibold">PolyGen Engine</p>
            <p className="mt-2 text-xs text-gray-500">
              Text-to-3D generation
            </p>
            <div className="mt-3 flex items-center gap-2 text-xs text-amber-400">
              <span className="h-2 w-2 rounded-full bg-amber-400" />
              Engine setup pending
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <section className="min-w-0 flex-1">

          {/* Header */}
          <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 px-6 py-5 md:px-10">
            <div>
              <h2 className="text-lg font-semibold">AI Workspace</h2>
              <p className="text-xs text-gray-500">
                Create your imagination in 3D
              </p>
            </div>

            <div className="flex items-center gap-3">
              <span className="rounded-full border border-white/10 px-3 py-2 text-xs text-gray-400">
                Free Workspace
              </span>
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-violet-600 font-semibold">
                S
              </div>
            </div>
          </header>

          {/* Dashboard */}
          <div className="mx-auto max-w-7xl p-6 md:p-10">

            <div className="mb-8">
              <p className="mb-2 text-sm font-medium text-violet-400">
                GENERATIVE AI · TEXT TO 3D
              </p>
              <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
                Bring your ideas to <span className="text-violet-400">life.</span>
              </h1>
              <p className="mt-3 text-sm text-gray-400">
                Describe an object and prepare it for 3D generation.
              </p>
            </div>

            {/* Prompt Section */}
            <div className="mb-8 rounded-2xl border border-white/10 bg-[#111827] p-5 md:p-7">
              <div className="mb-5 flex items-center justify-between">
                <h2 className="font-semibold">Create a 3D Model</h2>
                <span className="text-xs text-gray-500">TEXT PROMPT</span>
              </div>

              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your 3D model... Example: A futuristic red sports car with aerodynamic body, detailed wheels and metallic finish."
                maxLength={1000}
                rows={4}
                className="w-full resize-none rounded-xl border border-white/10 bg-[#090d18] p-4 text-sm text-white outline-none transition placeholder:text-gray-600 focus:border-violet-500"
              />

              <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                <p className="text-xs text-gray-500">
                  Be descriptive for better 3D results.
                </p>
                <p className="text-xs text-gray-500">
                  {prompt.length}/1000
                </p>
              </div>

              <div className="mt-5 flex flex-wrap items-center gap-3">
                <button
                  disabled={!prompt.trim()}
                  className="rounded-xl bg-violet-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  ✦ Generate 3D Asset
                </button>
                <button
                  onClick={() => setPrompt("")}
                  className="rounded-xl border border-white/10 px-5 py-3 text-sm text-gray-400 transition hover:bg-white/5"
                >
                  Clear
                </button>
              </div>

              <p className="mt-3 text-xs text-amber-400">
                Generation engine is not connected yet.
              </p>
            </div>

            {/* Preview Area */}
            <div className="grid gap-6 xl:grid-cols-[1fr_300px]">

              <div className="rounded-2xl border border-white/10 bg-[#111827] p-5">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <h2 className="font-semibold">3D Preview</h2>
                    <p className="mt-1 text-xs text-gray-500">
                      Your generated model will appear here
                    </p>
                  </div>
                  <span className="rounded-lg bg-white/5 px-3 py-2 text-xs text-gray-400">
                    GLB Preview
                  </span>
                </div>

                <div className="flex min-h-[320px] flex-col items-center justify-center rounded-xl border border-dashed border-white/10 bg-[#090d18] p-6 text-center">
                  <div className="mb-5 flex h-24 w-24 items-center justify-center rounded-3xl border border-violet-500/20 bg-violet-500/10 text-5xl">
                    ◈
                  </div>
                  <h3 className="font-medium text-gray-300">
                    Your 3D canvas is ready
                  </h3>
                  <p className="mt-2 max-w-sm text-xs leading-6 text-gray-500">
                    Submit a prompt after connecting the generation engine.
                    Your 3D model will be displayed in this workspace.
                  </p>
                </div>
              </div>

              {/* Status Panel */}
              <div className="rounded-2xl border border-white/10 bg-[#111827] p-5">
                <h2 className="font-semibold">Generation Status</h2>

                <div className="mt-5 rounded-xl border border-white/10 bg-[#090d18] p-4">
                  <p className="text-xs text-gray-500">CURRENT STATUS</p>
                  <div className="mt-3 flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-amber-400" />
                    <span className="text-sm text-amber-400">
                      Waiting for engine
                    </span>
                  </div>
                </div>

                <div className="mt-6 space-y-4">
                  <div>
                    <p className="text-xs text-gray-500">Generation Type</p>
                    <p className="mt-1 text-sm">Text to 3D</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Output Format</p>
                    <p className="mt-1 text-sm">GLB / GLTF</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Recent Assets</p>
                    <p className="mt-1 text-sm text-gray-400">
                      No assets generated yet
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <footer className="mt-10 border-t border-white/10 pt-5 text-center text-xs text-gray-600">
              PolyGen · Generative Text-to-3D Asset Pipeline
            </footer>

          </div>
        </section>
      </div>
    </main>
  );
}
