# StudioAI Commerce

StudioAI Commerce adalah versi repo yang dirapikan dari notebook submission Streamlit Stable Diffusion, lalu dinaikkan menjadi project **AI Product Photo Studio** sesuai blueprint pada file markdown.

## Fitur utama
- Generate product scene dari prompt
- Upload foto produk
- Auto-mask foreground sederhana
- Background replacement
- Manual inpainting
- Outpainting / zoom out
- Riwayat hasil
- Export semua hasil ke ZIP
- `MOCK_MODE` supaya app tetap bisa dijalankan tanpa GPU / tanpa model terunduh

## Struktur project
```text
studioai-commerce/
├── app/
├── core/
├── pipelines/
├── services/
├── assets/
├── data/
├── docs/
├── notebooks/
├── tests/
├── app.py
├── logic.py
├── requirements.txt
├── Dockerfile
└── run.sh
```

## Cara menjalankan
### Opsi cepat
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Mode mock (default)
Mode ini aktif dari `.env.example` / environment dan tidak perlu download model. Cocok untuk demo struktur aplikasi.

```bash
export MOCK_MODE=1
streamlit run app.py
```

### Mode real Diffusers
Kalau ingin pakai Stable Diffusion beneran:
```bash
export MOCK_MODE=0
export HF_TOKEN=your_huggingface_token
streamlit run app.py
```

## File referensi yang disertakan
- `docs/project_blueprint.md` -> isi file markdown yang kamu upload
- `notebooks/original_submission.ipynb` -> notebook asli yang kamu upload
- `docs/migration_notes.md` -> ringkasan perubahan dari notebook ke repo modular

## Catatan penting
- Token `ngrok` hardcoded dari notebook **tidak** dipakai lagi.
- Export hasil ada di tab **History**.
- `logic.py` disediakan sebagai compatibility layer sederhana untuk notebook lama.

## Testing
```bash
pytest -q
```
