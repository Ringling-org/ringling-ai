from pathlib import Path
import os
import subprocess
import json
import yaml
from services.crawler import crawl_page

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = BASE_DIR / "config" / "config.yaml"
CONFIG_PATH = Path(os.getenv("CONFIG_PATH", DEFAULT_CONFIG)).resolve()

def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config(CONFIG_PATH)

summarize_prompt = config["summarize"]["title_prompt"]
command = config["summarize"]["command"]
model = config["summarize"]["model"]

def summarize_title(url: str) -> str:
    web_doc = crawl_page(url)
    if web_doc is None:
        raise ValueError(f"URL 크롤링 실패: {url}")

    return do_summarize_title(web_doc)

def do_summarize_title(web_document: dict[str, str]) -> str:
    prompt = (
        summarize_prompt
        + "\n\ncontent: "
        + json.dumps({
            "title": web_document["title"],
            "content": web_document["content"]
        }, ensure_ascii=False)
    )

    command_line = [
        command,
        "-p", prompt,
        "-m", model
    ]
    result = subprocess.run(
        command_line,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"요약 모델 오류: {result.stderr}")

    return result.stdout.strip().splitlines()[-1]
