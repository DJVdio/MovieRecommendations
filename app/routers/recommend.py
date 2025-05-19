import re
import json
import random
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models import DoubanTop250, DoubanOneWeek
from ..services.silicon_flow import call_ai

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("", summary="智能推荐电影")
async def recommend_movie(
    query: str = Body(..., embed=True, description="如：'恐怖片'或'本周高分'"),
    db: AsyncSession = Depends(get_db)
):
    # 1. 拉取所有未观看电影
    top_movies = (await db.execute(
        select(DoubanTop250).where(DoubanTop250.is_watched == False)
    )).scalars().all()
    week_movies = (await db.execute(
        select(DoubanOneWeek).where(DoubanOneWeek.is_watched == False)
    )).scalars().all()

    candidates = [
        {"id": m.id, "title": m.title, "source": "top250", "rating": m.rating}
        for m in top_movies
    ] + [
        {"id": m.id, "title": m.title, "source": "one_week", "rating": m.rating}
        for m in week_movies
    ]

    if not candidates:
        return {"message": "没有可推荐的电影，请先抓取或新增数据。"}

    # 2. 构造 AI prompt，示例取前 10 条
    sample = json.dumps(candidates[:10], ensure_ascii=False, indent=2)
    ai_prompt = f"""
请基于以下“用户需求”+“候选电影列表”严格推荐一部最符合要求的电影：
one_week是近一周的电影榜单。
top250是豆瓣电影TOP250榜单。
用户需求：{query}

候选电影示例（最多10条）：
{sample}

请只返回一个 JSON 对象，格式如下：
{{
  "id": <数字>,
  "title": "<电影名称>",
  "source": "top250" 或 "one_week"
}}
"""

    # 3. 调用 AI
    try:
        response = await call_ai(ai_prompt)
    except Exception as e:
        # 降级：选最高评分
        backup = max(candidates, key=lambda x: x["rating"])
        return {
            "recommendation": {
                "id": backup["id"],
                "title": backup["title"],
                "source": backup["source"],
                "reason": f"AI服务异常，已降级使用最高评分: {str(e)}"
            }
        }

    # 4. 解析 AI 返回
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if not match:
        raise HTTPException(500, f"AI没有返回有效的JSON，原文：{content[:200]}")
    try:
        result = json.loads(match.group())
    except json.JSONDecodeError:
        raise HTTPException(500, f"解析AI返回JSON失败，原文：{match.group()}")


    return {
        "recommendation": {
            "id": result["id"],
            "title": result["title"],
            "source": result["source"],
            "reason": "AI智能推荐"
        }
    }