from django.apps import AppConfig
import nltk


class HomePageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home_page'

    def ready(self):
        required_nltk_data = {
            'tokenizers/punkt': 'punkt',
            'taggers/averaged_perceptron_tagger': 'averaged_perceptron_tagger',
            'corpora/stopwords': 'stopwords'
        }

        for path, package in required_nltk_data.items():
            try:
                nltk.data.find(path)
                print(f"Found NLTK data: {path}")
            except LookupError:
                print(f"Downloading missing NLTK data: {package}")
                nltk.download(package)
