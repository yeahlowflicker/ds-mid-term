import cv2
import numpy as np

def enhance_quality_with_sobel(image_bytes: bytes, edge_weight: float = 1.0) -> bytes:
    """
    Enhances the quality of an image by applying the Sobel operator to enhance edges 
    and then blending these edges with the original image to boost detail and sharpness.

    Parameters:
      image_bytes (bytes): The input image as a byte array.
      edge_weight (float): How much to weigh the sobel edges when blending (default: 1.0)

    Returns:
      bytes: The enhanced image encoded as PNG.
    """
    # Convert byte array to NumPy array and decode
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image data; unable to decode image.")
        
    # Optional: resize or apply denoising before processing
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    
    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise before edge detection
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Compute gradients using Sobel operator (use cv2.CV_64F for precision)
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    
    # Compute gradient magnitude and scale to 0-255
    magnitude = cv2.magnitude(grad_x, grad_y)
    # Avoid division by zero in case of blank input
    if np.max(magnitude) > 0:
        magnitude = np.uint8(255 * (magnitude / np.max(magnitude)))
    else:
        magnitude = np.uint8(magnitude)
    
    # Optional: sharpen the edge map using a threshold or morphological operations
    # Here we perform a simple threshold to create a strong edge mask:
    _, edge_mask = cv2.threshold(magnitude, 50, 255, cv2.THRESH_BINARY)
    edge_mask = cv2.GaussianBlur(edge_mask, (3, 3), 0)
    
    # Convert edge mask to three channels to blend with the color image
    edge_mask_color = cv2.cvtColor(edge_mask, cv2.COLOR_GRAY2BGR)
    
    # Blend the edge-enhanced image with the original image.
    # The idea is to add higher contrast details from the edge mask to the image.
    sharpened = cv2.addWeighted(image, 1.0, edge_mask_color, edge_weight / 255.0, 0)
    
    # Postprocess: Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    # This helps boosting the overall image contrast while preserving local details.
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    lab_enhanced = cv2.merge((cl, a, b))
    final_img = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    # Encode back to bytes (PNG format)
    success, encoded_image = cv2.imencode('.png', final_img)
    if not success:
        raise RuntimeError("Failed to encode the image.")

    return encoded_image.tobytes()

# Example usage
if __name__ == "__main__":
    # Load an image from file (as bytes) for testing purposes.
    with open("input_image.jpg", "rb") as f:
        img_bytes = f.read()
    
    # Enhance the image quality with Sobel edge processing and postprocessing
    enhanced_bytes = enhance_quality_with_sobel(img_bytes, edge_weight=1.5)
    
    # Save the result to verify the enhancement visually
    with open("enhanced_image.png", "wb") as out_file:
        out_file.write(enhanced_bytes)
