import json
from typing import Dict, Optional

import requests


class LlmClient:
    def __init__(self, timeout_s: int = 60):
        self._timeout_s = max(5, int(timeout_s))
        self._session = requests.Session()

    def translate(self, text: str, target_language: str, config: Dict[str, str]) -> str:
        api_key = config.get("api_key", "")
        base_url = config.get("base_url", "")
        model = config.get("model", "")
        system_prompt = config.get("system_prompt", "")
        proxy = config.get("proxy", "")

        if not text.strip():
            return ""
        if not api_key:
            return "请先配置 LLM Token"
        if not base_url:
            return "请先配置 OpenAPI 地址"
        if not model:
            return "请先选择模型"

        prompt = self._build_prompt(system_prompt, target_language, text)

        url = f"{base_url.rstrip('/')}/models/{model}:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ]
        }

        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        }

        proxies: Optional[Dict[str, str]] = None
        if proxy:
            proxies = {
                "http": proxy,
                "https": proxy,
            }

        try:
            response = self._session.post(
                url,
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=self._timeout_s,
                proxies=proxies,
            )
        except requests.RequestException as exc:
            return f"LLM 请求失败: {exc}"

        if response.status_code != 200:
            return self._format_error(response)

        try:
            data = response.json()
        except ValueError:
            return "LLM 响应解析失败"

        text_value = self._extract_text(data)
        if not text_value:
            return "LLM 未返回有效翻译"
        return text_value

    def _build_prompt(self, system_prompt: str, target_language: str, text: str) -> str:
        target_language = target_language or "英文"
        system_prompt = system_prompt.strip()
        if system_prompt:
            return f"{system_prompt}\n目标语言：{target_language}。请翻译：{text}"
        return f"目标语言：{target_language}。请翻译：{text}"

    def _extract_text(self, data: Dict) -> str:
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            return ""
        return str(parts[0].get("text", "")).strip()

    def _format_error(self, response: requests.Response) -> str:
        try:
            data = response.json()
        except ValueError:
            return f"LLM 请求失败: HTTP {response.status_code}"
        error = data.get("error", {})
        message = error.get("message") or data.get("message") or "未知错误"
        return f"LLM 请求失败: {message}"
