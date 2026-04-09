# Run Commands

## 1) Jalankan cepat
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 2) Jalankan mode mock
```bash
export MOCK_MODE=1
streamlit run app.py
```

## 3) Jalankan mode real Diffusers
```bash
export MOCK_MODE=0
export HF_TOKEN=your_huggingface_token
streamlit run app.py
```

## 4) Testing
```bash
PYTHONPATH=. pytest -q
```

## 5) Docker
```bash
docker build -t studioai-commerce .
docker run -p 8501:8501 studioai-commerce
```

## 6) Export kompatibel notebook lama
```bash
python -m streamlit run app.py
```
