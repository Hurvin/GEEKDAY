from __future__ import annotations

import argparse
import json
from urllib import request as urlrequest



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="向后端注入 fake 天气/人流变化事件")
    parser.add_argument("--api", default="http://localhost:8000/api/v1", help="后端 API 根地址")
    parser.add_argument("--type", choices=["weather", "crowd"], help="事件类型")
    parser.add_argument("--destination", default="潮州", help="目的地")
    parser.add_argument("--day", type=int, default=1, help="第几天")
    parser.add_argument("--old", dest="old_value", default="", help="变化前")
    parser.add_argument("--new", dest="new_value", default="", help="变化后")
    parser.add_argument("--note", default="", help="备注")
    return parser.parse_args()


def prompt_if_empty(value: str | None, prompt: str, default: str = "") -> str:
    if value:
        return value
    user_input = input(f"{prompt}{f'（默认 {default}）' if default else ''}: ").strip()
    return user_input or default


def main() -> None:
    args = parse_args()

    event_type = args.type or prompt_if_empty(None, "输入事件类型 weather/crowd", "weather")
    destination = prompt_if_empty(args.destination, "输入目的地", "潮州")
    day_index = args.day

    if not args.old_value:
        args.old_value = prompt_if_empty(None, "输入变化前值", "晴朗" if event_type == "weather" else "中")
    if not args.new_value:
        args.new_value = prompt_if_empty(None, "输入变化后值", "雷阵雨" if event_type == "weather" else "高")
    if not args.note:
        args.note = prompt_if_empty(None, "输入备注", "命令行模拟变更")

    payload = {
        "event_type": event_type,
        "destination": destination,
        "day_index": day_index,
        "old_value": args.old_value,
        "new_value": args.new_value,
        "note": args.note,
    }

    url = f"{args.api}/fake/events"
    req = urlrequest.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    print("✅ 已注入 fake 事件:")
    print(data)


if __name__ == "__main__":
    main()
