# Prefix-Based Text Classification: How Much Text Is Really Needed?

An interactive machine learning web application that demonstrates how classification accuracy is affected by using only the first few tokens (prefix) of text documents. This project is inspired by the 2025 research paper "The First Few Tokens Are All You Need: An Efficient and Effective Unsupervised Prefix Fine-Tuning Method for Reasoning Models" (arXiv:2503.02875).

## Project Overview

This application compares the performance of traditional ML classifiers when trained on:
- Full text documents
- Only the first N tokens (prefix) of documents

The key finding: In many cases, the first few tokens contain sufficient discriminative information for accurate classification, potentially enabling significant computational savings.

## Features

- **Multiple Datasets**: IMDb Movie Reviews (sentiment) and News Category Dataset (multi-class)
- **Multiple Models**: Logistic Regression, Naive Bayes, and Support Vector Machine
- **Interactive Experimentation**: Adjust prefix length with a slider (5-200 tokens)
- **Comprehensive Metrics**: Accuracy, Precision, Recall, F1 Score
- **Rich Visualizations**: Performance comparison charts and confusion matrices
- **New Brutalism Design**: Bold, expressive UI with flat colors and thick borders

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Lucide React for icons
- New Brutalism design aesthetic

### Backend
- Flask (Python) REST API
- scikit-learn for ML models
- pandas and numpy for data processing
- matplotlib and seaborn for visualizations

## Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- pip

### Frontend Setup
```bash
npm install
npm run dev
```

### Backend Setup

#### Option 1: Using the startup script (Recommended)

**Linux/Mac:**
```bash
./start-backend.sh
```

**Windows:**
```bash
start-backend.bat
```

#### Option 2: Manual setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The Flask backend will run on `http://localhost:5000`

## Logging & Monitoring

### Backend Logs
- **Console output**: Real-time logs in terminal
- **File logs**: `backend/backend.log`
- **Database logs**: Stored in Supabase `error_logs` table

### Frontend Logs
- **Console output**: Browser developer console
- **Database logs**: Stored in Supabase `error_logs` table
- **Automatic error capturing** for uncaught errors and unhandled promises

### Viewing Logs in Database

All logs are stored in Supabase:

```sql
-- View recent error logs
SELECT * FROM error_logs ORDER BY created_at DESC LIMIT 50;

-- View backend errors only
SELECT * FROM error_logs WHERE source = 'backend' ORDER BY created_at DESC;

-- View critical errors
SELECT * FROM error_logs WHERE level = 'critical' ORDER BY created_at DESC;
```

### Experiment History

All experiments are automatically saved to the database:

```sql
-- View recent experiments
SELECT dataset_id, model_id, prefix_length, performance_retention, created_at
FROM experiments
ORDER BY created_at DESC
LIMIT 20;
```

## Usage

1. **Start Backend**: Run `./start-backend.sh` (or `.bat` on Windows)
2. **Start Frontend**: Run `npm run dev` in a separate terminal
3. **Select a Dataset**: Choose between IMDb reviews or News categories
4. **Select a Model**: Pick from Logistic Regression, Naive Bayes, or SVM
5. **Set Prefix Length**: Use the slider to choose how many tokens to use (5-200)
6. **Run Experiment**: Click the button to train both models and compare results
7. **Review Results**: Examine metrics, visualizations, and key findings

### Troubleshooting

#### Backend Connection Issues

If you see "BACKEND OFFLINE" message:

1. Ensure Python backend is running: `cd backend && python app.py`
2. Check if port 5000 is available
3. Check backend logs in `backend/backend.log`
4. Click "RETRY CONNECTION" button in the UI

#### Missing Dependencies

Backend:
```bash
cd backend
pip install -r requirements.txt
```

Frontend:
```bash
npm install
```

## Key Findings

The application demonstrates that:
- Using only the first 50 tokens often retains 90%+ of full-text performance
- Initial tokens frequently contain the most discriminative information
- Significant computational savings are possible with minimal accuracy loss
- This aligns with recent research on efficient prefix-based fine-tuning

## Project Structure

```
project/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── DatasetSelector.tsx
│   │   ├── ModelSelector.tsx
│   │   ├── TokenSlider.tsx
│   │   ├── ExperimentButton.tsx
│   │   ├── ResultsDisplay.tsx
│   │   └── Footer.tsx
│   ├── App.tsx
│   └── index.css
├── backend/
│   ├── app.py              # Flask API
│   ├── ml_pipeline.py      # ML training & evaluation
│   ├── data_loader.py      # Dataset generation
│   └── requirements.txt
└── package.json
```

## Research Reference

This project is inspired by:

**"The First Few Tokens Are All You Need: An Efficient and Effective Unsupervised Prefix Fine-Tuning Method for Reasoning Models"**
- arXiv:2503.02875
- Published: 2025
- [Read on arXiv](https://arxiv.org/abs/2503.02875)

## License

MIT License - feel free to use this project for educational purposes.
