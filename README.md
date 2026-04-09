# StudioAI Commerce 📸✨
**AI Product Photo Studio for E-Commerce & MSMEs**
### By Muhammad Auffa Hakim Aditya



StudioAI Commerce is a Streamlit-based application specifically designed to help MSMEs (Micro, Small, and Medium Enterprises) and marketplace sellers create studio-quality product promotional visuals in seconds. Leveraging the power of Generative AI (Stable Diffusion), this application automates the product photo editing process, which is typically time-consuming and expensive.

## ✨ Key Features
- **Text-to-Image Scene Generation:** Create studio backgrounds or natural landscapes using only text prompts.
- **Smart Auto-Masking:** Automatic product extraction using `rembg` (with a simple fallback mask).
- **Background Replacement:** Instantly replace product backgrounds without external editing software.
- **Manual Inpainting:** Edit specific areas of the image to add or remove objects.
- **Outpainting / Zoom Out:** Expand the image canvas without distorting the main product's proportions.
- **Batch Generation:** Generate 1 to 4 image variations simultaneously.
- **Local History & Export:** Save generation history locally and download the final high-resolution PNG results.

```

## 📂 Directory Structure

studioai-commerce/
├── app/               # Streamlit UI and frontend components
├── core/              # Core configurations and utilities
├── pipelines/         # Logic for Stable Diffusion (Inpaint, T2I, Outpaint)
├── services/          # Masking services integration (rembg) and image processing
├── assets/            # Static application assets (logos, placeholders)
├── data/              # Local history storage folder
├── notebooks/         # Experimental notebooks (development)
├── tests/             # Unit testing
├── .env.example       # Environment variables template
├── Dockerfile         # Docker configuration for deployment
├── README.md
├── requirements.txt
└── run.sh             # Bash script for quick run
```

## ⚙️ System Requirements
- **OS:** Linux / macOS / Windows (WSL recommended)
- **GPU:** An NVIDIA GPU with at least 8GB of VRAM is highly recommended for fast image generation. (It can run on a CPU, but it will take significantly longer).
- **Python:** Version 3.9 - 3.10

## 🚀 Local Setup

1. **Clone this repository:**
   git clone https://github.com/USERNAME/studioai-commerce.git
   cd studioai-commerce

2. **Create and activate a Virtual Environment:**
   python -m venv .venv
   source .venv/bin/activate   # For Linux / macOS
   # .venv\Scripts\activate    # For Windows

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Environment Configuration:**
   cp .env.example .env
   # Edit the .env file if specific tokens are required (e.g., HuggingFace token)

5. **Run the Streamlit Application:**
   streamlit run app/main.py

## 🔄 Application Workflow
1. **Upload:** Upload a raw product photo (e.g., shoes on the floor).
2. **Generate / Edit Mode:** Select from the sidebar menu:
   - *Background Replacement* to change the background.
   - *Manual Inpainting* to tidy up details.
   - *Outpainting* for landscape/portrait formats for store banners.
3. **Prompting:** Enter a description of the desired background (example: "product resting on a wooden table with cinematic studio lighting").
4. **Download:** Review the generated results, select the best one, and download it locally.

## 📌 Technical & Security Notes
- This project **has removed hardcoded tokens (such as ngrok/HuggingFace)** from all scripts and notebooks to prevent credential leaks. Please use the `.env` file.
- Default models use `runwayml/stable-diffusion-v1-5` and `runwayml/stable-diffusion-inpainting`.
- The application is fault-tolerant: If the `rembg` library fails to load or process, the system will automatically switch to a simple fallback mask method.

## 🗺️ Development Roadmap
- [ ] **Preset Categories:** Automated prompt templates (Skincare, Food, Fashion, Gadgets).
- [ ] **Interactive UI:** Before/After slider for image comparison.
- [ ] **AI Copywriter:** Automatic Instagram/Shopee caption generator based on product visuals.
- [ ] **Cloud Deployment:** Publish the application to Hugging Face Spaces or AWS/GCP.

------------------------------------------------------------

## 👨‍💻 Author
**Muhammad Auffa Hakim Aditya**

This project was developed as an exploration of:
- Generative AI & Stable Diffusion
- Streamlit Web Application Development
- AI-Powered E-Commerce Solutions
- Computer Vision (Auto-Masking & Inpainting)
