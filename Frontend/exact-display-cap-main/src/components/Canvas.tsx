import { useState, useRef, useEffect } from 'react';
import { ChevronLeft, UploadCloud, Plus, GripHorizontal, MousePointer2, Link as LinkIcon, Edit2, Check, X, FileText } from 'lucide-react';
import { SimulatorNode } from './SimulatorNode';
import { PromptNode } from './PromptNode';
import { ResultNode } from './ResultNode';
import { PDFNode } from './PDFNode';
import type { Project, CanvasNode, Edge } from '@/types';

interface CanvasProps {
  project: Project;
  onBack: () => void;
  onAddSimulator: () => void;
  onConfigureSimulator: (node: CanvasNode) => void;
  onRunRequest: (simData: any, promptText: string) => void;
  onUpdateProject: (project: Project) => void;
}

export const Canvas = ({ project, onBack, onAddSimulator, onConfigureSimulator, onRunRequest, onUpdateProject }: CanvasProps) => {
  const [nodes, setNodes] = useState<CanvasNode[]>([
    {
      id: 'sim-1',
      type: 'simulator',
      x: 400,
      y: 300,
      data: {
        ...project.simulators[0],
      },
    },
    {
      id: 'prompt-1',
      type: 'prompt',
      x: 100,
      y: 300,
      data: { prompt: '', status: 'idle' },
    },
  ]);

  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [draggedNodeId, setDraggedNodeId] = useState<string | null>(null);
  const [connectingSourceId, setConnectingSourceId] = useState<string | null>(null);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [editingTitle, setEditingTitle] = useState(false);
  const [editingDesc, setEditingDesc] = useState(false);
  const [tempTitle, setTempTitle] = useState(project.title);
  const [tempDesc, setTempDesc] = useState(project.desc);
  useEffect(() => {
    console.log('Edges updated', edges);
  }, [edges]);
  const canvasRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    
    // Check if clicking on canvas background or SVG
    if (target === canvasRef.current || target.closest('svg')) {
      setIsPanning(true);
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
      setSelectedNodeId(null);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    setMousePos({ x: e.clientX, y: e.clientY });

    if (isPanning) {
      setPan({ x: e.clientX - panStart.x, y: e.clientY - panStart.y });
    } else if (draggedNodeId && !connectingSourceId) {
      const dx = e.movementX;
      const dy = e.movementY;
      setNodes((prev) =>
        prev.map((n) => (n.id === draggedNodeId ? { ...n, x: n.x + dx, y: n.y + dy } : n))
      );
    }
  };

  const handleMouseUp = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    
    // If we're in connection mode and didn't hit a connection port, cancel connection
    if (connectingSourceId && !target.closest('.connection-port')) {
      setConnectingSourceId(null);
    }
    
    setIsPanning(false);
    setDraggedNodeId(null);
  };

  const handleNodeSelect = (id: string) => {
    setSelectedNodeId(id);
  };

  const updateNodeData = (id: string, data: Partial<CanvasNode['data']>) => {
    setNodes((prev) => prev.map((n) => (n.id === id ? { ...n, data: { ...n.data, ...data } } : n)));
  };

  const isPromptConnected = (promptId: string) => {
    return edges.some((e) => e.source === promptId);
  };

  const hasResultFeedback = (promptId: string) => {
    return edges.some((e) => e.target === promptId && nodes.find(n => n.id === e.source)?.type === 'result');
  };

  const handleConnectEnd = (targetId: string) => {
    if (!connectingSourceId || connectingSourceId === targetId) {
      setConnectingSourceId(null);
      return;
    }

    setEdges((prev) => {
      const edgeExists = prev.some(
        (e) => e.source === connectingSourceId && e.target === targetId
      );
      if (edgeExists) {
        console.log('Edge already exists, skipping', connectingSourceId, '->', targetId);
        return prev;
      }
      const newEdge = {
        id: `${connectingSourceId}-${targetId}`,
        source: connectingSourceId,
        target: targetId,
      };
      console.log('Adding edge', newEdge);
      return [...prev, newEdge];
    });

    setConnectingSourceId(null);
  };

  const handleRunNode = (promptId: string) => {
    const promptNode = nodes.find((n) => n.id === promptId);
    const connectedEdge = edges.find((e) => e.source === promptId);
    const simNode = connectedEdge ? nodes.find((n) => n.id === connectedEdge.target) : null;

    if (!promptNode || !simNode || !promptNode.data.prompt) return;

    // Save current prompt to history before running
    const currentPrompt = promptNode.data.prompt;
    const history = promptNode.data.promptHistory || [];
    if (currentPrompt.trim() && !history.includes(currentPrompt)) {
      updateNodeData(promptId, { 
        status: 'running',
        promptHistory: [...history, currentPrompt]
      });
    } else {
      updateNodeData(promptId, { status: 'running' });
    }

    setTimeout(() => {
      const mockResults = Array.from({ length: 20 }, (_, i) => ({
        x: i,
        y: Math.random() * 100 + 50 + Math.sin(i * 0.5) * 30,
      }));

      const resultId = `result-${Date.now()}`;
      const resultNode: CanvasNode = {
        id: resultId,
        type: 'result',
        x: simNode.x + 350,
        y: simNode.y,
        data: { results: mockResults },
      };

      setNodes((prev) => [...prev, resultNode]);
      setEdges((prev) => [...prev, { id: `${simNode.id}-${resultId}`, source: simNode.id, target: resultId }]);
      updateNodeData(promptId, { status: 'idle' });
      
      // Add recommendedParams to simulator after run
      updateNodeData(simNode.id, { 
        ...simNode.data,
        recommendedParams: { alpha: '0.3-0.7', beta: '5-15' },
      });
    }, 2000);
  };

  const handleDeleteNode = (nodeId: string) => {
    setNodes((prev) => prev.filter((n) => n.id !== nodeId));
    setEdges((prev) => prev.filter((e) => e.source !== nodeId && e.target !== nodeId));
    if (selectedNodeId === nodeId) setSelectedNodeId(null);
  };

  const handleDeleteEdge = (edgeId: string) => {
    setEdges((prev) => prev.filter((e) => e.id !== edgeId));
  };

  const handleSaveTitle = () => {
    if (tempTitle.trim() && tempTitle.length <= 50) {
      onUpdateProject({ ...project, title: tempTitle });
      setEditingTitle(false);
    }
  };

  const handleSaveDesc = () => {
    if (tempDesc.length <= 200) {
      onUpdateProject({ ...project, desc: tempDesc });
      setEditingDesc(false);
    }
  };

  const getEdgePath = (sourceId: string, targetId: string) => {
    const source = nodes.find((n) => n.id === sourceId);
    const target = nodes.find((n) => n.id === targetId);
    if (!source || !target) return '';
    
    // Calculate source port position (right side)
    const sx = source.x + (
      source.type === 'prompt' ? 320 : 
      source.type === 'simulator' ? 256 : 
      source.type === 'pdf' ? 320 : 
      384
    );
    const sy = source.y + (
      source.type === 'prompt' ? 80 : 
      source.type === 'simulator' ? 60 : 
      source.type === 'pdf' ? 80 : 
      60
    );
    
    // Calculate target port position (left side)
    const tx = target.x;
    const ty = target.y + (
      target.type === 'prompt' ? 80 : 
      target.type === 'simulator' ? 60 : 
      target.type === 'pdf' ? 80 : 
      60
    );
    
    const dist = Math.abs(tx - sx);
    
    return `M ${sx} ${sy} C ${sx + dist * 0.4} ${sy}, ${tx - dist * 0.4} ${ty}, ${tx} ${ty}`;
  };

  return (
    <div
      ref={canvasRef}
      className="absolute inset-0 overflow-auto cursor-crosshair"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <div
        className="absolute inset-0 pointer-events-none opacity-10"
        style={{
          backgroundImage: 'radial-gradient(rgba(255,255,255,0.5) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
          transform: `translate(${pan.x % 40}px, ${pan.y % 40}px)`,
        }}
      />
      
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none" style={{ transform: `translate(${pan.x}px, ${pan.y}px)` }}>
        <svg className="absolute inset-0 w-full h-full overflow-visible">
          <defs>
            <linearGradient id="edge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#8B5CF6" />
              <stop offset="100%" stopColor="#3B82F6" />
            </linearGradient>
          </defs>
          {edges.map((edge) => (
            <g key={edge.id}>
              <path
                d={getEdgePath(edge.source, edge.target)}
                stroke="url(#edge-gradient)"
                strokeWidth="2"
                fill="none"
                className="animate-pulse opacity-80 cursor-pointer hover:opacity-100"
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm('Delete this connection?')) {
                    handleDeleteEdge(edge.id);
                  }
                }}
              />
            </g>
          ))}
          {connectingSourceId && (() => {
            const source = nodes.find((n) => n.id === connectingSourceId);
            if (!source) return null;
            const sx = source.x + (
              source.type === 'prompt' ? 320 : 
              source.type === 'simulator' ? 256 : 
              source.type === 'pdf' ? 320 : 
              192
            );
            const sy = source.y + (
              source.type === 'prompt' ? 80 : 
              source.type === 'simulator' ? 60 : 
              source.type === 'pdf' ? 80 : 
              60
            );
            const tx = mousePos.x - pan.x;
            const ty = mousePos.y - pan.y;
            return (
              <path
                d={`M ${sx} ${sy} C ${sx + 100} ${sy}, ${tx - 100} ${ty}, ${tx} ${ty}`}
                stroke="#8B5CF6"
                strokeWidth="2"
                fill="none"
                strokeDasharray="5,5"
                className="opacity-50"
              />
            );
          })()}
        </svg>
        
        <div className="pointer-events-auto">
          {nodes.map((node) => (
            <div key={node.id}>
              {node.type === 'simulator' && (
                <SimulatorNode
                  node={node}
                  isSelected={selectedNodeId === node.id}
                  onSelect={handleNodeSelect}
                  onDragStart={(e, id) => {
                    if (!connectingSourceId) {
                      setDraggedNodeId(id);
                    }
                  }}
                  onConfigure={onConfigureSimulator}
                  onConnectEnd={handleConnectEnd}
                  onDelete={handleDeleteNode}
                />
              )}
              {node.type === 'prompt' && (
                <PromptNode
                  node={node}
                  isSelected={selectedNodeId === node.id}
                  onSelect={handleNodeSelect}
                  onDragStart={(e, id) => {
                    if (!connectingSourceId) {
                      setDraggedNodeId(id);
                    }
                  }}
                  onConnectStart={(id) => {
                    setConnectingSourceId(id);
                    setDraggedNodeId(null);
                  }}
                  onConnectEnd={handleConnectEnd}
                  updateData={updateNodeData}
                  isConnected={isPromptConnected(node.id)}
                  hasContent={!!node.data.prompt && node.data.prompt.trim().length > 0}
                  onRun={() => handleRunNode(node.id)}
                  hasFeedback={hasResultFeedback(node.id)}
                  onDelete={handleDeleteNode}
                />
              )}
              {node.type === 'result' && (
                <ResultNode
                  node={node}
                  isSelected={selectedNodeId === node.id}
                  onSelect={handleNodeSelect}
                  onDragStart={(e, id) => {
                    if (!connectingSourceId) {
                      setDraggedNodeId(id);
                    }
                  }}
                  onConnectStart={(id) => {
                    setConnectingSourceId(id);
                    setDraggedNodeId(null);
                  }}
                  onDelete={handleDeleteNode}
                />
              )}
              {node.type === 'pdf' && (
                <PDFNode
                  node={node}
                  isSelected={selectedNodeId === node.id}
                  onSelect={handleNodeSelect}
                  onDragStart={(e, id) => {
                    if (!connectingSourceId) {
                      setDraggedNodeId(id);
                    }
                  }}
                  onDelete={handleDeleteNode}
                  updateData={updateNodeData}
                  onConnectStart={(id) => {
                    setConnectingSourceId(id);
                    setDraggedNodeId(null);
                  }}
                  onConnectEnd={handleConnectEnd}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="absolute top-8 left-12 z-20 pointer-events-auto">
        <button
          onClick={onBack}
          className="flex items-center text-xs font-mono text-gray-500 hover:text-white mb-4 transition-colors"
        >
          <ChevronLeft className="w-3 h-3 mr-2" /> BACK TO GRID
        </button>
        
        {editingTitle ? (
          <div className="flex items-center gap-2 mb-2">
            <input
              type="text"
              value={tempTitle}
              onChange={(e) => setTempTitle(e.target.value)}
              maxLength={50}
              className="text-4xl font-bold tracking-tight bg-white/5 border border-white/20 rounded px-2 py-1"
              autoFocus
            />
            <button
              onClick={handleSaveTitle}
              className="p-2 bg-green-500/20 border border-green-500/40 rounded hover:bg-green-500/30 transition-colors"
            >
              <Check className="w-4 h-4 text-green-400" />
            </button>
            <button
              onClick={() => {
                setTempTitle(project.title);
                setEditingTitle(false);
              }}
              className="p-2 bg-red-500/20 border border-red-500/40 rounded hover:bg-red-500/30 transition-colors"
            >
              <X className="w-4 h-4 text-red-400" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2 mb-2 group">
            <h1 className="text-4xl font-bold tracking-tight">{project.title}</h1>
            <button
              onClick={() => setEditingTitle(true)}
              className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded transition-all"
            >
              <Edit2 className="w-4 h-4" />
            </button>
          </div>
        )}

        <div className="flex flex-col gap-2 items-start">
          <div className="flex flex-wrap gap-2">
            {project.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 bg-white/5 text-gray-400 text-[10px] rounded border border-white/10"
              >
                {tag}
              </span>
            ))}
          </div>
          
          {editingDesc ? (
            <div className="flex flex-col gap-2 w-1/2">
              <textarea
                value={tempDesc}
                onChange={(e) => setTempDesc(e.target.value)}
                maxLength={200}
                className="text-[10px] font-mono bg-white/5 border border-white/20 rounded p-2 resize-none h-32 w-full"
                autoFocus
              />
              <div className="flex items-center gap-2">
                <span className="text-[8px] text-gray-500">{tempDesc.length}/200</span>
                <button
                  onClick={handleSaveDesc}
                  className="px-2 py-1 bg-green-500/20 border border-green-500/40 rounded hover:bg-green-500/30 transition-colors text-[10px]"
                >
                  <Check className="w-3 h-3 text-green-400" />
                </button>
                <button
                  onClick={() => {
                    setTempDesc(project.desc);
                    setEditingDesc(false);
                  }}
                  className="px-2 py-1 bg-red-500/20 border border-red-500/40 rounded hover:bg-red-500/30 transition-colors text-[10px]"
                >
                  <X className="w-3 h-3 text-red-400" />
                </button>
              </div>
            </div>
          ) : (
            <div className="group flex items-start gap-2 max-w-md">
              <p className="text-[10px] text-gray-400 font-mono border-l-2 border-purple-500 pl-2 italic">
                {project.desc || 'AI_AGENT: Analyzing canvas topology for project description...'}
              </p>
              <button
                onClick={() => setEditingDesc(true)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded transition-all flex-shrink-0"
              >
                <Edit2 className="w-3 h-3" />
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="absolute top-32 right-12 z-20 pointer-events-auto group/actions">
        <div className="glass-panel p-3 rounded hover:bg-white/10 transition-all cursor-pointer">
          <Plus className="w-5 h-5 text-gray-400 group-hover/actions:text-white" />
        </div>
        
        <div className="absolute top-0 right-full mr-2 opacity-0 invisible group-hover/actions:opacity-100 group-hover/actions:visible transition-all flex flex-col gap-2">
          <button
            onClick={onAddSimulator}
            className="glass-panel p-3 rounded hover:bg-white/10 transition-colors flex items-center gap-2 whitespace-nowrap"
          >
            <UploadCloud className="w-4 h-4 text-gray-400" />
            <span className="text-[10px] font-mono uppercase">
              Upload Simulator
            </span>
          </button>
          <button 
            onClick={() => {
              const newPromptId = `prompt-${Date.now()}`;
              const newNode: CanvasNode = {
                id: newPromptId,
                type: 'prompt',
                x: 100,
                y: 300 + nodes.length * 50,
                data: { prompt: '', status: 'idle' },
              };
              setNodes((prev) => [...prev, newNode]);
            }}
            className="glass-panel p-3 rounded hover:bg-white/10 transition-colors flex items-center gap-2 whitespace-nowrap"
          >
            <Plus className="w-4 h-4 text-gray-400" />
            <span className="text-[10px] font-mono uppercase">
              New Prompt Node
            </span>
          </button>
          <button 
            onClick={() => {
              const newPDFId = `pdf-${Date.now()}`;
              const newNode: CanvasNode = {
                id: newPDFId,
                type: 'pdf',
                x: 100,
                y: 150 + nodes.length * 50,
                data: { pdfFileName: '' },
              };
              setNodes((prev) => [...prev, newNode]);
            }}
            className="glass-panel p-3 rounded hover:bg-white/10 transition-colors flex items-center gap-2 whitespace-nowrap"
          >
            <FileText className="w-4 h-4 text-orange-400" />
            <span className="text-[10px] font-mono uppercase">
              Add PDF Context
            </span>
          </button>
        </div>
      </div>

      <div className="absolute bottom-12 right-12 z-20 pointer-events-auto flex gap-4">
        <div className="glass-panel px-4 py-2 flex items-center gap-4 rounded-full">
          <span className="text-[10px] text-gray-500 font-mono uppercase">Controls</span>
          <div className="h-3 w-px bg-white/10"></div>
          <div className="flex gap-3 text-[10px] font-mono text-gray-400">
            <span className="flex items-center">
              <GripHorizontal className="w-3 h-3 mr-1" /> Pan
            </span>
            <span className="flex items-center">
              <MousePointer2 className="w-3 h-3 mr-1" /> Select
            </span>
            <span className="flex items-center">
              <LinkIcon className="w-3 h-3 mr-1" /> Drag to Connect
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
