import { Play, Loader2 } from 'lucide-react';

interface ExperimentButtonProps {
  onRunExperiment: () => void;
  isLoading: boolean;
}

export default function ExperimentButton({
  onRunExperiment,
  isLoading,
}: ExperimentButtonProps) {
  return (
    <button
      onClick={onRunExperiment}
      disabled={isLoading}
      className="w-full border-4 border-black bg-yellow-300 p-8 font-black text-2xl hover:bg-yellow-400 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all hover:translate-x-1 hover:translate-y-1 active:translate-x-0 active:translate-y-0"
    >
      <div className="flex items-center justify-center gap-4">
        {isLoading ? (
          <>
            <Loader2 size={32} strokeWidth={3} className="animate-spin" />
            <span>RUNNING EXPERIMENT...</span>
          </>
        ) : (
          <>
            <Play size={32} strokeWidth={3} fill="currentColor" />
            <span>RUN EXPERIMENT</span>
          </>
        )}
      </div>
    </button>
  );
}
