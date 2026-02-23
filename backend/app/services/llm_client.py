from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from app.core.config import settings

MODEL_CATALOG = [
    {
        "value": "Qwen2.5-72B-Instruct",
        "label": "Qwen2.5-72B",
        "desc": "综合能力强，适合旅行规划与生成",
    },
    {
        "value": "DeepSeek-V3",
        "label": "DeepSeek-V3",
        "desc": "推理与代码能力均衡，适合复杂任务",
    },
    {
        "value": "DeepSeek-R1",
        "label": "DeepSeek-R1",
        "desc": "强化推理链路，适合深度思考",
    },
    {
        "value": "Hunyuan-TurboS",
        "label": "Hunyuan",
        "desc": "通用处理与长文本理解表现稳定",
    },
]


class LLMClient:
    def __init__(self) -> None:
        key = (settings.sophnet_api_key or "").strip()
        self.enabled = bool(key) and key != "replace_with_your_api_key"
        self.client = (
            OpenAI(
                api_key=key,
                base_url=settings.sophnet_base_url,
            )
            if self.enabled
            else None
        )

    def generate_itinerary(self, prompt_data: dict[str, Any]) -> dict[str, Any]:
        if not self.enabled or self.client is None:
            return self._fallback(prompt_data)

        messages = [
            {
                "role": "system",
                "content": (
                    "你是潮韵云脑行程规划智能体。请严格输出 JSON 对象，不要输出解释性文字。"
                    "JSON 字段必须包含：summary(字符串), itinerary(数组), culture_tips(字符串数组), "
                    "risk_alerts(字符串数组), signal_basis(字符串数组)。"
                    "其中 itinerary 的每一项包含 day(数字), period(字符串), activity(字符串), reason(字符串)。"
                ),
            },
            {
                "role": "user",
                "content": json.dumps(prompt_data, ensure_ascii=False),
            },
        ]
        try:
            requested_model = str(prompt_data.get("request", {}).get("model") or "").strip()
            model_values = {item["value"] for item in MODEL_CATALOG}
            target_model = requested_model if requested_model in model_values else settings.sophnet_model
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.2,
            )
            content = response.choices[0].message.content or ""
            parsed = self._parse_json_content(content)
            normalized = self._normalize_output(parsed, prompt_data)
            normalized["model_used"] = target_model
            return normalized
        except Exception:
            return self._fallback(prompt_data)

    @staticmethod
    def get_model_catalog() -> list[dict[str, str]]:
        return MODEL_CATALOG

    def _parse_json_content(self, content: str) -> dict[str, Any]:
        text = content.strip()
        # 兼容 ```json ... ``` 包裹
        fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            text = fenced.group(1).strip()

        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # 兼容前后有说明文字，仅提取首个 JSON 对象
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            maybe_json = text[start : end + 1]
            parsed = json.loads(maybe_json)
            if isinstance(parsed, dict):
                return parsed

        raise ValueError("LLM 未返回可解析的 JSON 对象")

    def _normalize_output(self, raw: dict[str, Any], prompt_data: dict[str, Any]) -> dict[str, Any]:
        itinerary_raw = raw.get("itinerary", [])
        itinerary: list[dict[str, Any]] = []
        if isinstance(itinerary_raw, list):
            for item in itinerary_raw:
                if not isinstance(item, dict):
                    continue
                itinerary.append(
                    {
                        "day": int(item.get("day", 1)),
                        "period": str(item.get("period", "全天")),
                        "activity": str(item.get("activity", "待补充活动")),
                        "reason": str(item.get("reason", "根据实时信号动态规划")),
                    }
                )

        return {
            "summary": str(raw.get("summary", "已生成动态行程建议")),
            "itinerary": itinerary if itinerary else self._fallback(prompt_data)["itinerary"],
            "culture_tips": [str(x) for x in raw.get("culture_tips", []) if isinstance(x, (str, int, float))],
            "risk_alerts": [str(x) for x in raw.get("risk_alerts", []) if isinstance(x, (str, int, float))],
            "signal_basis": [str(x) for x in raw.get("signal_basis", []) if isinstance(x, (str, int, float))],
        }

    def _fallback(self, prompt_data: dict[str, Any]) -> dict[str, Any]:
        request = prompt_data["request"]
        destination = request.get("destination", "潮汕")
        requested_model = str(request.get("model") or "").strip()
        model_values = {item["value"] for item in MODEL_CATALOG}
        target_model = requested_model if requested_model in model_values else settings.sophnet_model
        return {
            "summary": f"已基于规则为你生成 {destination} 动态行程建议。",
            "itinerary": [
                {
                    "day": 1,
                    "period": "上午",
                    "activity": "城市文化地标参访",
                    "reason": "首日先建立区域认知并控制体力消耗",
                },
                {
                    "day": 1,
                    "period": "下午",
                    "activity": "茶馆休整与非遗体验",
                    "reason": "符合潮汕午后节律并规避高温或降雨影响",
                },
            ],
            "culture_tips": prompt_data.get("culture_hints", []),
            "risk_alerts": prompt_data.get("risk_alerts", []),
            "signal_basis": prompt_data.get("signal_basis", []),
            "model_used": target_model,
        }
