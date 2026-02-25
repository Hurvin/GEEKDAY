# Chaoyun Yunnao Backend

FastAPI + LangGraph + MCP Server backend for MVP.

## Fake 事件联调

用于快速触发前端天气/人流量弹窗：

```bash
python scripts/fake_event_cli.py --type weather --destination 潮州 --day 1 --old 晴朗 --new 雷阵雨
python scripts/fake_event_cli.py --type crowd --destination 汕头 --day 2 --old 中 --new 高
```
