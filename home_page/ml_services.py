import numpy as np
import torch
import torch.nn as nn
from twilio.rest import Client
from .models import LostItem, FoundItem
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_categories, num_items):  # Include all parameters
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),   # 0
            nn.ReLU(),                            # 1
            nn.Dropout(0.3),                      # 2
            nn.Linear(hidden_size, hidden_size), # 3
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
    checkpoint = torch.load(path, map_location=torch.device('cpu'))

    # Use the saved architecture parameters
    input_size = checkpoint['input_size']
    hidden_size = checkpoint['hidden_size']
    num_categories = checkpoint['num_categories']
    num_items = checkpoint['num_items']

    print(f"Hidden Size {checkpoint['hidden_size']}")

    # Rebuild the model exactly as trained
    model = NeuralNetwork(input_size, hidden_size, num_categories, num_items)
    optimizer = torch.optim.Adam(model.parameters())
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    model.load_state_dict(checkpoint['model_state_dict'])  # strict=True by default
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

    model.eval()  # Set to eval mode for inference
    return model, optimizer, scheduler

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
        self.text_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
    def match_items(self, lost_item, found_items, threshold=0.7):
        matches = []

        print(f'Matches: {matches}')
        
        for found_item in found_items:
            similarity_score = self._calculate_similarity(lost_item, found_item)
            if similarity_score >= threshold:
                matches.append({
                    'found_item': found_item,
                    'similarity': similarity_score
                })

        print(f'Matches: {matches}')
        
        return sorted(matches, key=lambda x: x['similarity'], reverse=True)
    
    def _calculate_similarity(self, lost_item, found_item):
        scores = []

        print('Calculating Similarity...')
        
        # Category similarity (exact match)
        if lost_item.category == found_item.category:
            scores.append(1.0)
        else:
            scores.append(0.0)

        print('checling category...')
            
        # Image similarity
        if lost_item.image and found_item.image:
            img_score = self._compare_images(lost_item.image.path, found_item.image.path)
            scores.append(img_score)
            
        # Text similarity
        text_score = self._compare_descriptions(lost_item, found_item)
        scores.append(text_score)

        print(f'Score {scores}')
        
        # Weight and combine scores
        weights = [0.3, 0.4, 0.3] if lost_item.image and found_item.image else [0.3, 0.3] # Category, Image, Text weights
        final_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)

        print(f'Final Score {final_score}')
        
        return final_score
    
    def _compare_images(self, img1_path, img2_path):
        print('Comparing Image..')
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
        print('Extracting Features in image...')
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        features = self.image_model.predict(x, verbose=0)
        return features.flatten()
    
    def _compare_descriptions(self, lost_item, found_item):
        print('Comparing Description...')
        lost_text = f"{lost_item.item_name} {lost_item.description}"
        found_text = f"{found_item.item_name} {found_item.description}"

        print(f'Lost Text {lost_text}')
        print(f'Found Text {found_text}')
        
        # Get embeddings
        lost_embedding = self.text_model.encode([lost_text])[0]
        found_embedding = self.text_model.encode([found_text])[0]
        
        # Calculate similarity
        similarity = cosine_similarity(
            lost_embedding.reshape(1, -1), 
            found_embedding.reshape(1, -1)
        )[0][0]

        print(f'Similarity {similarity}')
        
        return float(similarity)