import torch
import numpy as np
from PIL import Image
import io
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

class RealESRGAN_Anime:
    def __init__(self, model_path='weights/RealESRGAN_x4plus_anime_6B.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Create the model architecture specific for anime
        model_arch = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=6,
            num_grow_ch=32,
            scale=4
        )

        # Pass the anime model into RealESRGANer
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
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(img)[:, :, ::-1]  # RGB to BGR for OpenCV

        # Run enhancement
        output, _ = self.model.enhance(img, outscale=4)

        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        output_image = Image.fromarray(output_rgb)

        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        return buffer.getvalue()
