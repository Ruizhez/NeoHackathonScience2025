export type Parameter = {
  id: string;
  name: string;
  desc: string;
  type: string;
  default: string;
  range?: string;
};

export type OutputMetric = {
  id: string;
  name: string;
  desc: string;
  unit: string;
};

export type Simulator = {
  id: string;
  name: string;
  desc: string;
  fileName: string;
  params: Parameter[];
  outputs: OutputMetric[];
};

export type Project = {
  id: string;
  title: string;
  desc: string;
  goal?: string;
  tags: string[];
  createdAt: string;
  simulators: Simulator[];
};

export type NodeType = 'simulator' | 'prompt' | 'result' | 'pdf';

export type NodeData = {
  name?: string;
  fileName?: string;
  params?: Parameter[];
  outputs?: OutputMetric[];
  prompt?: string;
  promptHistory?: string[];
  status?: 'idle' | 'running' | 'complete';
  recommendedParams?: Record<string, string>;
  results?: any[];
  pdfFileName?: string;
};

export type CanvasNode = {
  id: string;
  type: NodeType;
  x: number;
  y: number;
  data: NodeData;
};

export type Edge = {
  id: string;
  source: string;
  target: string;
};
