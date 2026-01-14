import { Database } from 'lucide-react';

interface Dataset {
  id: string;
  name: string;
  description: string;
  samples: number;
}

const datasets: Dataset[] = [
  {
    id: 'imdb',
    name: 'IMDb Movie Reviews',
    description: 'Binary sentiment classification (positive/negative)',
    samples: 2000,
  },
  {
    id: 'news',
    name: 'News Category Dataset',
    description: 'Multi-class news article classification',
    samples: 2000,
  },
];

interface DatasetSelectorProps {
  selectedDataset: string;
  onSelectDataset: (dataset: string) => void;
}

export default function DatasetSelector({
  selectedDataset,
  onSelectDataset,
}: DatasetSelectorProps) {
  return (
    <div className="border-4 border-black p-6 bg-white">
      <div className="flex items-center gap-3 mb-4">
        <Database size={24} strokeWidth={3} />
        <h2 className="text-2xl font-black">SELECT DATASET</h2>
      </div>
      <div className="space-y-3">
        {datasets.map((dataset) => (
          <button
            key={dataset.id}
            onClick={() => onSelectDataset(dataset.id)}
            className={`w-full text-left p-4 border-4 border-black font-bold transition-all ${
              selectedDataset === dataset.id
                ? 'bg-yellow-300 translate-x-1 translate-y-1'
                : 'bg-white hover:bg-gray-100'
            }`}
          >
            <div className="flex justify-between items-start mb-1">
              <span className="text-lg font-black">{dataset.name}</span>
              <span className="text-sm bg-black text-white px-2 py-1 font-bold">
                {dataset.samples} samples
              </span>
            </div>
            <p className="text-sm">{dataset.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
