import { useState } from 'react';
import { X } from 'lucide-react';
import { MagneticButton } from './MagneticButton';
import { SimulatorEditor } from './SimulatorEditor';
import type { Simulator } from '@/types';

interface SimulatorConfigModalProps {
  simulator: Simulator;
  onCancel: () => void;
  onSave: (simulator: Simulator) => void;
}

export const SimulatorConfigModal = ({ simulator, onCancel, onSave }: SimulatorConfigModalProps) => {
  const [params, setParams] = useState([...simulator.params]);
  const [outputs, setOutputs] = useState([...simulator.outputs]);

  const addParam = () =>
    setParams([...params, { id: Date.now().toString(), name: '', desc: '', type: 'float', default: '', range: '' }]);
  const addOutput = () =>
    setOutputs([...outputs, { id: Date.now().toString(), name: '', desc: '', unit: '' }]);
  const removeParam = (id: string) => setParams(params.filter((p) => p.id !== id));
  const removeOutput = (id: string) => setOutputs(outputs.filter((o) => o.id !== id));
  const handleParamChange = (id: string, field: string, value: string) =>
    setParams(params.map((p) => (p.id === id ? { ...p, [field]: value } : p)));
  const handleOutputChange = (id: string, field: string, value: string) =>
    setOutputs(outputs.map((o) => (o.id === id ? { ...o, [field]: value } : o)));

  return (
    <div className="glass-panel p-8 max-w-4xl mx-auto h-[80vh] flex flex-col animate-in fade-in zoom-in-95 duration-300 mt-20 relative z-50">
      <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-6">
        <h2 className="text-xl font-bold font-mono uppercase tracking-widest">
          Configure Kernel: {simulator.name}
        </h2>
        <button onClick={onCancel}>
          <X className="w-5 h-5 text-gray-500 hover:text-white" />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto pr-2 custom-scroll">
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
      </div>
      
      <div className="pt-6 mt-6 border-t border-white/10 flex justify-end">
        <MagneticButton onClick={() => onSave({ ...simulator, params, outputs })}>
          Save Configuration
        </MagneticButton>
      </div>
    </div>
  );
};
