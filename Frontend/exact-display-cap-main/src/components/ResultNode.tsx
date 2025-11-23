import { Activity, Download, FileJson, Copy, MoreVertical } from 'lucide-react';
import type { CanvasNode } from '@/types';
import { useState } from 'react';

interface ResultNodeProps {
  node: CanvasNode;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onDragStart: (e: React.MouseEvent, id: string) => void;
  onConnectStart: (id: string) => void;
  onDelete: (id: string) => void;
}

export const ResultNode = ({
  node,
  isSelected,
  onSelect,
  onDragStart,
  onConnectStart,
  onDelete,
}: ResultNodeProps) => {
  const [showMenu, setShowMenu] = useState(false);
  
  return (
    <div
      className={`absolute node-panel w-96 rounded-xl overflow-visible cursor-grab active:cursor-grabbing group ${
        isSelected ? 'selected' : ''
      }`}
      style={{ left: node.x, top: node.y }}
      onMouseDown={(e) => {
        e.stopPropagation();
        onSelect(node.id);
        onDragStart(e, node.id);
      }}
    >
      <div className="bg-gradient-to-r from-green-900/40 to-transparent p-3 border-b border-white/10 flex justify-between items-center rounded-t-xl">
        <div className="flex items-center gap-2">
          <div className="p-1 bg-green-500/20 rounded border border-green-500/30">
            <Activity className="w-3 h-3 text-green-400" />
          </div>
          <span className="text-xs font-bold font-mono uppercase text-green-100">
            output result
          </span>
        </div>
        <div className="flex gap-2">
          <button className="text-gray-400 hover:text-white p-1 hover:bg-white/10 rounded transition-colors">
            <FileJson className="w-3 h-3" />
          </button>
          <button className="text-gray-400 hover:text-white p-1 hover:bg-white/10 rounded transition-colors">
            <Download className="w-3 h-3" />
          </button>
          <div className="relative" onMouseLeave={() => setShowMenu(false)}>
            <button 
              onClick={(e) => {
                e.stopPropagation();
                setShowMenu(!showMenu);
              }}
              className="text-gray-400 hover:text-white p-1 hover:bg-white/10 rounded transition-colors"
            >
              <MoreVertical className="w-3 h-3" />
            </button>
            {showMenu && (
              <div className="absolute right-0 top-full mt-1 w-32 bg-gray-900 border border-white/20 rounded-lg shadow-xl z-50 overflow-hidden">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowMenu(false);
                    if (confirm('Delete this result node?')) {
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
        {node.data.results && (node.data.results.runs?.length > 0 || Array.isArray(node.data.results)) ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] text-gray-400 font-mono uppercase">JSON Output</span>
              <button
                className="text-gray-400 hover:text-white p-1 hover:bg-white/10 rounded transition-colors"
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(node.data.results, null, 2));
                }}
              >
                <Copy className="w-3 h-3" />
              </button>
            </div>
            <pre className="bg-black/40 border border-white/10 rounded p-3 text-[10px] font-mono text-green-400 overflow-auto max-h-64 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
              {JSON.stringify(node.data.results, null, 2)}
            </pre>
            <div className="grid grid-cols-3 gap-2">
              <div className="bg-white/5 p-2 rounded border border-white/10">
                <div className="text-[10px] text-gray-500 uppercase font-mono mb-1">Records</div>
                <div className="text-sm font-bold">
                  {node.data.results.runs?.length || (Array.isArray(node.data.results) ? node.data.results.length : 1)}
                </div>
              </div>
              <div className="bg-white/5 p-2 rounded border border-white/10">
                <div className="text-[10px] text-gray-500 uppercase font-mono mb-1">Size</div>
                <div className="text-sm font-bold">
                  {(JSON.stringify(node.data.results).length / 1024).toFixed(1)} KB
                </div>
              </div>
              <div className="bg-white/5 p-2 rounded border border-white/10">
                <div className="text-[10px] text-gray-500 uppercase font-mono mb-1">Type</div>
                <div className="text-sm font-bold">JSON</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500 text-sm font-mono">
            Awaiting simulation results...
          </div>
        )}
      </div>

      {/* Input Port (left side) - receives from simulator */}
      <div className="connection-port absolute top-1/2 -left-1.5 w-3 h-3 bg-gray-900 border border-gray-500 rounded-full hover:border-green-500 transition-colors z-30"></div>

      {/* Output Port (right side) - for feedback to prompt */}
      <div
        className="connection-port absolute top-1/2 -right-1.5 w-4 h-4 bg-green-900 border-2 border-green-500 rounded-full hover:scale-125 hover:shadow-lg hover:shadow-green-500/50 transition-all cursor-crosshair z-30"
        onMouseDown={(e) => {
          e.stopPropagation();
          e.preventDefault();
          onConnectStart(node.id);
        }}
      ></div>
    </div>
  );
};
