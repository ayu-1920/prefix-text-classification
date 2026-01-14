import { FileText, User } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t-4 border-black bg-black text-white mt-12">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="border-4 border-white p-6">
            <div className="flex items-center gap-3 mb-3">
              <FileText size={24} strokeWidth={3} />
              <h3 className="text-xl font-black">RESEARCH PAPER</h3>
            </div>
            <p className="font-bold mb-2">
              "The First Few Tokens Are All You Need: An Efficient and Effective Unsupervised
              Prefix Fine-Tuning Method for Reasoning Models"
            </p>
            <p className="text-sm font-bold text-gray-300">
              arXiv:2503.02875, 2025
            </p>
            <a
              href="https://arxiv.org/abs/2503.02875"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 bg-yellow-300 text-black border-2 border-white px-4 py-2 font-black hover:bg-yellow-400 transition-colors"
            >
              READ PAPER
            </a>
          </div>

          <div className="border-4 border-white p-6">
            <div className="flex items-center gap-3 mb-3">
              <User size={24} strokeWidth={3} />
              <h3 className="text-xl font-black">ABOUT THIS PROJECT</h3>
            </div>
            <p className="font-bold mb-3">
              An interactive demonstration exploring how much text is truly necessary for accurate
              classification tasks, inspired by cutting-edge research in prefix-based fine-tuning.
            </p>
            <p className="text-sm font-bold text-gray-300">
              Built with React, Flask, and scikit-learn
            </p>
          </div>
        </div>

        <div className="text-center mt-6 pt-6 border-t-4 border-white">
          <p className="font-black text-lg">
            ML RESEARCH DEMONSTRATION · 2025
          </p>
        </div>
      </div>
    </footer>
  );
}
