from .celery_app import app
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import cv2
import numpy as np
from scipy.stats import variation


class MLPClassifierV2(torch.nn.Module):
    def __init__(self, input_dim=1796):
        super(MLPClassifierV2, self).__init__()
        self.dropout1 = torch.nn.Dropout(0.5)
        self.dropout2 = torch.nn.Dropout(0.3)
        self.dropout3 = torch.nn.Dropout(0.1)
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 1024),
            torch.nn.BatchNorm1d(1024),
            torch.nn.ReLU(),
            self.dropout1,
            torch.nn.Linear(1024, 512),
            torch.nn.BatchNorm1d(512),
            torch.nn.ReLU(),
            self.dropout2,
            torch.nn.Linear(512, 128),
            torch.nn.BatchNorm1d(128),
            torch.nn.ReLU(),
            self.dropout3,
            torch.nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.model(x)

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((380, 380)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def extract_frames(video_path, max_frames=60):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idxs = np.linspace(0, frame_count - 1, max_frames, dtype=int)
    for idx in frame_idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    return frames

def calculate_eyeblink_rate(frames):
    return np.random.uniform(0.1, 0.5)

def calculate_head_pose_variance(frames):
    return np.random.uniform(0.05, 0.2)

def calculate_texture_variance(frames):
    textures = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        textures.append(variation(gray))
    return np.mean(textures)

def calculate_blur_score(frames):
    blurs = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurs.append(cv2.Laplacian(gray, cv2.CV_64F).var())
    return np.mean(blurs)


def load_models():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    effnet = models.efficientnet_b4(weights=models.EfficientNet_B4_Weights.DEFAULT)
    effnet.classifier = torch.nn.Identity()
    effnet = effnet.to(device).eval()

    mlp_model = MLPClassifierV2(input_dim=1796)
    mlp_model.load_state_dict(torch.load('models/best_model.pth', map_location=device))
    mlp_model = mlp_model.to(device).eval()

    return {'effnet': effnet, 'mlp': mlp_model, 'device': device}


loaded_models = load_models()

@app.task
def predict(video_path: str, max_frames=60):
    effnet = loaded_models['effnet']
    mlp_model = loaded_models['mlp']
    device = loaded_models['device']


    # Извлечение кадров
    frames = extract_frames(video_path, max_frames)
    if len(frames) == 0:
        raise ValueError("No frames extracted from video.")
    

    predictions = []

    # Обработка каждого кадра
    for idx, frame in enumerate(frames):
        
        try:
            input_tensor = transform(frame).unsqueeze(0).to(device)
            with torch.no_grad():
                effnet_feature = effnet(input_tensor).squeeze().cpu().numpy()

            eyeblink_rate = calculate_eyeblink_rate([frame])
            head_pose_var = calculate_head_pose_variance([frame])
            texture_var = calculate_texture_variance([frame])
            blur_score = calculate_blur_score([frame])


            final_feature = np.concatenate([effnet_feature, np.array([eyeblink_rate, head_pose_var, texture_var, blur_score])])
            final_feature = torch.tensor(final_feature, dtype=torch.float32).unsqueeze(0).to(device)

            with torch.no_grad():
                output = mlp_model(final_feature)
                prob = torch.sigmoid(output).item()

            pred = 1 if prob >= 0.5 else 0
            predictions.append(pred)

        except Exception as e:
            continue  # Пропускаем ошибочный кадр и продолжаем обработку

    # Подсчёт итоговых результатов
    predictions = np.array(predictions)
    real_votes = np.sum(predictions == 0)
    fake_votes = np.sum(predictions == 1)
    verdict = "REAL" if real_votes >= fake_votes else "FAKE"
    confidence = f"{max(real_votes, fake_votes) / len(predictions) * 100:.2f}%"


    if isinstance(confidence, str) and confidence.endswith('%'):
        confidence = float(confidence.strip('%'))

    return {
        'verdict': verdict,
        'real_votes': int(real_votes),
        'fake_votes': int(fake_votes),
        'total_frames': len(predictions),
        'confidence': confidence
    }
