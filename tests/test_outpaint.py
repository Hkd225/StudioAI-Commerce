from PIL import Image

from pipelines.outpaint import prepare_outpainting


def test_prepare_outpainting_expands_canvas():
    image = Image.new("RGB", (128, 128), "white")
    canvas, mask = prepare_outpainting(image, expand_pixels=64)
    assert canvas.size[0] > image.size[0]
    assert canvas.size == mask.size
