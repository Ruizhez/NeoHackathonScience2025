import { motion } from 'framer-motion';
import { Cpu, FileCode, Settings, Sparkles, MoreVertical } from 'lucide-react';
import type { CanvasNode } from '@/types';
import { useState } from 'react';

interface SimulatorNodeProps {
  node: CanvasNode;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onDragStart: (e: React.MouseEvent, id: string) => void;
  onConfigure: (node: CanvasNode) => void;
  onConnectEnd: (id: string) => void;
  onDelete: (id: string) => void;
}

export const SimulatorNode = ({
  node,
  isSelected,
  onSelect,
  onDragStart,
  onConfigure,
  onConnectEnd,
  onDelete,
}: SimulatorNodeProps) => {
  const recommendedParams = node.data.recommendedParams;
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div
      className={`absolute node-panel w-64 rounded-xl overflow-visible cursor-grab active:cursor-grabbing group ${
        isSelected ? 'selected' : ''
      }`}
      style={{ left: node.x, top: node.y }}
      onMouseDown={(e) => {
        const target = e.target as HTMLElement;
        // Don't start dragging if clicking on port or button
        if (target.closest('.connection-port') || target.closest('button')) {
          return;
        }
        e.stopPropagation();
        onSelect(node.id);
        onDragStart(e, node.id);
      }}
    >
      {recommendedParams && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute -top-20 left-0 right-0 bg-purple-900/90 backdrop-blur-md border border-purple-500/50 rounded-lg p-2 shadow-xl z-10"
        >
          <div className="flex items-center gap-2 text-[10px] text-purple-300 font-bold mb-1 uppercase">
            <Sparkles className="w-3 h-3" /> AI Scan Ranges
          </div>
          <div className="text-[10px] font-mono text-white space-y-1">
            {Object.entries(recommendedParams).map(([key, val]) => (
              <div key={key} className="flex justify-between">
                <span className="opacity-70">{key}:</span>
                <span className="text-purple-200">{val}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <div className="bg-white/5 p-3 border-b border-white/10 flex justify-between items-center rounded-t-xl">
        <div className="flex items-center gap-2">
          <div className="p-1 bg-blue-500/20 rounded border border-blue-500/30">
            <Cpu className="w-3 h-3 text-blue-400" />
          </div>
          <span className="text-xs font-bold font-mono uppercase text-blue-100">
            simulator
          </span>
        </div>
        <div className="flex gap-2">
          <button
            className="text-gray-400 hover:text-white p-1 hover:bg-white/10 rounded transition-colors"
            onMouseDown={(e) => {
              e.stopPropagation();
              onConfigure(node);
            }}
          >
            <Settings className="w-3 h-3" />
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
                    if (confirm('Delete this simulator node?')) {
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
      
      <div className="p-4 bg-transparent">
        <div className="font-bold text-sm mb-1 text-white">{node.data.name}</div>
        <div className="text-[10px] text-gray-500 font-mono mb-3 flex items-center gap-1">
          <FileCode className="w-3 h-3" />
          {node.data.fileName}
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="px-2 py-0.5 bg-white/5 text-gray-400 text-[10px] rounded border border-white/10">
            {node.data.params?.length || 0} Params
          </span>
          <span className="px-2 py-0.5 bg-white/5 text-gray-400 text-[10px] rounded border border-white/10">
            {node.data.outputs?.length || 0} Metrics
          </span>
        </div>
      </div>
      
      {/* Output Port */}
      <div className="connection-port absolute top-1/2 -right-1.5 w-3 h-3 bg-gray-900 border border-gray-500 rounded-full hover:border-green-500 transition-colors z-30"></div>
      
      {/* Input Port - Connection Target */}
      <div 
        className="connection-port absolute top-1/2 -left-1.5 w-4 h-4 bg-gray-900 border-2 border-blue-500/50 rounded-full hover:border-blue-500 hover:scale-125 hover:bg-blue-500/20 transition-all cursor-crosshair z-30"
        onMouseUp={(e) => {
          e.stopPropagation();
          e.preventDefault();
          console.log('Input port mouseUp, calling onConnectEnd');
          onConnectEnd(node.id);
        }}
        onMouseDown={(e) => {
          e.stopPropagation();
          e.preventDefault();
        }}
      ></div>
    </div>
  );
};
