from transformers import AutoModelForCausalLM, AutoTokenizer
import re
from bs4 import BeautifulSoup
import requests
import json

LOCAL_MODEL_PATH = "/mnt/c/Users/OYTGMCDs/Desktop/clova-project/HyperCLOVAX-SEED-Text-Instruct-1.5B"
model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)


def do_inference(url: str) -> str:
    res = generate_summary_title(web_document=extract_document_from_url(url))
    return extract_between_tags(res, "<|im_start|>assistant", "<|im_end|>")[0]


def generate_summary_title(web_document: dict[str, str]) -> list:
    chat = [
        {"role": "tool_list", "content": ""},
        {"role": "system", "content": (
            "너는 웹페이지 본문을 읽고 내용을 요약하는 전문가야.\n"
            "- 반드시 **의미가 명확한 문장형 **으로 요약해.\n"
            "- **40자 이내의 완성된 문장**이어야 해.\n"
            "- **본문의 핵심 키워드**를 반드시 포함해야 해.\n"
            "**설명, 부연, 해석 없이** 제목만 작성해.\n"
            "입력은 다음과 같은 형식이야:\n"
            "content: {\"title\" : \"제목\", \"content\" : \"내용\"\"}\n"
            "→ 주어진 title이 의미하는 내용을 참고하여 본문을 읽고, 핵심을 포착해 요약 문장을 만들어.\n"
            "출력은 **요약 문장 하나만** 정확하게 반환해."
        )},
        {
            "role": "user",
            "content": json.dumps({
                "title": web_document["title"],
                "content": web_document["content"]
            }, ensure_ascii=False)
        },
    ]
    print({"role": "user", "content": {"title": web_document["title"], "content": web_document["content"]}})

    inputs = tokenizer.apply_chat_template(chat, add_generation_prompt=True, return_dict=True, return_tensors="pt")
    output_ids = model.generate(**inputs, max_length=2048, stop_strings=["<|endofturn|>", "<|stop|>"],tokenizer=tokenizer)
    return tokenizer.batch_decode(output_ids)[0]


def extract_document_from_url(url: str) -> dict[str, str]:
    """
    주어진 URL의 웹페이지 내용을 크롤링하여 텍스트만 추출합니다.

    Args:
        url (str): 크롤링할 웹페이지의 URL.

    Returns:
        str: 웹페이지의 본문 텍스트 내용. 오류 발생 시 None을 반환합니다.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPError 발생 시 예외 처리

        soup = BeautifulSoup(response.content, 'html.parser')
        title = next(soup.stripped_strings, "제목 없음")
        # 텍스트 추출 (script, style 태그 제외)
        for script in soup.find_all('script'):
            script.decompose()
        for style in soup.find_all('style'):
            style.decompose()

        content = soup.get_text(separator='\n', strip=True)[:2000]
        return dict(title=title, content=content)

    except requests.exceptions.RequestException as e:
        print(f"요청 오류: {e}")
        return None
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return None


def extract_between_tags(text: str, start_tag: str, end_tag: str) -> list[str]:
    """
    주어진 텍스트에서 start_tag와 end_tag 사이의 문자열을 모두 추출하여 리스트로 반환합니다.
    """
    # 정규식 패턴 생성
    pattern = re.escape(start_tag) + r'(.*?)' + re.escape(end_tag)
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]
