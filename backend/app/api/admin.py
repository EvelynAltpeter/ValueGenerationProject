"""
Admin API Endpoints
For managing item bank, scraping, and system maintenance
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.leetcode_scraper import LeetCodeScraper
from ..utils.api import envelope

router = APIRouter(prefix="/api/admin", tags=["admin"])


class ScrapeRequest(BaseModel):
    limit: int = 50


@router.post("/scrape-leetcode")
async def scrape_leetcode(request: ScrapeRequest):
    """
    Scrape problems from LeetCode and store in database
    R-LOG-01: All scraping operations logged
    """
    try:
        scraper = LeetCodeScraper()
        count = await scraper.scrape_and_store(limit=request.limit)
        return envelope({
            "status": "success",
            "problemsStored": count,
            "message": f"Successfully scraped and stored {count} problems"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.get("/item-bank-stats")
async def item_bank_stats():
    """Get statistics about the item bank"""
    from ..database import get_item_bank_collection
    
    collection = get_item_bank_collection()
    
    total_count = await collection.count_documents({})
    
    # Count by track
    python_count = await collection.count_documents({"trackId": "python_core_v1"})
    sql_count = await collection.count_documents({"trackId": "sql_core_v1"})
    js_count = await collection.count_documents({"trackId": "javascript_core_v1"})
    
    # Count by difficulty
    easy_count = await collection.count_documents({"difficulty": "easy"})
    medium_count = await collection.count_documents({"difficulty": "medium"})
    hard_count = await collection.count_documents({"difficulty": "hard"})
    
    return envelope({
        "total": total_count,
        "byTrack": {
            "python_core_v1": python_count,
            "sql_core_v1": sql_count,
            "javascript_core_v1": js_count
        },
        "byDifficulty": {
            "easy": easy_count,
            "medium": medium_count,
            "hard": hard_count
        }
    })

