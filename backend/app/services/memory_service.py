from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.agent.tools.mock_data import CHAOSHAN_CULTURE_RULES

MEMORY_DIR = Path(__file__).resolve().parents[1] / "memory"
LONG_TERM_PATH = MEMORY_DIR / "long_term_memory.json"
LONG_TERM_MD_PATH = MEMORY_DIR / "long_term_memory.md"
MID_TERM_PATH = MEMORY_DIR / "mid_term_memory.json"


def _ensure_memory_dir() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _sync_long_term_markdown(data: dict[str, Any]) -> None:
    profiles = data.get("user_profiles", {})
    rules = data.get("culture_rules", [])
    lines: list[str] = [
        "# Long Term Memory",
        "",
        "## User Profiles",
    ]
    for user_id, profile in profiles.items():
        lines.extend(
            [
                f"### {user_id}",
                f"- departure_city: {profile.get('departure_city', '')}",
                f"- home_city: {profile.get('home_city', '')}",
                f"- preferences: {', '.join(profile.get('preferences', []))}",
                f"- food_preferences: {', '.join(profile.get('food_preferences', []))}",
                f"- budget_level: {profile.get('budget_level', '')}",
                f"- note: {profile.get('note', '')}",
                "",
            ]
        )
    lines.extend(["## Culture Rules"])
    for rule in rules:
        lines.append(f"- {rule}")
    LONG_TERM_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def init_long_term_memory() -> dict[str, Any]:
    _ensure_memory_dir()
    default = {
        "user_profiles": {},
        "culture_rules": CHAOSHAN_CULTURE_RULES,
        "updated_at": _now_iso(),
    }
    data = _load_json(LONG_TERM_PATH, default)
    if "culture_rules" not in data:
        data["culture_rules"] = CHAOSHAN_CULTURE_RULES
    _save_json(LONG_TERM_PATH, data)
    _sync_long_term_markdown(data)
    return data


def get_long_term_context(user_id: str) -> dict[str, Any]:
    data = init_long_term_memory()
    profile = data.get("user_profiles", {}).get(user_id, {})
    return {
        "user_profile": profile,
        "culture_rules": data.get("culture_rules", []),
    }


def update_user_profile(user_id: str, profile_data: dict[str, Any]) -> dict[str, Any]:
    data = init_long_term_memory()
    profiles = data.setdefault("user_profiles", {})
    current = profiles.get(user_id, {})
    merged = {
        "departure_city": profile_data.get("departure_city") or current.get("departure_city", ""),
        "home_city": profile_data.get("home_city") or current.get("home_city", ""),
        "preferences": profile_data.get("preferences") or current.get("preferences", []),
        "food_preferences": profile_data.get("food_preferences") or current.get("food_preferences", []),
        "budget_level": profile_data.get("budget_level") or current.get("budget_level", ""),
        "note": profile_data.get("note") or current.get("note", ""),
        "updated_at": _now_iso(),
    }
    profiles[user_id] = merged
    data["updated_at"] = _now_iso()
    _save_json(LONG_TERM_PATH, data)
    _sync_long_term_markdown(data)
    return merged


def get_short_term_memory(history: list[dict[str, Any]], max_rounds: int = 3) -> list[dict[str, str]]:
    if not history:
        return []
    user_count = 0
    start_idx = 0
    for idx in range(len(history) - 1, -1, -1):
        if str(history[idx].get("role", "")).strip() == "user":
            user_count += 1
            if user_count == max_rounds:
                start_idx = idx
                break
    sliced = history[start_idx:]
    output: list[dict[str, str]] = []
    for item in sliced:
        role = str(item.get("role", "")).strip()
        content = str(item.get("content", "")).strip()
        if role in {"user", "assistant", "system"} and content:
            output.append({"role": role, "content": content})
    return output


def _is_confirmation_text(text: str) -> bool:
    confirm_words = ["确认", "就按这个", "按这个来", "就这样", "可以", "没问题", "确定", "采纳", "安排吧"]
    value = text.strip()
    return any(word in value for word in confirm_words)


def _extract_structured_itinerary(text: str) -> dict[str, Any]:
    day = None
    period = ""
    for i in range(1, 8):
        if f"第{i}天" in text or f"D{i}" in text:
            day = i
            break
    for p in ["上午", "中午", "下午", "晚上", "全天"]:
        if p in text:
            period = p
            break
    return {
        "day": day,
        "period": period or "未指定",
        "activity": text[:140],
    }


def append_mid_term_if_confirmed(
    user_id: str,
    user_message: str,
    assistant_reply: str,
) -> dict[str, Any] | None:
    if not _is_confirmation_text(user_message):
        return None
    _ensure_memory_dir()
    default = {"users": {}, "updated_at": _now_iso()}
    data = _load_json(MID_TERM_PATH, default)
    users = data.setdefault("users", {})
    entries = users.setdefault(user_id, [])
    structured = _extract_structured_itinerary(assistant_reply)
    snippet = {
        "confirmed_at": _now_iso(),
        "confirmation_message": user_message[:120],
        "assistant_reply_excerpt": assistant_reply[:220],
        "structured_itinerary": structured,
    }
    entries.append(snippet)
    users[user_id] = entries[-20:]
    data["updated_at"] = _now_iso()
    _save_json(MID_TERM_PATH, data)
    return snippet


def get_mid_term_memory(user_id: str, limit: int = 8) -> list[dict[str, Any]]:
    _ensure_memory_dir()
    default = {"users": {}, "updated_at": _now_iso()}
    data = _load_json(MID_TERM_PATH, default)
    users = data.get("users", {})
    entries = users.get(user_id, [])
    return entries[-limit:]
