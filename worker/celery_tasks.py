import numpy as np
import torch
from .celery_app  import app
import torch.nn as nn
import numpy as np


class TransformerClassifier(nn.Module):
    def __init__(self, input_dim=1792, seq_len=60, d_model=512, nhead=8,
                 num_layers=4, dim_feedforward=1024, dropout=0.5):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead,
            dim_feedforward=dim_feedforward, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Sequential(
            nn.Linear(d_model, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.input_proj(x)
        x = self.transformer_encoder(x)
        x = x.mean(dim=1)
        return self.classifier(x).squeeze(1)



def load_model(model_path: str):
    model = TransformerClassifier()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model


@app.task
def predict(model_path: str, features: list):
    with torch.no_grad():
        features = np.array(features)
        model = load_model(model_path)
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # [1, 60, 1792]
        output = model(x)
        prob = output.item()
        label = "FAKE" if prob > 0.5 else "REAL"
        return label, round(prob, 4)
        
    
