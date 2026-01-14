import { useState, useEffect } from 'react';
import Header from './components/Header';
import DatasetSelector from './components/DatasetSelector';
import ModelSelector from './components/ModelSelector';
import TokenSlider from './components/TokenSlider';
import ExperimentButton from './components/ExperimentButton';
import ResultsDisplay from './components/ResultsDisplay';
import Footer from './components/Footer';
import { logger } from './lib/logger';
import { AlertCircle } from 'lucide-react';

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

const BACKEND_URL = 'http://localhost:5000';

function App() {
  const [selectedDataset, setSelectedDataset] = useState('imdb');
  const [selectedModel, setSelectedModel] = useState('logistic');
  const [tokenCount, setTokenCount] = useState(50);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<ExperimentResults | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    logger.info('Application started');
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      const response = await fetch(`${BACKEND_URL}/api/models`, {
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        setBackendStatus('online');
        logger.info('Backend is online');
      } else {
        setBackendStatus('offline');
        logger.warning('Backend responded with error status', { status: response.status });
      }
    } catch (err) {
      setBackendStatus('offline');
      logger.warning('Backend is offline or unreachable', { error: err instanceof Error ? err.message : String(err) });
    }
  };

  const handleRunExperiment = async () => {
    if (backendStatus === 'offline') {
      setError('Backend server is offline. Please start the backend server by running: cd backend && python app.py');
      logger.error('Attempted to run experiment with offline backend');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);

    logger.info('Starting experiment', {
      dataset: selectedDataset,
      model: selectedModel,
      tokenCount,
    });

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000);

      const response = await fetch(`${BACKEND_URL}/api/experiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dataset: selectedDataset,
          model: selectedModel,
          prefixLength: tokenCount,
        }),
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      logger.info('Experiment completed successfully', {
        accuracy: data.prefix?.accuracy,
        performanceRetention: data.performance_retention,
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      logger.error('Experiment failed', err instanceof Error ? err : new Error(errorMessage), {
        dataset: selectedDataset,
        model: selectedModel,
        tokenCount,
      });

      if (err instanceof Error && err.name === 'AbortError') {
        setError('Request timeout. The experiment took too long to complete.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {backendStatus === 'offline' && (
          <div className="border-4 border-black bg-orange-300 p-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-black mb-2">BACKEND OFFLINE</h3>
                <p className="font-bold mb-2">
                  The Python backend server is not running. To use this application:
                </p>
                <ol className="list-decimal list-inside space-y-1 font-bold ml-4">
                  <li>Open a terminal in the project directory</li>
                  <li>Navigate to backend: <code className="bg-black text-white px-2 py-1">cd backend</code></li>
                  <li>Install dependencies: <code className="bg-black text-white px-2 py-1">pip install -r requirements.txt</code></li>
                  <li>Start server: <code className="bg-black text-white px-2 py-1">python app.py</code></li>
                </ol>
                <button
                  onClick={checkBackendStatus}
                  className="mt-4 px-4 py-2 bg-black text-white font-bold border-2 border-black hover:bg-white hover:text-black transition-colors"
                >
                  RETRY CONNECTION
                </button>
              </div>
            </div>
          </div>
        )}

        {backendStatus === 'checking' && (
          <div className="border-4 border-black bg-blue-300 p-6">
            <p className="font-bold">Checking backend status...</p>
          </div>
        )}
        <section className="border-4 border-black p-6 bg-yellow-300">
          <h2 className="text-2xl font-black mb-4">RESEARCH QUESTION</h2>
          <p className="text-lg font-bold">
            How much text do we really need for accurate classification? This experiment tests
            whether the first few tokens of a document contain enough information to classify it
            correctly — inspired by recent findings in prefix-based fine-tuning research.
          </p>
        </section>

        <div className="grid md:grid-cols-2 gap-6">
          <DatasetSelector
            selectedDataset={selectedDataset}
            onSelectDataset={setSelectedDataset}
          />
          <ModelSelector
            selectedModel={selectedModel}
            onSelectModel={setSelectedModel}
          />
        </div>

        <TokenSlider tokenCount={tokenCount} onTokenCountChange={setTokenCount} />

        <ExperimentButton
          onRunExperiment={handleRunExperiment}
          isLoading={isLoading}
        />

        {error && (
          <div className="border-4 border-black bg-red-400 p-6">
            <h3 className="text-xl font-black mb-2">ERROR</h3>
            <p className="font-bold">{error}</p>
          </div>
        )}

        {results && <ResultsDisplay results={results} />}
      </main>

      <Footer />
    </div>
  );
}

export default App;
