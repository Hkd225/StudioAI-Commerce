from core.utils import slugify


def test_slugify_basic():
    assert slugify("StudioAI Commerce!!") == "studioai-commerce"
