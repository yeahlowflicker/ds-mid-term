from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import torch
import cv2
import numpy as np
from PIL import Image
import io

class RealESRGAN:
    def __init__(self, model_path='weights/RealESRGAN_x4plus.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_arch = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=4
        )
        self.model = RealESRGANer(
            scale=4,
            model_path=model_path,
            model=model_arch,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=False,
            device=self.device
        )
    
    def enhance(self, image_bytes):
         # Load image
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(img)[:, :, ::-1]  # RGB to BGR for OpenCV
        
        # Run enhancement
        output, _ = self.model.enhance(img, outscale=4)
        
        # Convert BGR to RGB and back to PIL
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        output_image = Image.fromarray(output_rgb)
        
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        return buffer.getvalue()