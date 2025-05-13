import numpy as np
import torch
import torch.nn as nn
from twilio.rest import Client
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# from keybert import KeyBERT
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk import pos_tag
# from fuzzywuzzy import fuzz
# import re
from sklearn.feature_extraction.text import TfidfVectorizer

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_categories, num_items):  # Include all parameters
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),   # 0
            nn.ReLU(),                            # 1
            nn.Dropout(0.3),                      # 2
            nn.Linear(hidden_size, hidden_size),  # 3
            nn.ReLU(),                            # 4
            nn.Dropout(0.3)
        )
        self.category_output = nn.Linear(hidden_size, num_categories)
        self.item_output = nn.Linear(hidden_size, num_items)

    def forward(self, x):
        x = self.flatten(x)
        features = self.linear_stack(x)
        category = self.category_output(features)
        item = self.item_output(features)
        return category, item

# Load the model
def load_model(path):
    # checkpoint = torch.load(path, map_location=torch.device('cpu'))
    checkpoint = torch.load(path, map_location='cpu')
    print(f'Model: {checkpoint}')
    # checkpoint.eval()

    # Use the saved architecture parameters
    input_size = checkpoint['input_size']
    hidden_size = checkpoint['hidden_size']
    num_categories = checkpoint['num_categories']
    num_items = checkpoint['num_items']

    # print(f"Hidden Size {checkpoint['hidden_size']}")

    # Rebuild the model exactly as trained
    model = NeuralNetwork(input_size, hidden_size, num_categories, num_items)
    optimizer = torch.optim.Adam(model.parameters())
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    model.load_state_dict(checkpoint['model_state_dict'])  # strict=True by default
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

    model.eval()  # Set to eval mode for inference
    return model, optimizer, scheduler

# def load_model(file_id, map_location='cpu'):
#     # Build direct download URL from file ID
#     url = f"https://drive.google.com/uc?export=download&id={file_id}"

#     response = requests.get(url)
#     print(f"Response {response}")
#     if response.status_code != 200:
#         raise Exception("Failed to fetch model from Google Drive")

#     # Wrap content in BytesIO and load using torch
#     buffer = io.BytesIO(response.content)
#     print(f"Buffer {buffer}")
#     model, optimizer, scheduler = torch.load(buffer, map_location=map_location, weights_only=False)
#     print(f"Model {model}")
#     print(f"Optimizer {optimizer}")
#     print(f"Scheduler {scheduler}")
#     model.eval()
#     return model, optimizer, scheduler

# Example usage:
# model, optimizer, scheduler = load_model('model_checkpoint.pth')

# def send_sms(to_number, message):
#     """Send SMS using Twilio"""
#     try:
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         client.messages.create(
#             body=message,
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=to_number
#         )
#     except Exception as e:
#         print(f"SMS sending failed: {str(e)}")

class ItemMatcher:
    def __init__(self):
        # Initialize pre-trained models
        self.image_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        # self.text_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        # self.text_model_advanced = SentenceTransformer('paraphrase-mpnet-base-v2', cache_folder='./model_cache')
        # self.keyword_model = KeyBERT(model=self.text_model)
        # self.stop_words = set(stopwords.words('english'))
        # self.important_pos = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ'}  # Nouns and adjectives

    def match_items(self, lost_item, found_items, threshold=0.6):
        matches = []
        
        for found_item in found_items:
            similarity_score = self._calculate_similarity(lost_item, found_item)
            print(f"Similarity score between '{lost_item.item_name}' and '{found_item.item_name}': {similarity_score}")
            if similarity_score >= threshold:
                matches.append({
                    'found_matched': found_item,
                    'similarity': similarity_score
                })
        
        return sorted(matches, key=lambda x: x['similarity'], reverse=True)
    
    def _calculate_similarity(self, lost_item, found_item):
        scores = []

        print(scores)
        
        # Category similarity (exact match)
        if lost_item.category == found_item.category:
            scores.append(1.0)
        else:
            scores.append(0.0)
            
        # Image similarity
        if lost_item.image and found_item.image:
            img_score = self._compare_images(lost_item.image.path, found_item.image.path)
            scores.append(img_score)
            
        # Text similarity
        print('text score')
        text_score = self._compare_descriptions(lost_item, found_item)
        scores.append(text_score)

        print(f"Scores: {scores}")
        
        # Weight and combine scores
        weights = [0.3, 0.4, 0.3] if lost_item.image and found_item.image else [0.3, 0.3] # Category, Image, Text weights
        final_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        
        return final_score
    
    def _compare_images(self, img1_path, img2_path):
        try:
            # Extract features from both images
            feat1 = self._extract_image_features(img1_path)
            feat2 = self._extract_image_features(img2_path)
            
            # Calculate cosine similarity 
            similarity = cosine_similarity(feat1.reshape(1, -1), feat2.reshape(1, -1))[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Image comparison error: {str(e)}")
            return 0.0
    
    def _extract_image_features(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        features = self.image_model.predict(x, verbose=0)
        return features.flatten()
    
    # def _extract_keywords(self, text):
    #     return text
        # Tokenize and tag parts of speech
        # print(f'Keyword Extraction')
        # print(f'Text {text}')
        # tokens = word_tokenize(text.lower())
        # print(f'Tokens {tokens}')
        # tagged = pos_tag(tokens)
        # print(f'Tagged {tagged}')
        
        # # Extract important words (nouns and adjectives)
        # keywords = [word for word, pos in tagged 
        #            if pos in self.important_pos 
        #            and word not in self.stop_words]
        # print(f'Keywords {keywords}')
        # return keywords
    
    # def _compare_descriptions(self, lost_item, found_item):
    #     lost_text = f"{lost_item.item_name} {lost_item.description}"
    #     found_text = f"{found_item.item_name} {found_item.description}"

    #     print(f'Lost Text {lost_text}')
    #     print(f'Found Text {found_text}')
        
    #     # Get embeddings
    #     lost_embedding = self.text_model.encode([lost_text])[0]
    #     found_embedding = self.text_model.encode([found_text])[0]
    #     # lost_embedding_advanced = self.text_model_advanced.encode([lost_text])[0]
    #     # found_embedding_advanced = self.text_model_advanced.encode([found_text])[0]

    #     # Calculate similarity
    #     similarity = cosine_similarity(
    #         lost_embedding.reshape(1, -1), 
    #         found_embedding.reshape(1, -1)
    #     )[0][0]

    #     # similarity_advanced = cosine_similarity(
    #     #     lost_embedding_advanced.reshape(1, -1), 
    #     #     found_embedding_advanced.reshape(1, -1)
    #     # )[0][0]
        
    #     return float(similarity)
    def _compare_descriptions(self, lost_item, found_item):
        lost_text = f"{lost_item.item_name} {lost_item.description}"
        found_text = f"{found_item.item_name} {found_item.description}"
        descriptions = [lost_text, found_text]

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform(descriptions)

        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return float(similarity[0][0])
        # # Get embeddings for semantic similarity
        # lost_embedding = self.text_model.encode([lost_text])[0]
        # found_embedding = self.text_model.encode([found_text])[0]
        # # Calculate semantic similarity
        # semantic_sim = float(cosine_similarity(
        #     lost_embedding.reshape(1, -1), 
        #     found_embedding.reshape(1, -1)
        # )[0][0])

        # # Extract keywords
        # lost_keywords = self._extract_keywords(lost_text)
        # found_keywords = self._extract_keywords(found_text)

        # # Calculate keyword matching score
        # keyword_matches = 0
        # total_keywords = len(lost_keywords)
        
        # for lost_word in lost_keywords:
        #     best_match = max([fuzz.ratio(lost_word, found_word) for found_word in found_keywords], default=0)
        #     if best_match > 80:  # 80% similarity threshold for fuzzy matching
        #         keyword_matches += 1

        # keyword_sim = keyword_matches / total_keywords if total_keywords > 0 else 0
        # # Check for negative patterns (contradictions)
        # negative_patterns = [
        #     (r'different color', r'color: (\w+)'),
        #     (r'not working', r'working condition'),
        #     (r'broken', r'good condition')
        # ]
        
        # contradiction_penalty = 0
        # for pattern, opposing in negative_patterns:
        #     if (re.search(pattern, lost_text.lower()) and re.search(opposing, found_text.lower())) or \
        #        (re.search(pattern, found_text.lower()) and re.search(opposing, lost_text.lower())):
        #         contradiction_penalty += 0.3

        # print(f'Contradiction Penalty {contradiction_penalty}')

        # # Combined score with weights
        # weights = {
        #     'semantic': 0.4,
        #     'keyword': 0.4,
        #     'contradiction': 0.2
        # }
        
        # final_score = (
        #     (semantic_sim * weights['semantic']) +
        #     (keyword_sim * weights['keyword']) -
        #     (contradiction_penalty * weights['contradiction'])
        # )

        # print(f'Final Score {final_score}')

        # # Ensure score is between 0 and 1
        # final_score = max(0, min(1, final_score))

        # print(f'Final Score (clamped) {final_score}')
        
        # return final_score