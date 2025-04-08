# 🪄 AI Image Enhancer (React Native + Real-ESRGAN)

This is a mobile application that allows users to enhance the resolution of low-quality images using AI. It supports both **photo** and **anime-style** image enhancement using the **Real-ESRGAN model**.

---

## ✨ Features

- Upload an image from your gallery
- Select enhancement model:  
  `Default Model` or `Anime Model`
- Preview original and enhanced image
- Works with AI backend using Real-ESRGAN
- Modern UI with light/dark mode support

---

## 🧱 Tech Stack

| Layer      | Tech                                |
|------------|-------------------------------------|
| Frontend   | Expo (React Native), TypeScript     |
| Backend    | Python (Flask) + Real-ESRGAN model  |
| Enhancement Models | Real-ESRGAN, Anime model (x4) |
| UI Theme   | Custom tabs, parallax, collapsible |

---

## 🚀 Getting Started

### 📱 Frontend (React Native + Expo)

```bash
cd image-enhancer-app
npm install
npx expo start
```

- Make sure you're using Node.js and Expo CLI
- Install `expo-image-picker`, `@react-native-picker/picker`, and `react-native-paper` if not already

### 🧠 Backend (Flask + ESRGAN)

```bash
cd esrgan-backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python app.py
```

> Make sure to use **Python 3.9** for compatibility with Real-ESRGAN and PyTorch

---

## 📂 Folder Structure

```
├── esrgan-backend/       # Python Flask backend w/ Real-ESRGAN
├── image-enhancer-app/   # React Native frontend (Expo)
│   ├── app/(tabs)/index.tsx     # Home / Tutorial screen
│   ├── app/(tabs)/enhance.tsx   # Main enhancer screen
│   └── utils/imageEnhancer.ts   # Handles backend requests
```