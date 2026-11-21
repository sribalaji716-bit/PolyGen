
import { checkBackendHealth } from "./api";

async function testBackend() {
  try {
    const result = await checkBackendHealth();
    console.log("Backend Connection Successful:", result);
  } catch (error) {
    console.error("Backend Connection Failed:", error);
  }
}

testBackend();
