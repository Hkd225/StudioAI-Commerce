# Migration Notes

Notebook submission asli memiliki struktur utama:
- `logic.py` ditulis dari beberapa cell
- `app.py` Streamlit ada di satu file besar
- deployment memakai `pyngrok` dan token hardcoded

Perubahan pada repo ini:
1. Logic dipecah ke `core/`, `pipelines/`, dan `services/`.
2. UI dipisah ke `app/ui_generate.py`, `app/ui_edit.py`, dan `app/ui_history.py`.
3. Ditambahkan `MOCK_MODE` agar aplikasi tetap dapat dijalankan tanpa GPU.
4. Ditambahkan fitur export ZIP dan dokumentasi repo.
5. Token rahasia dipindah ke `.env.example`.
