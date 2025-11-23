import { FileText, MoreVertical, GripHorizontal, Sparkles } from 'lucide-react';
import type { CanvasNode } from '@/types';
import { useState } from 'react';

interface PDFNodeProps {
  node: CanvasNode;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onDragStart: (e: React.MouseEvent, id: string) => void;
  onDelete: (id: string) => void;
  updateData: (id: string, data: Partial<CanvasNode['data']>) => void;
  onConnectStart: (id: string) => void;
  onConnectEnd: (id: string) => void;
}

export const PDFNode = ({
  node,
  isSelected,
  onSelect,
  onDragStart,
  onDelete,
  updateData,
  onConnectStart,
  onConnectEnd,
}: PDFNodeProps) => {
  const [showMenu, setShowMenu] = useState(false);
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      updateData(node.id, { pdfFileName: file.name });
    }
  };

  return (
    <div
      className={`absolute cursor-move select-none ${
        isSelected ? 'ring-2 ring-purple-500' : ''
      }`}
      style={{ left: node.x, top: node.y }}
      onClick={(e) => {
        e.stopPropagation();
        onSelect(node.id);
      }}
    >
      <div className="glass-panel p-4 w-80 backdrop-blur-xl border border-white/20 rounded-lg shadow-lg hover:shadow-purple-500/20 transition-shadow">
        <div
          className="flex items-center justify-between mb-3 cursor-grab active:cursor-grabbing"
          onMouseDown={(e) => {
            e.stopPropagation();
            onDragStart(e, node.id);
          }}
        >
          <div className="flex items-center gap-2">
            <GripHorizontal className="w-4 h-4 text-gray-500" />
            <FileText className="w-4 h-4 text-orange-400" />
            <span className="text-xs font-mono text-gray-300 uppercase">PDF Context</span>
          </div>
          <div className="relative" onMouseLeave={() => setShowMenu(false)}>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowMenu(!showMenu);
              }}
              className="p-1 hover:bg-white/10 rounded transition-colors text-gray-400 hover:text-white"
            >
              <MoreVertical className="w-4 h-4" />
            </button>
            {showMenu && (
              <div className="absolute right-0 top-full mt-1 w-32 bg-gray-900 border border-white/20 rounded-lg shadow-xl z-50 overflow-hidden">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowMenu(false);
                    if (confirm('Delete this PDF node?')) {
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

        <div className="space-y-3">
          <div className="relative">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
              id={`pdf-upload-${node.id}`}
              onClick={(e) => e.stopPropagation()}
            />
            <label
              htmlFor={`pdf-upload-${node.id}`}
              className="flex items-center justify-center gap-2 p-4 border-2 border-dashed border-white/20 rounded cursor-pointer hover:border-orange-400/50 hover:bg-orange-400/5 transition-all"
              onClick={(e) => e.stopPropagation()}
            >
              <FileText className="w-5 h-5 text-orange-400" />
              <span className="text-xs text-gray-400">
                {node.data.pdfFileName || 'Upload PDF file'}
              </span>
            </label>
          </div>

          {node.data.pdfFileName && (
            <div className="p-3 bg-white/5 rounded border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4 text-orange-400" />
                <span className="text-xs text-gray-300 font-mono truncate flex-1">
                  {node.data.pdfFileName}
                </span>
                <div className="flex items-center gap-1 px-2 py-1 bg-purple-500/20 rounded border border-purple-500/40">
                  <Sparkles className="w-3 h-3 text-purple-400" />
                  <span className="text-[8px] text-purple-400 font-mono uppercase">Analyzed</span>
                </div>
              </div>
              <p className="text-[10px] text-gray-500 italic">
                Context loaded for AI assistance
              </p>
            </div>
          )}
        </div>

        <div className="flex justify-between items-center mt-4 pt-3 border-t border-white/10">
          <span className="text-[8px] text-gray-600 font-mono uppercase">
            Background Knowledge
          </span>
          <div 
            className="connection-port w-3 h-3 rounded-full bg-orange-500 border-2 border-white/20 hover:scale-125 transition-transform cursor-crosshair"
            onMouseDown={(e) => {
              e.stopPropagation();
              if (node.data.pdfFileName) {
                onConnectStart(node.id);
              }
            }}
            onMouseUp={(e) => {
              e.stopPropagation();
            }}
            title={node.data.pdfFileName ? "Connect to Research Intent" : "Upload PDF first"}
            style={{ opacity: node.data.pdfFileName ? 1 : 0.3 }}
          />
        </div>
      </div>
    </div>
  );
};
