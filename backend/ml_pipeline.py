import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

from realistic_data import RealisticDataLoader

class MLPipeline:
    def __init__(self):
        self.data_loader = RealisticDataLoader()
        self.vectorizer_full = None
        self.vectorizer_prefix = None
        self.model_full = None
        self.model_prefix = None

    def get_model(self, model_id):
        """Get model instance based on ID"""
        models = {
            'logistic': LogisticRegression(max_iter=1000, random_state=42),
            'naive_bayes': MultinomialNB(),
            'svm': LinearSVC(max_iter=1000, random_state=42)
        }
        return models.get(model_id, LogisticRegression(max_iter=1000, random_state=42))

    def extract_prefix(self, texts, n_tokens):
        """Extract first N tokens from texts"""
        prefixes = []
        for text in texts:
            tokens = text.split()
            prefix = ' '.join(tokens[:n_tokens])
            prefixes.append(prefix if prefix else text)
        return prefixes

    def train_and_evaluate(self, X_train, X_test, y_train, y_test, model):
        """Train model and return metrics"""
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='weighted', zero_division=0
        )
        cm = confusion_matrix(y_test, y_pred)

        # Convert to list safely (handle both list and numpy array inputs)
        y_pred_list = y_pred.tolist() if hasattr(y_pred, 'tolist') else list(y_pred)
        y_test_list = y_test.tolist() if hasattr(y_test, 'tolist') else list(y_test)

        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred_list,
            'true_labels': y_test_list
        }

    def create_comparison_plot(self, full_metrics, prefix_metrics, prefix_length):
        """Create bar chart comparing full vs prefix performance"""
        fig, ax = plt.subplots(figsize=(10, 6))

        metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        full_values = [
            full_metrics['accuracy'],
            full_metrics['precision'],
            full_metrics['recall'],
            full_metrics['f1_score']
        ]
        prefix_values = [
            prefix_metrics['accuracy'],
            prefix_metrics['precision'],
            prefix_metrics['recall'],
            prefix_metrics['f1_score']
        ]

        x = np.arange(len(metrics))
        width = 0.35

        bars1 = ax.bar(x - width/2, full_values, width, label='Full Text',
                       color='#FFD700', edgecolor='black', linewidth=2)
        bars2 = ax.bar(x + width/2, prefix_values, width,
                       label=f'First {prefix_length} Tokens',
                       color='#FFFFFF', edgecolor='black', linewidth=2)

        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Full Text vs Prefix Performance', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontweight='bold')
        legend = ax.legend(frameon=True, edgecolor='black')
        legend.get_frame().set_linewidth(2)
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3, linewidth=1)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontweight='bold', fontsize=9)

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf.getvalue()

    def create_confusion_matrix_plot(self, cm, title, labels):
        """Create confusion matrix heatmap"""
        fig, ax = plt.subplots(figsize=(8, 6))

        # Create heatmap without problematic colorbar styling parameters
        sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd',
                   xticklabels=labels, yticklabels=labels,
                   linewidths=2, linecolor='black', cbar=True)

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
        ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf.getvalue()

    def run_experiment(self, dataset_id, model_id, prefix_length):
        """Run complete experiment comparing full text vs prefix"""
        # Load data
        texts, labels, label_names = self.data_loader.load_dataset(dataset_id)

        # Split data
        X_train_full, X_test_full, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Extract prefixes
        X_train_prefix = self.extract_prefix(X_train_full, prefix_length)
        X_test_prefix = self.extract_prefix(X_test_full, prefix_length)

        # Vectorize full text
        self.vectorizer_full = TfidfVectorizer(max_features=5000, stop_words='english')
        X_train_full_vec = self.vectorizer_full.fit_transform(X_train_full)
        X_test_full_vec = self.vectorizer_full.transform(X_test_full)

        # Vectorize prefix text
        self.vectorizer_prefix = TfidfVectorizer(max_features=5000, stop_words='english')
        X_train_prefix_vec = self.vectorizer_prefix.fit_transform(X_train_prefix)
        X_test_prefix_vec = self.vectorizer_prefix.transform(X_test_prefix)

        # Train and evaluate full text model
        model_full = self.get_model(model_id)
        full_metrics = self.train_and_evaluate(
            X_train_full_vec, X_test_full_vec, y_train, y_test, model_full
        )

        # Train and evaluate prefix model
        model_prefix = self.get_model(model_id)
        prefix_metrics = self.train_and_evaluate(
            X_train_prefix_vec, X_test_prefix_vec, y_train, y_test, model_prefix
        )

        # Calculate performance retention
        performance_retention = (prefix_metrics['accuracy'] / full_metrics['accuracy']) * 100

        # Generate plots
        comparison_plot = self.create_comparison_plot(full_metrics, prefix_metrics, prefix_length)

        cm_full_plot = self.create_confusion_matrix_plot(
            np.array(full_metrics['confusion_matrix']),
            'Confusion Matrix - Full Text',
            label_names
        )

        cm_prefix_plot = self.create_confusion_matrix_plot(
            np.array(prefix_metrics['confusion_matrix']),
            f'Confusion Matrix - First {prefix_length} Tokens',
            label_names
        )

        return {
            'full_text': full_metrics,
            'prefix': prefix_metrics,
            'performance_retention': float(performance_retention),
            'prefix_length': prefix_length,
            'dataset_size': len(texts),
            'train_size': len(X_train_full),
            'test_size': len(X_test_full),
            'label_names': label_names,
            'plots': {
                'comparison': comparison_plot,
                'confusion_full': cm_full_plot,
                'confusion_prefix': cm_prefix_plot
            }
        }

    def compare_token_counts(self, dataset_id, model_id):
        """Compare model performance across different token counts"""
        texts, labels, label_names = self.data_loader.load_dataset(dataset_id)

        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )

        token_counts = [5, 10, 20, 30, 50, 75, 100, 150, 200, -1]  # -1 means full text
        accuracies = []

        for n_tokens in token_counts:
            if n_tokens == -1:
                X_train_current = X_train
                X_test_current = X_test
            else:
                X_train_current = self.extract_prefix(X_train, n_tokens)
                X_test_current = self.extract_prefix(X_test, n_tokens)

            vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            X_train_vec = vectorizer.fit_transform(X_train_current)
            X_test_vec = vectorizer.transform(X_test_current)

            model = self.get_model(model_id)
            model.fit(X_train_vec, y_train)
            y_pred = model.predict(X_test_vec)

            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(float(accuracy))

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))

        x_labels = [str(t) if t != -1 else 'Full' for t in token_counts]
        bars = ax.bar(range(len(token_counts)), accuracies,
                     color='#FFD700', edgecolor='black', linewidth=2)

        ax.set_xlabel('Number of Tokens', fontsize=12, fontweight='bold')
        ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
        ax.set_title('Model Accuracy vs Token Count', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(token_counts)))
        ax.set_xticklabels(x_labels, fontweight='bold')
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3, linewidth=1)

        # Add value labels
        for i, (bar, acc) in enumerate(zip(bars, accuracies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{acc:.3f}',
                   ha='center', va='bottom', fontweight='bold', fontsize=9)

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return {
            'token_counts': [t if t != -1 else 'Full' for t in token_counts],
            'accuracies': accuracies,
            'plot': buf.getvalue()
        }
