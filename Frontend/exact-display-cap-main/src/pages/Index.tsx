import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Hexagon, LayoutGrid, List } from 'lucide-react';
import { WireframeTerrain } from '@/components/WireframeTerrain';
import { MagneticButton } from '@/components/MagneticButton';
import { ProjectCard } from '@/components/ProjectCard';
import { Canvas } from '@/components/Canvas';
import { CreateResearchWizard } from '@/components/CreateResearchWizard';
import { SimulatorConfigModal } from '@/components/SimulatorConfigModal';
import type { Project, CanvasNode, Simulator } from '@/types';

const Index = () => {
  const [view, setView] = useState<'dashboard' | 'canvas' | 'wizard'>('dashboard');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [wizardMode, setWizardMode] = useState<'create' | 'addSimulator'>('create');
  const [projects, setProjects] = useState<Project[]>([
    {
      id: 'PRJ-01',
      title: 'Quantum Flux Dynamics',
      desc: 'Simulated particle interactions in high-energy quantum fields with advanced wave propagation modeling.',
      tags: ['Physics', 'Quantum'],
      createdAt: '2023-11-01',
      simulators: [
        {
          id: 's1',
          name: 'Solver_Alpha',
          desc: 'Core quantum solver',
          fileName: 'solver.py',
          params: [
            { id: 'p1', name: 'alpha', type: 'float', default: '0.5', desc: 'Wave coefficient' },
            { id: 'p2', name: 'beta', type: 'int', default: '10', desc: 'Iteration count' },
          ],
          outputs: [],
        },
      ],
    },
  ]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);
  const [editingSimulator, setEditingSimulator] = useState<Simulator | null>(null);

  useEffect(() => {
    if (view === 'canvas' && activeProject && !activeProject.desc) {
      const timer = setTimeout(() => {
        const aiDesc = `AI_GENERATED: Project configured with ${activeProject.simulators[0]?.name} kernel. Targeting optimized parameter space exploration for input vector [${activeProject.simulators[0]?.params.map((p) => p.name).join(', ')}].`;
        const updatedProject = { ...activeProject, desc: aiDesc };
        setActiveProject(updatedProject);
        setProjects((prev) => prev.map((p) => (p.id === updatedProject.id ? updatedProject : p)));
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [view, activeProject]);

  const handleCreateProject = ({ title, simulator }: { title: string; simulator: Simulator }) => {
    const newPrj: Project = {
      id: `PRJ-${Math.random().toString(36).substr(2, 4).toUpperCase()}`,
      title: title || 'Untitled',
      desc: '',
      simulators: [simulator],
      tags: [],
      createdAt: new Date().toISOString().split('T')[0],
    };
    setProjects([...projects, newPrj]);
    setActiveProject(newPrj);
    setView('canvas');
  };

  const handleAddSimulator = () => {
    setWizardMode('addSimulator');
    setView('wizard');
  };

  const handleRunRequest = (simData: any, promptText: string) => {
    console.log('Run triggered from canvas node:', simData, promptText);
  };

  const handleAddSimulatorToProject = (simulator: Simulator) => {
    if (!activeProject) return;
    const newSimulator = { ...simulator, id: `s${Date.now()}` };
    const updatedProject = {
      ...activeProject,
      simulators: [...activeProject.simulators, newSimulator],
    };
    setActiveProject(updatedProject);
    setProjects((prev) => prev.map((p) => (p.id === updatedProject.id ? updatedProject : p)));
    setView('canvas');
  };

  const handleSaveSimulatorConfig = (updatedSim: Simulator) => {
    if (!activeProject) return;
    const updatedProject = {
      ...activeProject,
      simulators: activeProject.simulators.map((s) => (s.id === updatedSim.id ? updatedSim : s)),
    };
    setActiveProject(updatedProject);
    setProjects((prev) => prev.map((p) => (p.id === updatedProject.id ? updatedProject : p)));
    setEditingSimulator(null);
  };

  const handleDeleteProject = (projectId: string) => {
    setProjects((prev) => prev.filter((p) => p.id !== projectId));
  };

  const handleUpdateProject = (updatedProject: Project) => {
    setActiveProject(updatedProject);
    setProjects((prev) => prev.map((p) => (p.id === updatedProject.id ? updatedProject : p)));
  };

  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-white selection:text-black overflow-hidden relative">
      <WireframeTerrain />

      {view === 'dashboard' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="relative z-10 min-h-screen p-12"
        >
          <header className="flex justify-between items-center mb-16">
            <div 
              className="flex items-center gap-3 cursor-pointer group" 
              onClick={() => setView('dashboard')}
            >
              <div className="w-8 h-8 border border-white/40 flex items-center justify-center group-hover:border-white transition-colors bg-black">
                <Hexagon className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold tracking-tight font-space-grotesk text-white mix-blend-difference">
                SIMFORGE
              </span>
            </div>

            <div className="flex gap-4 items-center">
              <div className="flex gap-2 bg-white/5 rounded-lg p-1 border border-white/10">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded transition-colors ${
                    viewMode === 'grid' ? 'bg-white/10 text-white' : 'text-gray-500 hover:text-white'
                  }`}
                >
                  <LayoutGrid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded transition-colors ${
                    viewMode === 'list' ? 'bg-white/10 text-white' : 'text-gray-500 hover:text-white'
                  }`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>

              <MagneticButton onClick={() => {
                setWizardMode('create');
                setView('wizard');
              }}>
                <Plus className="w-4 h-4 mr-2 inline" />
                New Research
              </MagneticButton>
            </div>
          </header>

          <div
            className={
              viewMode === 'grid'
                ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                : 'space-y-4'
            }
          >
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onOpen={() => {
                  setActiveProject(project);
                  setView('canvas');
                }}
                onDelete={() => handleDeleteProject(project.id)}
              />
            ))}
          </div>
        </motion.div>
      )}

      {view === 'canvas' && activeProject && (
        <Canvas
          project={activeProject}
          onBack={() => setView('dashboard')}
          onAddSimulator={handleAddSimulator}
          onConfigureSimulator={(node: CanvasNode) => {
            // Find simulator by matching the node data
            const sim = activeProject.simulators[0]; // For now, use first simulator
            if (sim) setEditingSimulator(sim);
          }}
          onRunRequest={handleRunRequest}
          onUpdateProject={handleUpdateProject}
        />
      )}

      <AnimatePresence>
        {view === 'wizard' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => {
              setView(wizardMode === 'create' ? 'dashboard' : 'canvas');
            }}
          >
            <div onClick={(e) => e.stopPropagation()}>
              <CreateResearchWizard 
                mode={wizardMode}
                onCancel={() => setView(wizardMode === 'create' ? 'dashboard' : 'canvas')} 
                onSave={wizardMode === 'create' ? handleCreateProject : (data: any) => handleAddSimulatorToProject(data.simulator)} 
              />
            </div>
          </motion.div>
        )}

        {editingSimulator && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => setEditingSimulator(null)}
          >
            <div onClick={(e) => e.stopPropagation()}>
              <SimulatorConfigModal
                simulator={editingSimulator}
                onCancel={() => setEditingSimulator(null)}
                onSave={handleSaveSimulatorConfig}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Index;
