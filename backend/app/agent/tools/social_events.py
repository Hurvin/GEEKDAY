from __future__ import annotations

import random
from datetime import datetime, timedelta

# 模拟的社交媒体活动数据库
# 在真实场景中，这里的数据会来自爬虫或搜索引擎 API
MOCK_SOCIAL_EVENTS = [
    {
        "title": "甲子英歌舞巡游",
        "type": "民俗",
        "location": "潮阳区文光塔广场",
        "time_desc": "本周六下午 14:00 - 16:00",
        "source": "小红书 @潮汕摄影阿光",
        "url": "https://xiaohongshu.com/...",
        "tags": ["英歌舞", "热血", "摄影"],
        "desc": "据博主爆料，这周六会有三支英歌队在文光塔斗舞，场面非常震撼，建议提前一小时去占位！"
    },
    {
        "title": "广济桥光影秀（特别版）",
        "type": "演出",
        "location": "潮州广济桥",
        "time_desc": "每晚 20:00 / 21:00 各一场",
        "source": "公众号 [潮州发布]",
        "url": "https://weixin.qq.com/...",
        "tags": ["夜景", "灯光秀"],
        "desc": "官方发布通知，本周灯光秀增加了无人机表演环节，最佳观赏点在滨江长廊。"
    },
    {
        "title": "龙湖古寨非遗市集",
        "type": "市集",
        "location": "龙湖古寨直街",
        "time_desc": "本周末全天",
        "source": "抖音 @吃喝玩乐在潮州",
        "url": "https://douyin.com/...",
        "tags": ["美食", "手工艺", "非遗"],
        "desc": "视频里看到有很多老手艺人出摊，有糖画、麦秆画，还有现做的潮州春卷！"
    },
    {
        "title": "汕头小公园复古舞会",
        "type": "活动",
        "location": "小公园中山纪念亭",
        "time_desc": "周五晚 19:30",
        "source": "朋友圈热传",
        "url": "",
        "tags": ["复古", "社交"],
        "desc": "一群年轻人自发组织的摇摆舞会，穿复古装可以免费领一杯手打柠檬茶。"
    }
]

def search_social_events(destination: str, days: int = 1) -> list[dict]:
    """
    模拟搜索社交媒体上的本地活动
    """
    # 简单过滤，实际场景可以用向量搜索或关键词匹配
    # 这里为了演示，随机返回 1-2 个活动，假装是“刚刚”发现的
    
    # 模拟网络延迟
    # time.sleep(0.5) 
    
    # 随机选择 2 个活动返回
    events = random.sample(MOCK_SOCIAL_EVENTS, 2)
    return events
