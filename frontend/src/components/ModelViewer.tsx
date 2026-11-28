
"use client";

import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import {
  Bounds,
  Html,
  OrbitControls,
  useGLTF,
  useProgress,
} from "@react-three/drei";

interface ModelViewerProps {
  modelUrl: string;
}

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);

  return (
    <Bounds fit clip observe margin={1.3}>
      <primitive object={scene} />
    </Bounds>
  );
}

function LoadingScreen() {
  const { progress } = useProgress();

  return (
    <Html center>
      <div className="rounded-lg bg-slate-900 px-4 py-3 text-sm text-white whitespace-nowrap">
        Loading model... {Math.round(progress)}%
      </div>
    </Html>
  );
}

export default function ModelViewer({ modelUrl }: ModelViewerProps) {
  return (
    <div className="h-[420px] w-full overflow-hidden rounded-xl bg-[#090d18]">
      <Canvas camera={{ position: [4, 3, 5], fov: 45 }}>
        <color attach="background" args={["#090d18"]} />

        <ambientLight intensity={1.5} />
        <directionalLight position={[5, 5, 5]} intensity={2} />
        <directionalLight position={[-5, -3, -5]} intensity={1} />

        <Suspense fallback={<LoadingScreen />}>
          <Model url={modelUrl} />
        </Suspense>

        <OrbitControls
          makeDefault
          enableDamping
          minDistance={1}
          maxDistance={15}
        />
      </Canvas>
    </div>
  );
}
