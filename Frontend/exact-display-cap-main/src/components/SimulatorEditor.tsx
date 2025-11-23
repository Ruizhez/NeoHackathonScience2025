import { Settings, Activity, Trash2 } from 'lucide-react';
import type { Parameter, OutputMetric } from '@/types';

interface SimulatorEditorProps {
  params: Parameter[];
  outputs: OutputMetric[];
  onAddParam: () => void;
  onAddOutput: () => void;
  onRemoveParam: (id: string) => void;
  onRemoveOutput: (id: string) => void;
  onParamChange: (id: string, field: string, value: string) => void;
  onOutputChange: (id: string, field: string, value: string) => void;
}

export const SimulatorEditor = ({
  params,
  outputs,
  onAddParam,
  onAddOutput,
  onRemoveParam,
  onRemoveOutput,
  onParamChange,
  onOutputChange,
}: SimulatorEditorProps) => {
  return (
    <div className="space-y-8">
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-mono text-sm text-blue-400 uppercase flex items-center gap-2">
            <Settings className="w-3 h-3" /> Input Parameters
          </h3>
          <button
            onClick={onAddParam}
            className="text-[10px] border border-white/20 px-2 py-1 hover:bg-white/10"
          >
            + ADD PARAM
          </button>
        </div>
        <div className="space-y-2">
          {params.map((p, idx) => (
            <div
              key={p.id}
              className="grid grid-cols-12 gap-2 bg-white/5 p-2 rounded border border-white/10 items-center"
            >
              <div className="col-span-1 text-gray-500 font-mono text-[10px] text-center">
                #{idx + 1}
              </div>
              <input
                value={p.name}
                onChange={(e) => onParamChange(p.id, 'name', e.target.value)}
                placeholder="Name"
                className="col-span-2 glass-input p-1 text-[10px]"
              />
              <input
                value={p.desc}
                onChange={(e) => onParamChange(p.id, 'desc', e.target.value)}
                placeholder="Description"
                className="col-span-3 glass-input p-1 text-[10px]"
              />
              <select
                value={p.type}
                onChange={(e) => onParamChange(p.id, 'type', e.target.value)}
                className="col-span-2 glass-input p-1 text-[10px]"
              >
                <option value="float">Float</option>
                <option value="int">Int</option>
                <option value="string">Str</option>
              </select>
              <input
                value={p.default}
                onChange={(e) => onParamChange(p.id, 'default', e.target.value)}
                placeholder="Default"
                className="col-span-2 glass-input p-1 text-[10px]"
              />
              <input
                value={p.range || ''}
                onChange={(e) => onParamChange(p.id, 'range', e.target.value)}
                placeholder="Range"
                className="col-span-1 glass-input p-1 text-[10px]"
              />
              <button
                onClick={() => onRemoveParam(p.id)}
                className="col-span-1 text-red-500 hover:bg-red-500/20 p-1 rounded flex justify-center"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-mono text-sm text-green-400 uppercase flex items-center gap-2">
            <Activity className="w-3 h-3" /> Output Metrics
          </h3>
          <button
            onClick={onAddOutput}
            className="text-[10px] border border-white/20 px-2 py-1 hover:bg-white/10"
          >
            + ADD METRIC
          </button>
        </div>
        <div className="space-y-2">
          {outputs.map((o, idx) => (
            <div
              key={o.id}
              className="grid grid-cols-12 gap-2 bg-white/5 p-2 rounded border border-white/10 items-center"
            >
              <div className="col-span-1 text-gray-500 font-mono text-[10px] text-center">
                #{idx + 1}
              </div>
              <input
                value={o.name}
                onChange={(e) => onOutputChange(o.id, 'name', e.target.value)}
                placeholder="Metric Name"
                className="col-span-3 glass-input p-1 text-[10px]"
              />
              <input
                value={o.desc}
                onChange={(e) => onOutputChange(o.id, 'desc', e.target.value)}
                placeholder="Description"
                className="col-span-5 glass-input p-1 text-[10px]"
              />
              <input
                value={o.unit}
                onChange={(e) => onOutputChange(o.id, 'unit', e.target.value)}
                placeholder="Unit"
                className="col-span-2 glass-input p-1 text-[10px]"
              />
              <button
                onClick={() => onRemoveOutput(o.id)}
                className="col-span-1 text-red-500 hover:bg-red-500/20 p-1 rounded flex justify-center"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
