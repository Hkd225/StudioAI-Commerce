import io
import zipfile

from PIL import Image

from services.export_service import build_export_zip


def test_build_export_zip_contains_images():
    img = Image.new("RGB", (64, 64), "red")
    data = build_export_zip([{"label": "demo", "kind": "test", "image": img}], readme_text="hello")
    assert zipfile.is_zipfile(io.BytesIO(data))
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        assert "README_EXPORT.txt" in names
        assert any(name.endswith('.png') for name in names)
