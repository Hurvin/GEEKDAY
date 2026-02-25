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
                    "你是潮韵同行行程规划智能体。请严格输出 JSON 对象，不要输出解释性文字。"
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

    def generate_chat_reply(self, request_data: dict[str, Any]) -> dict[str, str]:
        requested_model = str(request_data.get("model") or "").strip()
        model_values = {item["value"] for item in MODEL_CATALOG}
        target_model = requested_model if requested_model in model_values else settings.sophnet_model

        if not self.enabled or self.client is None:
            user_message = str(request_data.get("message", "")).strip()
            fallback_text = "我是潮韵同行智能体，当前使用离线兜底回复。"
            if user_message:
                fallback_text += f" 你刚刚问的是：{user_message}"
            return {"reply": fallback_text, "model_used": target_model}

        short_term = request_data.get("short_term_memory", [])
        mid_term = request_data.get("mid_term_memory", [])
        long_term = request_data.get("long_term_memory", {})

        profile = long_term.get("user_profile", {}) if isinstance(long_term, dict) else {}
        culture_rules = long_term.get("culture_rules", []) if isinstance(long_term, dict) else []
        mid_term_json = json.dumps(mid_term, ensure_ascii=False)
        profile_json = json.dumps(profile, ensure_ascii=False)
        rules_text = "；".join(str(x) for x in culture_rules[:8])

        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "你是潮韵同行文旅智能体，请用简洁、友好的中文回答。"
                    "需要结合潮汕文旅场景给出可执行建议。"
                    "你将收到三层记忆："
                    "短期记忆（最近3轮原始对话，保留细节）、"
                    "中期记忆（已确认行程片段JSON）、"
                    "长期记忆（用户偏好与文化规则文档）。"
                    "回答时优先保持与三层记忆一致。"
                ),
            },
            {
                "role": "system",
                "content": (
                    f"[长期记忆-用户偏好]{profile_json}\n"
                    f"[长期记忆-文化规则]{rules_text}\n"
                    f"[中期记忆-已确认行程JSON]{mid_term_json}"
                ),
            },
        ]
        if isinstance(short_term, list):
            for item in short_term:
                if not isinstance(item, dict):
                    continue
                role = str(item.get("role", "")).strip()
                content = str(item.get("content", "")).strip()
                if role in {"user", "assistant", "system"} and content:
                    messages.append({"role": role, "content": content})

        user_message = str(request_data.get("message", "")).strip()
        if user_message:
            messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.4,
            )
            content = (response.choices[0].message.content or "").strip()
            if not content:
                content = "我已经收到你的问题，但暂时没有生成有效文本，请换一种问法试试。"
            return {"reply": content, "model_used": target_model}
        except Exception:
            return {
                "reply": "模型调用失败，已切换兜底回复。请稍后重试或更换模型。",
                "model_used": target_model,
            }

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
