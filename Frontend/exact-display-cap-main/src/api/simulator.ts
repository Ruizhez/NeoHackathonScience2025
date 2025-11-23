/**
 * API client for Simulator Agent backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SimulationRequest {
  simulator_path: string;
  demand: string;
  k?: number;
}

export interface SimulationResponse {
  success: boolean;
  data?: {
    experiment_name: string;
    experiment_description: string;
    runs: Array<{
      inputs: Record<string, number>;
      final: Record<string, number>;
      raw_keys?: string[];
      error?: string;
    }>;
    selection_summary: {
      objective: {
        type: string;
        target: string;
      };
      candidate_count: number;
      success_count: number;
    };
  };
  error?: string;
}

/**
 * Run simulation with the backend
 */
export async function runSimulation(
  request: SimulationRequest
): Promise<SimulationResponse> {
  try {
    console.log('🔵 Sending request to backend:', request);
    console.log('🔵 API URL:', `${API_BASE_URL}/api/simulate`);

    const response = await fetch(`${API_BASE_URL}/api/simulate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    console.log('🔵 Response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('🔴 Backend error response:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const data = await response.json();
    console.log('🟢 Backend response:', data);
    return data;
  } catch (error) {
    console.error('🔴 Error calling simulation API:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Check if API server is healthy
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
