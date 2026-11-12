# Models Directory

PixelProof AI supports three model tiers:

1. **Local Fine-Tuned ViT (Safetensors format)**:
   Place your Hugging Face Vision Transformer weights in:
   `models/my_deepfake_model/` (`model.safetensors`, `config.json`, `preprocessor_config.json`)

2. **PyTorch Checkpoint (.pth format)**:
   Place your PyTorch state dict in:
   `models/vit_deepfake.pth`

3. **PixelProof Native Engine (Vercel Serverless / Edge)**:
   Automatically active when running in resource-constrained or serverless environments without GPU or PyTorch C-libraries. Analyzes high-frequency Laplacian gradients and chromatic dispersion across a 4x4 spatial grid.

*(Note: Large weight files `*.safetensors` and `*.pth` are excluded from Git to comply with GitHub's 100MB file limit).*
