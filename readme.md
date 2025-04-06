# Image Enhancement with ESRGAN

This project demonstrates how to use **Enhanced Super-Resolution Generative Adversarial Networks (ESRGAN)** to enhance low-resolution images. Users can upload low-resolution images, which are then processed using either the **Real-ESRGAN** or **Anime ESRGAN** model for 4x upscaling.

## **Features**
- Enhance images using **Real-ESRGAN** and **Anime ESRGAN** models.
- **Flask** backend that handles image enhancement.

## **Technologies Used**
- **Frontend**: 
  
- **Backend**: 
  - **Flask** for the backend API.
  - **PyTorch** and **Real-ESRGAN** for image enhancement.

## **Installation & Setup**
> Python version: 3.9

### Backend (Flask):
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ds-mid-term.git
   cd ds-mid-term
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask app:
    ```bash
    python app.py
    ```