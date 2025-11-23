import { motion } from 'framer-motion';
import { Clock, Layers, MoreVertical } from 'lucide-react';
import type { Project } from '@/types';
import { useState } from 'react';

interface ProjectCardProps {
  project: Project;
  onOpen: () => void;
  onDelete: () => void;
}

export const ProjectCard = ({ project, onOpen, onDelete }: ProjectCardProps) => {
  const [showMenu, setShowMenu] = useState(false);
  
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      className="glass-panel-hover rounded-xl p-6 cursor-pointer group"
      onClick={onOpen}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold mb-2 tracking-tight">{project.title}</h3>
          <p className="text-[10px] text-gray-500 font-mono flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {project.createdAt}
          </p>
        </div>
        <div className="relative" onMouseLeave={() => setShowMenu(false)}>
          <button 
            onClick={(e) => {
              e.stopPropagation();
              setShowMenu(!showMenu);
            }}
            className="p-2 rounded border border-white/10 hover:bg-white/10 transition-colors text-gray-400 hover:text-white"
          >
            <MoreVertical className="w-4 h-4" />
          </button>
          {showMenu && (
            <div className="absolute right-0 top-full mt-1 w-32 bg-gray-900 border border-white/20 rounded-lg shadow-xl z-50 overflow-hidden">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setShowMenu(false);
                  onDelete();
                }}
                className="w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-red-500/20 transition-colors flex items-center gap-2"
              >
                Delete
              </button>
            </div>
          )}
        </div>
      </div>
      
      <p className="text-sm text-gray-400 mb-4 line-clamp-2">{project.desc}</p>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {project.tags.map((tag) => (
          <span
            key={tag}
            className="px-2 py-0.5 bg-white/5 text-gray-400 text-[10px] rounded border border-white/10"
          >
            {tag}
          </span>
        ))}
      </div>
      
      <div className="flex items-center gap-2 text-[10px] font-mono text-gray-500">
        <Layers className="w-3 h-3" />
        {project.simulators.length} Simulator{project.simulators.length !== 1 ? 's' : ''}
      </div>
    </motion.div>
  );
};
