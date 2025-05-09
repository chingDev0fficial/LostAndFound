from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services import process_lost_item, process_found_item
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .ml_services import load_model
from pathlib import Path
import os
import torch
from PIL import Image
from torchvision import transforms
from huggingface_hub import hf_hub_download

HF_TOKEN = os.getenv("HF_TOKEN")

REPO_ID = repo_id="chingDev/item-recognizer"
FILE_NAME = 'model_checkpoint.pth'

MODEL_PATH = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILE_NAME,
    token=HF_TOKEN
)

# Create your views here.
def home(request):
    return render(request, 'home_page/home.html')

def about(request):
    return render(request, 'home_page/about.html')

def contact(request):
    return render(request, 'home_page/contact.html')

@csrf_exempt
def item_lost_report(request):
    if request.method == 'POST':
        try:
            result = process_lost_item(request)
            print(result)
            return JsonResponse({
                'result': result,
                'success': True,
                'message': 'Successfully Submitted the Form'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
        
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def item_found_report(request):
    if request.method == 'POST':
        try:
            result = process_found_item(request)
            
            return JsonResponse({
                'result': result,
                'success': True,
                'message': 'Found item report submitted successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def recognize_image(request):
    # model, optimizer, scheduler = load_model(Path(__file__).parent / 
    #                                          'ml_models' / 
    #                                          'model_checkpoint.pth')
    
    # model, optimizer, scheduler = load_model('1PWzIlXi3OMSZo200h5mTpI4J3GaeEM6r')
    # print(f'request {request.FILES.get("image")}')
    image_file = request.FILES['image']
    temp_path = os.path.join('temp', image_file.name)
    path = default_storage.save(temp_path, ContentFile(image_file.read()))

    with Image.open(default_storage.open(path)) as img:
        # Preprocess image for model
        img = img.convert('RGB')
        img = img.resize((224, 224))  # Resize to model input size
        
        # Load model and get prediction
        # model, optimizer, scheduler = load_model(Path(__file__).parent.parent / 
        #                                         'ml_services' / 'ml_models' / 
        #                                         'model_checkpoint.pth')
        model, optimizer, scheduler = load_model(MODEL_PATH)
        

        # Convert PIL image to tensor and get prediction
        transform = transforms.Compose([
            transforms.Resize((28, 28)),  # Resize images to consistent size
            transforms.ToTensor(),  # Convert to PyTorch tensor
        ])
        image_tensor = transform(img).unsqueeze(0)
        # Your prediction code here...

        category_output, item_output = model(image_tensor)
                
        # Get predicted category
        categ_probabilities = torch.softmax(category_output, dim=1)
        categ_confidence, categ_predicted = torch.max(categ_probabilities, 1)

        # Get predicted item
        item_probabilities = torch.softmax(item_output, dim=1)
        item_confidence, item_predicted = torch.max(item_probabilities, 1)
        
        # Map to category name
        # categories = [choice[0] for choice in FoundItem.CATEGORY_CHOICES]
        # predicted_category = categories[predicted.item()]
        # print(f'Category: {categ_predicted.item()}')
        # print(f'Item: {item_predicted.item()}')

        categ = ['stationery', 'electronics']  # Convert category index to string
        lab = {
            0: ['Pen'],      # Stationery labels
            1: ['Laptop', 'Mouse']    # Electronics labels
        }  # Convert label index to string

        c = categ[categ_predicted.item()]
        l = lab[categ_predicted.item()][item_predicted.item()]

        print(f'Category: {c}')
        print(f'Item: {l}')

        return JsonResponse({
            'success': True,
            'category': [c, categ_confidence.item()],
            'item': [l, item_confidence.item()]
            # 'suggested_name': f"Found {predicted_category.replace('_', ' ').title()}"
        })
                
        # Clean up temporary file
        # default_storage.delete(path)
        
        # return JsonResponse({
        #     'success': True,
        #     'category': 'predicted_category',
        #     'confidence': 0.95,
        #     'suggested_name': 'Predicted Item Name'
        # })

    data = {'status': 'success'}
    return JsonResponse(data)