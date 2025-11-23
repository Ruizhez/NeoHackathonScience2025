import { BrainCircuit, Play, MoreVertical, History } from 'lucide-react';
import type { CanvasNode } from '@/types';
import { useState } from 'react';

interface PromptNodeProps {
  node: CanvasNode;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onDragStart: (e: React.MouseEvent, id: string) => void;
  onConnectStart: (id: string) => void;
  onConnectEnd: (id: string) => void;
  updateData: (id: string, data: Partial<CanvasNode['data']>) => void;
  isConnected: boolean;
  hasContent: boolean;
  onRun: () => void;
  hasFeedback: boolean;
  onDelete: (id: string) => void;
}

export const PromptNode = ({
  node,
  isSelected,
  onSelect,
  onDragStart,
  onConnectStart,
  onConnectEnd,
  updateData,
  isConnected,
  hasContent,
  onRun,
  hasFeedback,
  onDelete,
}: PromptNodeProps) => {
  const [showMenu, setShowMenu] = useState(false);
  
  return (
    <div
      className={`absolute node-panel w-80 rounded-xl overflow-visible cursor-grab active:cursor-grabbing group ${
        isSelected ? 'selected' : ''
      }`}
      style={{ left: node.x, top: node.y }}
      onMouseDown={(e) => {
        const target = e.target as HTMLElement;
        // Don't start dragging if clicking on port, button or textarea
        if (target.closest('.connection-port') || target.closest('button') || target.tagName === 'TEXTAREA') {
          return;
        }
        e.stopPropagation();
        onSelect(node.id);
        onDragStart(e, node.id);
      }}
    >
      <div className="bg-gradient-to-r from-purple-900/40 to-transparent p-3 border-b border-white/10 flex justify-between items-center rounded-t-xl">
        <div className="flex items-center gap-2">
          <div className="p-1 bg-purple-500/20 rounded border border-purple-500/30">
            <BrainCircuit className="w-3 h-3 text-purple-400" />
          </div>
          <span className="text-xs font-bold font-mono uppercase text-purple-100">
            AI Assistant
          </span>
        </div>

        <div className="flex gap-2">
          <button
            disabled={!isConnected || !hasContent || node.data.status === 'running'}
            onClick={(e) => {
              e.stopPropagation();
              onRun();
            }}
            className={`text-[10px] px-3 py-1 rounded font-mono font-bold flex items-center gap-1 transition-all border ${
              isConnected && hasContent
                ? 'bg-green-500/20 text-green-400 border-green-500/50 hover:bg-green-500/30 cursor-pointer shadow-[0_0_10px_rgba(16,185,129,0.3)]'
                : 'bg-gray-800 text-gray-600 border-gray-700 cursor-not-allowed'
            }`}
          >
            <Play className="w-3 h-3" />
            {node.data.status === 'running' ? 'RUNNING' : 'RUN'}
          </button>
          <div className="relative" onMouseLeave={() => setShowMenu(false)}>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowMenu(!showMenu);
              }}
              className="p-1.5 rounded border border-white/10 hover:bg-white/10 transition-all text-gray-400 hover:text-white"
            >
              <MoreVertical className="w-3 h-3" />
            </button>
            {showMenu && (
              <div className="absolute right-0 top-full mt-1 w-32 bg-gray-900 border border-white/20 rounded-lg shadow-xl z-50 overflow-hidden">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowMenu(false);
                    if (confirm('Delete this prompt node?')) {
                      onDelete(node.id);
                    }
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-red-500/20 transition-colors flex items-center gap-2"
                >
                  Delete
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="p-4">
        <textarea
          value={node.data.prompt || ''}
          onChange={(e) => updateData(node.id, { prompt: e.target.value })}
          onMouseDown={(e) => e.stopPropagation()}
          placeholder="Describe research objective..."
          className="w-full h-32 glass-input p-3 text-sm rounded resize-none focus:ring-1 focus:ring-purple-500"
        />
        
        {/* History Section */}
        {node.data.promptHistory && node.data.promptHistory.length > 0 && (
          <div className="mt-3 p-3 bg-gray-900/40 rounded border border-gray-700/50">
            <div className="flex items-center gap-2 mb-2">
              <History className="w-3 h-3 text-gray-400" />
              <span className="text-[10px] font-mono text-gray-400 uppercase">History</span>
            </div>
            <div className="space-y-2 max-h-32 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-800">
              {node.data.promptHistory.map((historicalPrompt, index) => (
                <div 
                  key={index}
                  className="p-2 bg-gray-800/50 rounded text-[11px] text-gray-300 font-mono cursor-pointer hover:bg-gray-800 transition-all"
                  onClick={(e) => {
                    e.stopPropagation();
                    updateData(node.id, { prompt: historicalPrompt });
                  }}
                  title="Click to restore this prompt"
                >
                  {historicalPrompt.length > 100 ? `${historicalPrompt.substring(0, 100)}...` : historicalPrompt}
                </div>
              ))}
            </div>
          </div>
        )}
        
        {!isConnected && (
          <p className="mt-2 text-[10px] text-gray-500 font-mono">
            → Connect to simulator to enable execution
          </p>
        )}
        {isConnected && !hasContent && (
          <p className="mt-2 text-[10px] text-yellow-500 font-mono">
            → Add research intent to enable run
          </p>
        )}
        {hasFeedback && (
          <p className="mt-2 text-[10px] text-green-500 font-mono flex items-center gap-1">
            ✓ Result feedback connected - refine prompt to iterate
          </p>
        )}
      </div>

      {/* Input Port - for result feedback */}
      <div
        className="connection-port absolute top-1/2 -left-1.5 w-4 h-4 bg-gray-900 border-2 border-green-500/50 rounded-full hover:border-green-500 hover:scale-125 hover:bg-green-500/20 transition-all cursor-crosshair z-30"
        onMouseUp={(e) => {
          e.stopPropagation();
          e.preventDefault();
          onConnectEnd(node.id);
        }}
        onMouseDown={(e) => {
          e.stopPropagation();
          e.preventDefault();
        }}
      ></div>

      {/* Output Port - Connection Source */}
      <div
        className="connection-port absolute top-1/2 -right-1.5 w-4 h-4 bg-purple-900 border-2 border-purple-500 rounded-full hover:scale-125 hover:shadow-lg hover:shadow-purple-500/50 transition-all cursor-crosshair z-30"
        onMouseDown={(e) => {
          e.stopPropagation();
          e.preventDefault();
          console.log('Output port mouseDown, calling onConnectStart');
          onConnectStart(node.id);
        }}
      ></div>
    </div>
  );
};
