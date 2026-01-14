import { Cpu } from 'lucide-react';

interface Model {
  id: string;
  name: string;
  description: string;
}

const models: Model[] = [
  {
    id: 'logistic',
    name: 'Logistic Regression',
    description: 'Fast linear classifier',
  },
  {
    id: 'naive_bayes',
    name: 'Naive Bayes',
    description: 'Probabilistic classifier',
  },
  {
    id: 'svm',
    name: 'Support Vector Machine',
    description: 'Powerful kernel-based classifier',
  },
];

interface ModelSelectorProps {
  selectedModel: string;
  onSelectModel: (model: string) => void;
}

export default function ModelSelector({
  selectedModel,
  onSelectModel,
}: ModelSelectorProps) {
  return (
    <div className="border-4 border-black p-6 bg-white">
      <div className="flex items-center gap-3 mb-4">
        <Cpu size={24} strokeWidth={3} />
        <h2 className="text-2xl font-black">SELECT MODEL</h2>
      </div>
      <div className="space-y-3">
        {models.map((model) => (
          <button
            key={model.id}
            onClick={() => onSelectModel(model.id)}
            className={`w-full text-left p-4 border-4 border-black font-bold transition-all ${
              selectedModel === model.id
                ? 'bg-yellow-300 translate-x-1 translate-y-1'
                : 'bg-white hover:bg-gray-100'
            }`}
          >
            <div className="text-lg font-black mb-1">{model.name}</div>
            <p className="text-sm">{model.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
