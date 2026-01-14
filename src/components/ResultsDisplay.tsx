import { BarChart3, Target, TrendingUp } from 'lucide-react';

interface ExperimentResults {
  full_text: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    confusion_matrix: number[][];
  };
  prefix: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    confusion_matrix: number[][];
  };
  performance_retention: number;
  prefix_length: number;
  dataset_size: number;
  train_size: number;
  test_size: number;
  label_names: string[];
  plots: {
    comparison: string;
    confusion_full: string;
    confusion_prefix: string;
  };
}

interface ResultsDisplayProps {
  results: ExperimentResults;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const getPerformanceColor = (retention: number) => {
    if (retention >= 95) return 'bg-green-300';
    if (retention >= 85) return 'bg-yellow-300';
    return 'bg-red-300';
  };

  return (
    <div className="space-y-6">
      <div className="border-4 border-black p-6 bg-yellow-300">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp size={28} strokeWidth={3} />
          <h2 className="text-3xl font-black">EXPERIMENT RESULTS</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="border-4 border-black bg-white p-4">
            <p className="text-sm font-bold mb-1">Dataset Size</p>
            <p className="text-2xl font-black">{results.dataset_size}</p>
          </div>
          <div className="border-4 border-black bg-white p-4">
            <p className="text-sm font-bold mb-1">Prefix Length</p>
            <p className="text-2xl font-black">{results.prefix_length} tokens</p>
          </div>
          <div className={`border-4 border-black p-4 ${getPerformanceColor(results.performance_retention)}`}>
            <p className="text-sm font-bold mb-1">Performance Retention</p>
            <p className="text-2xl font-black">{results.performance_retention.toFixed(1)}%</p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="border-4 border-black p-6 bg-white">
          <div className="flex items-center gap-3 mb-4">
            <Target size={24} strokeWidth={3} />
            <h3 className="text-2xl font-black">FULL TEXT</h3>
          </div>
          <div className="space-y-3">
            <MetricRow label="Accuracy" value={results.full_text.accuracy} />
            <MetricRow label="Precision" value={results.full_text.precision} />
            <MetricRow label="Recall" value={results.full_text.recall} />
            <MetricRow label="F1 Score" value={results.full_text.f1_score} />
          </div>
        </div>

        <div className="border-4 border-black p-6 bg-white">
          <div className="flex items-center gap-3 mb-4">
            <Target size={24} strokeWidth={3} />
            <h3 className="text-2xl font-black">PREFIX ONLY</h3>
          </div>
          <div className="space-y-3">
            <MetricRow label="Accuracy" value={results.prefix.accuracy} />
            <MetricRow label="Precision" value={results.prefix.precision} />
            <MetricRow label="Recall" value={results.prefix.recall} />
            <MetricRow label="F1 Score" value={results.prefix.f1_score} />
          </div>
        </div>
      </div>

      <div className="border-4 border-black p-6 bg-white">
        <div className="flex items-center gap-3 mb-4">
          <BarChart3 size={24} strokeWidth={3} />
          <h3 className="text-2xl font-black">PERFORMANCE COMPARISON</h3>
        </div>
        <div className="border-4 border-black bg-gray-100 p-4">
          <img
            src={`data:image/png;base64,${results.plots.comparison}`}
            alt="Performance Comparison"
            className="w-full"
          />
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="border-4 border-black p-6 bg-white">
          <h3 className="text-xl font-black mb-4">CONFUSION MATRIX - FULL TEXT</h3>
          <div className="border-4 border-black bg-gray-100 p-2">
            <img
              src={`data:image/png;base64,${results.plots.confusion_full}`}
              alt="Confusion Matrix Full Text"
              className="w-full"
            />
          </div>
        </div>

        <div className="border-4 border-black p-6 bg-white">
          <h3 className="text-xl font-black mb-4">CONFUSION MATRIX - PREFIX</h3>
          <div className="border-4 border-black bg-gray-100 p-2">
            <img
              src={`data:image/png;base64,${results.plots.confusion_prefix}`}
              alt="Confusion Matrix Prefix"
              className="w-full"
            />
          </div>
        </div>
      </div>

      <div className="border-4 border-black p-6 bg-yellow-300">
        <h3 className="text-2xl font-black mb-4">KEY FINDINGS</h3>
        <div className="space-y-3 font-bold text-lg">
          <p>
            Using only the first {results.prefix_length} tokens achieves{' '}
            <span className="bg-white border-2 border-black px-2 py-1">
              {results.performance_retention.toFixed(1)}%
            </span>{' '}
            of the full text performance.
          </p>
          <p>
            Accuracy dropped from{' '}
            <span className="bg-white border-2 border-black px-2 py-1">
              {(results.full_text.accuracy * 100).toFixed(1)}%
            </span>{' '}
            to{' '}
            <span className="bg-white border-2 border-black px-2 py-1">
              {(results.prefix.accuracy * 100).toFixed(1)}%
            </span>
            {' '}— a difference of only{' '}
            <span className="bg-white border-2 border-black px-2 py-1">
              {((results.full_text.accuracy - results.prefix.accuracy) * 100).toFixed(1)}%
            </span>.
          </p>
          <p className="text-base mt-4 pt-4 border-t-4 border-black">
            This demonstrates that the beginning of a text often contains the most discriminative
            information for classification tasks. This finding aligns with recent research on
            prefix-based fine-tuning, suggesting that significant computational savings can be
            achieved by focusing on initial tokens without substantial performance loss.
          </p>
        </div>
      </div>
    </div>
  );
}

function MetricRow({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex justify-between items-center p-3 border-2 border-black">
      <span className="font-bold">{label}</span>
      <span className="font-black text-xl">{(value * 100).toFixed(2)}%</span>
    </div>
  );
}
