import { useState } from 'react';
import { Hexagon, ChevronRight, UploadCloud, ArrowLeft } from 'lucide-react';
import { MagneticButton } from './MagneticButton';
import { SimulatorEditor } from './SimulatorEditor';
import type { Parameter, OutputMetric } from '@/types';

interface CreateResearchWizardProps {
  mode?: 'create' | 'addSimulator';
  onCancel: () => void;
  onSave: (data: { title: string; simulator: any } | { simulator: any }) => void;
}

export const CreateResearchWizard = ({
  mode = 'create',
  onCancel,
  onSave
}: CreateResearchWizardProps) => {
  const [step, setStep] = useState(1);
  const [projectTitle, setProjectTitle] = useState('Untitled');
  const [file, setFile] = useState<{ name: string } | null>(null);
  const [simMeta, setSimMeta] = useState({ name: '', desc: '' });
  const [params, setParams] = useState<Parameter[]>([{
    id: '1',
    name: '',
    desc: '',
    type: 'float',
    default: '',
    range: ''
  }]);
  const [outputs, setOutputs] = useState<OutputMetric[]>([{
    id: '1',
    name: '',
    desc: '',
    unit: ''
  }]);

  const addParam = () => setParams([...params, {
    id: Date.now().toString(),
    name: '',
    desc: '',
    type: 'float',
    default: '',
    range: ''
  }]);

  const addOutput = () => setOutputs([...outputs, {
    id: Date.now().toString(),
    name: '',
    desc: '',
    unit: ''
  }]);

  const removeParam = (id: string) => setParams(params.filter(p => p.id !== id));
  const removeOutput = (id: string) => setOutputs(outputs.filter(o => o.id !== id));

  const handleParamChange = (id: string, field: string, value: string) => 
    setParams(params.map(p => p.id === id ? { ...p, [field]: value } : p));

  const handleOutputChange = (id: string, field: string, value: string) => 
    setOutputs(outputs.map(o => o.id === id ? { ...o, [field]: value } : o));

  const handleFinish = () => {
    const simulator = {
      ...simMeta,
      fileName: file?.name || 'unknown.py',
      params,
      outputs,
      id: Date.now().toString()
    };
    
    if (mode === 'addSimulator') {
      onSave({ simulator });
    } else {
      onSave({ title: projectTitle, simulator });
    }
  };

  return (
    <div className="glass-panel p-8 max-w-6xl w-full h-[85vh] flex flex-col animate-in fade-in zoom-in-95 duration-300 mt-20 relative z-50">
      <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <Hexagon className="w-5 h-5 text-white" />
          <h2 className="text-xl font-bold font-mono uppercase tracking-widest mx-0">
            {mode === 'addSimulator' ? 'ADD SIMULATOR' : 'NEW PROJECT'}
          </h2>
        </div>
        <div className="flex gap-2 items-center">
          <span className={`text-[10px] font-mono ${step === 1 ? 'text-blue-400' : 'text-gray-600'}`}>
            STEP 1: SETUP
          </span>
          <ChevronRight className="w-3 h-3 text-gray-700" />
          <span className={`text-[10px] font-mono ${step === 2 ? 'text-blue-400' : 'text-gray-600'}`}>
            STEP 2: KERNEL CONFIG
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scroll min-h-0">
        {step === 1 && (
          <div className="space-y-8">{mode === 'create' && (
              <div className="group">
                <label className="block text-sm font-mono text-gray-500 uppercase tracking-widest mb-2">
                  Project Designation
                </label>
                <input 
                  value={projectTitle} 
                  onChange={e => setProjectTitle(e.target.value)} 
                  className="w-full glass-input p-4 text-xl font-mono placeholder:text-gray-700" 
                  placeholder="Untitled" 
                  autoFocus 
                />
              </div>
            )}
            
            <div 
              className="border-2 border-dashed border-white/20 rounded-xl p-12 flex flex-col items-center justify-center hover:border-blue-500/50 hover:bg-blue-500/5 transition-all cursor-pointer" 
              onClick={() => setFile({ name: 'solver_core.py' })}
            >
              <UploadCloud className={`w-12 h-12 mb-4 ${file ? 'text-green-400' : 'text-gray-500'}`} />
              {file ? (
                <span className="font-mono text-green-400">{file.name} UPLOADED</span>
              ) : (
                <span className="font-mono text-gray-500 text-xs">
                  Drop simulation code here • Python/Jupyter • Max 20MB
                </span>
              )}
            </div>
            
            <div className={`grid grid-cols-2 gap-4 transition-opacity duration-300 ${file ? 'opacity-100' : 'opacity-40 pointer-events-none'}`}>
              <div className="group">
                <label className="block text-sm font-mono text-gray-500 uppercase mb-2">
                  Simulator Name
                </label>
                <input 
                  value={simMeta.name} 
                  onChange={e => setSimMeta({ ...simMeta, name: e.target.value })} 
                  className="w-full glass-input p-2 font-mono text-sm" 
                  placeholder="e.g., FLUID_DYNAMICS"
                  disabled={!file}
                />
              </div>
              <div className="group">
                <label className="block font-mono text-gray-500 uppercase mb-2 text-sm">
                  Description
                </label>
                <input 
                  value={simMeta.desc} 
                  onChange={e => setSimMeta({ ...simMeta, desc: e.target.value })} 
                  className="w-full glass-input p-2 font-mono text-sm" 
                  placeholder="Functionality summary..."
                  disabled={!file}
                />
              </div>
            </div>
          </div>
        )}
        
        {step === 2 && (
          <SimulatorEditor 
            params={params} 
            outputs={outputs} 
            onAddParam={addParam} 
            onAddOutput={addOutput} 
            onRemoveParam={removeParam} 
            onRemoveOutput={removeOutput} 
            onParamChange={handleParamChange} 
            onOutputChange={handleOutputChange} 
          />
        )}
      </div>
      
      <div className="pt-6 mt-6 border-t border-white/10 flex justify-between items-center flex-shrink-0">
        <button 
          onClick={step === 1 ? onCancel : () => setStep(1)} 
          className="flex items-center gap-2 text-gray-400 hover:text-white font-mono text-sm transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          {step === 1 ? 'Cancel' : 'Back'}
        </button>
        
        {step === 1 ? (
          <MagneticButton onClick={() => setStep(2)} disabled={!file}>
            Next: Configure
          </MagneticButton>
        ) : (
          <MagneticButton onClick={handleFinish}>
            {mode === 'addSimulator' ? 'Add Simulator' : 'Initialize Project'}
          </MagneticButton>
        )}
      </div>
    </div>
  );
};
