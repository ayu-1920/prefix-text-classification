import random
import numpy as np

class RealisticDataLoader:
    def __init__(self):
        self.datasets = {
            'imdb': self._generate_realistic_imdb_data,
            'news': self._generate_realistic_news_data
        }

    def load_dataset(self, dataset_id):
        if dataset_id in self.datasets:
            return self.datasets[dataset_id]()
        else:
            return self._generate_realistic_imdb_data()

    def _generate_realistic_imdb_data(self):
        """Generate more realistic IMDb data with more noise and ambiguity"""
        # Use time-based seed for variation
        random.seed()
        np.random.seed()

        positive_words = [
            'excellent', 'amazing', 'wonderful', 'great', 'good', 'nice', 'enjoyed',
            'loved', 'fantastic', 'brilliant', 'outstanding', 'superb', 'impressive'
        ]

        negative_words = [
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'disappointing',
            'boring', 'waste', 'poor', 'dreadful', 'pathetic', 'mediocre', 'weak'
        ]

        neutral_words = [
            'movie', 'film', 'story', 'plot', 'character', 'scene', 'acting',
            'director', 'cast', 'performance', 'script', 'watched', 'thought',
            'seemed', 'overall', 'experience', 'shows', 'features', 'minutes'
        ]

        ambiguous_words = [
            'interesting', 'different', 'unique', 'unexpected', 'surprising',
            'unusual', 'average', 'okay', 'fine', 'decent', 'alright'
        ]

        texts = []
        labels = []

        # Generate positive reviews
        for i in range(1000):
            length = random.randint(30, 120)
            words = []
            
            # Much more realistic distribution
            for j in range(length):
                if j < 10:  # First 10 words - still mixed
                    word_type = random.choices(
                        [positive_words, neutral_words, ambiguous_words, negative_words],
                        weights=[0.35, 0.40, 0.15, 0.10]  # 10% negative in positive reviews
                    )[0]
                else:  # Later words - very mixed
                    word_type = random.choices(
                        [positive_words, neutral_words, ambiguous_words, negative_words],
                        weights=[0.25, 0.45, 0.20, 0.10]  # Even more mixing
                    )[0]
                words.append(random.choice(word_type))
            
            texts.append(' '.join(words))
            # Add 8% label noise
            if random.random() < 0.08:
                labels.append(0)  # Wrong label
            else:
                labels.append(1)  # Correct positive label

        # Generate negative reviews
        for i in range(1000):
            length = random.randint(30, 120)
            words = []
            
            for j in range(length):
                if j < 10:  # First 10 words - still mixed
                    word_type = random.choices(
                        [negative_words, neutral_words, ambiguous_words, positive_words],
                        weights=[0.35, 0.40, 0.15, 0.10]  # 10% positive in negative reviews
                    )[0]
                else:  # Later words - very mixed
                    word_type = random.choices(
                        [negative_words, neutral_words, ambiguous_words, positive_words],
                        weights=[0.25, 0.45, 0.20, 0.10]  # Even more mixing
                    )[0]
                words.append(random.choice(word_type))
            
            texts.append(' '.join(words))
            # Add 8% label noise
            if random.random() < 0.08:
                labels.append(1)  # Wrong label
            else:
                labels.append(0)  # Correct negative label

        # Shuffle
        combined = list(zip(texts, labels))
        random.shuffle(combined)
        texts, labels = zip(*combined)

        return list(texts), list(labels), ['Negative', 'Positive']

    def _generate_realistic_news_data(self):
        """Generate more realistic news data"""
        random.seed()
        np.random.seed()

        categories = {
            'tech': ['technology', 'software', 'computer', 'digital', 'internet', 'app', 
                    'smartphone', 'laptop', 'programming', 'coding', 'data', 'ai'],
            'sports': ['game', 'team', 'player', 'score', 'match', 'win', 'lose',
                      'championship', 'league', 'season', 'coach', 'football', 'basketball'],
            'business': ['company', 'market', 'stock', 'economy', 'financial', 'profit',
                       'revenue', 'investment', 'trade', 'business', 'corporate', 'earnings'],
            'politics': ['government', 'election', 'policy', 'political', 'vote', 
                        'president', 'congress', 'senate', 'democrat', 'republican', 'bill']
        }

        common_words = ['said', 'reported', 'according', 'announced', 'today', 'yesterday',
                      'official', 'spokesperson', 'statement', 'news', 'update', 'latest']

        texts = []
        labels = []
        label_names = list(categories.keys())

        for label_idx, (category, category_words) in enumerate(categories.items()):
            other_words = [w for cat, words in categories.items() if cat != category for w in words]
            
            for i in range(500):
                length = random.randint(40, 100)
                words = []
                
                for j in range(length):
                    if j < 12:  # First 12 words - mixed but category-leaning
                        word_type = random.choices(
                            [category_words, common_words, other_words],
                            weights=[0.30, 0.50, 0.20]  # 20% other category words
                        )[0]
                    else:  # Later words - very mixed
                        word_type = random.choices(
                            [category_words, common_words, other_words],
                            weights=[0.20, 0.55, 0.25]  # 25% other category words
                        )[0]
                    words.append(random.choice(word_type))
                
                texts.append(' '.join(words))
                # Add 10% label noise for multi-class
                if random.random() < 0.10:
                    wrong_label = random.choice([i for i in range(len(categories)) if i != label_idx])
                    labels.append(wrong_label)
                else:
                    labels.append(label_idx)

        # Shuffle
        combined = list(zip(texts, labels))
        random.shuffle(combined)
        texts, labels = zip(*combined)

        return list(texts), list(labels), [c.capitalize() for c in label_names]
