import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from pathlib import Path

DATA_DIR = Path("ml/data/processed")
print("🔍 Looking for data in:", DATA_DIR.resolve())

if not (DATA_DIR / "train").exists():
    raise FileNotFoundError(f"❌ Train folder not found at {DATA_DIR / 'train'}")
if not (DATA_DIR / "val").exists():
    raise FileNotFoundError(f"❌ Val folder not found at {DATA_DIR / 'val'}")
if not (DATA_DIR / "test").exists():
    raise FileNotFoundError(f"❌ Test folder not found at {DATA_DIR / 'test'}")

BATCH_SIZE = 32
NUM_EPOCHS = 5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ Transforms
train_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

test_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])
train_dataset = datasets.ImageFolder(DATA_DIR / "train", transform=train_transforms)
val_dataset = datasets.ImageFolder(DATA_DIR / "val", transform=test_transforms)
test_dataset = datasets.ImageFolder(DATA_DIR / "test", transform=test_transforms)


train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader  = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# ✅ Model
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 32 * 32, 256),  # works for 128x128 inputs
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN(num_classes=len(train_dataset.classes)).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ✅ Training + validation loop
for epoch in range(NUM_EPOCHS):
    # --- Train ---
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_acc = 100 * correct / total
    train_loss = running_loss / len(train_loader)

    # --- Validate ---
    model.eval()
    val_correct, val_total = 0, 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()

    val_acc = 100 * val_correct / val_total

    print(f"Epoch {epoch+1}/{NUM_EPOCHS} "
          f"| Train Loss: {train_loss:.4f} "
          f"| Train Acc: {train_acc:.2f}% "
          f"| Val Acc: {val_acc:.2f}%")

# ✅ Test evaluation
model.eval()
test_correct, test_total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        _, predicted = outputs.max(1)
        test_total += labels.size(0)
        test_correct += predicted.eq(labels).sum().item()

test_acc = 100 * test_correct / test_total
print(f"\n🎯 Final Test Accuracy: {test_acc:.2f}%")

# ✅ Save model
Path("ml/models").mkdir(parents=True, exist_ok=True)
torch.save(model.state_dict(), "ml/models/simple_cnn.pth")
print("✅ Model saved to ml/models/simple_cnn.pth")
