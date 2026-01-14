import { Brain } from 'lucide-react';

export default function Header() {
  return (
    <header className="border-b-4 border-black bg-yellow-300 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 mb-4">
          <div className="border-4 border-black bg-white p-3">
            <Brain size={40} strokeWidth={3} />
          </div>
          <div>
            <h1 className="text-4xl font-black tracking-tight">
              PREFIX-BASED TEXT CLASSIFICATION
            </h1>
            <p className="text-lg font-bold mt-1">
              How Much Text Is Really Needed?
            </p>
          </div>
        </div>
        <div className="border-4 border-black bg-white p-4">
          <p className="font-bold text-sm">
            Inspired by: "The First Few Tokens Are All You Need: An Efficient and Effective
            Unsupervised Prefix Fine-Tuning Method for Reasoning Models" (arXiv:2503.02875, 2025)
          </p>
        </div>
      </div>
    </header>
  );
}
