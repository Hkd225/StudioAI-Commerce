from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = os.getenv("APP_TITLE", "StudioAI Commerce")
    model_id: str = os.getenv("MODEL_ID", "runwayml/stable-diffusion-v1-5")
    inpaint_model_id: str = os.getenv("INPAINT_MODEL_ID", "runwayml/stable-diffusion-inpainting")
    output_dir: str = os.getenv("OUTPUT_DIR", "data/outputs")
    temp_dir: str = os.getenv("TEMP_DIR", "data/temp")
    mock_mode: bool = os.getenv("MOCK_MODE", "1") == "1"
    enable_clipseg: bool = os.getenv("ENABLE_CLIPSEG", "0") == "1"
    hf_token: str | None = os.getenv("HF_TOKEN")
    ngrok_authtoken: str | None = os.getenv("NGROK_AUTHTOKEN")

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    @property
    def temp_path(self) -> Path:
        return Path(self.temp_dir)


def get_settings() -> Settings:
    return Settings()


def ensure_dirs(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    settings.output_path.mkdir(parents=True, exist_ok=True)
    settings.temp_path.mkdir(parents=True, exist_ok=True)
