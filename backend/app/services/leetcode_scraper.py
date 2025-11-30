"""
LeetCode Problem Scraper
Scrapes problem statements, test cases, and metadata from LeetCode
R-LOG-01: All scraping operations are logged
"""

import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import json
from ..models.domain import QuestionMetadata, SkillTrack, DifficultyBand
from ..utils.trace_logger import log_event


class LeetCodeScraper:
    """
    Scraper for LeetCode problems using their public GraphQL API
    """
    
    LEETCODE_API = "https://leetcode.com/graphql"
    LEETCODE_PROBLEMS_API = "https://leetcode.com/api/problems/all/"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/json',
        })
    
    def get_all_problems(self) -> List[Dict]:
        """
        Fetch all problems from LeetCode
        Returns: List of problem metadata
        """
        try:
            log_event("leetcode_scraper", "scraper", {"action": "fetch_all_problems"})
            
            response = self.session.get(self.LEETCODE_PROBLEMS_API)
            response.raise_for_status()
            
            data = response.json()
            problems = data.get('stat_status_pairs', [])
            
            log_event("leetcode_scraper", "scraper", {
                "action": "fetch_complete",
                "count": str(len(problems))
            })
            
            return problems
        
        except Exception as e:
            log_event("leetcode_scraper", "scraper", {
                "action": "fetch_error",
                "error": str(e)
            })
            return []
    
    def get_problem_detail(self, title_slug: str) -> Optional[Dict]:
        """
        Fetch detailed problem information using GraphQL API
        """
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                content
                difficulty
                topicTags {
                    name
                }
                codeSnippets {
                    lang
                    code
                }
                sampleTestCase
                hints
            }
        }
        """
        
        try:
            payload = {
                "query": query,
                "variables": {"titleSlug": title_slug}
            }
            
            response = self.session.post(self.LEETCODE_API, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get('data', {}).get('question')
        
        except Exception as e:
            log_event("leetcode_scraper", "scraper", {
                "action": "fetch_detail_error",
                "titleSlug": title_slug,
                "error": str(e)
            })
            return None
    
    def map_to_skill_track(self, tags: List[str], title: str) -> SkillTrack:
        """
        Map LeetCode tags to our skill tracks with improved logic
        """
        tags_lower = [tag.lower() for tag in tags]
        title_lower = title.lower()
        
        # SQL track - database problems
        if any(tag in tags_lower for tag in ['database', 'sql']):
            return SkillTrack.sql_core_v1
        
        # JavaScript track - web/DOM/async focused
        if any(tag in tags_lower for tag in ['javascript', 'async', 'promise', 'closure']):
            return SkillTrack.javascript_core_v1
        
        # JavaScript track - also string manipulation, DOM-like problems
        if any(keyword in title_lower for keyword in ['string', 'array', 'valid', 'palindrome']):
            # Distribute between Python and JavaScript
            return SkillTrack.javascript_core_v1 if hash(title) % 2 == 0 else SkillTrack.python_core_v1
        
        # Python track - algorithms and data structures
        if any(tag in tags_lower for tag in ['dynamic-programming', 'tree', 'graph', 'backtracking', 
                                               'depth-first-search', 'breadth-first-search', 'binary-search']):
            return SkillTrack.python_core_v1
        
        # Default distribution for remaining problems
        hash_val = hash(title) % 3
        if hash_val == 0:
            return SkillTrack.python_core_v1
        elif hash_val == 1:
            return SkillTrack.javascript_core_v1
        else:
            return SkillTrack.python_core_v1  # Prefer Python for general problems
    
    def map_difficulty(self, difficulty: str) -> DifficultyBand:
        """
        Map LeetCode difficulty to our difficulty bands
        """
        difficulty_map = {
            'Easy': DifficultyBand.easy,
            'Medium': DifficultyBand.medium,
            'Hard': DifficultyBand.hard
        }
        return difficulty_map.get(difficulty, DifficultyBand.medium)
    
    def convert_to_question_metadata(self, problem_detail: Dict) -> Optional[QuestionMetadata]:
        """
        Convert LeetCode problem to our QuestionMetadata format
        """
        try:
            if not problem_detail:
                return None
            
            tags = [tag['name'] for tag in problem_detail.get('topicTags', [])]
            title = problem_detail.get('title', '')
            track_id = self.map_to_skill_track(tags, title)
            difficulty = self.map_difficulty(problem_detail.get('difficulty', 'Medium'))
            
            # Extract Python code snippet if available
            code_snippets = problem_detail.get('codeSnippets', [])
            python_snippet = next(
                (snippet['code'] for snippet in code_snippets if snippet['lang'] == 'Python3'),
                None
            )
            
            # Determine subskill from first tag
            subskill = tags[0] if tags else "general"
            
            question = QuestionMetadata(
                questionId=f"lc_{problem_detail['questionId']}",
                trackId=track_id,
                prompt=self._clean_html(problem_detail.get('content', '')),
                questionType="coding",
                difficulty=difficulty,
                tags=tags,
                subskill=subskill,
                referenceSolution=python_snippet,
                timeLimitSeconds=600  # 10 minutes per problem
            )
            
            return question
        
        except Exception as e:
            log_event("leetcode_scraper", "scraper", {
                "action": "conversion_error",
                "error": str(e)
            })
            return None
    
    def _clean_html(self, html_content: str) -> str:
        """
        Clean HTML tags from problem description
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    
    async def scrape_and_store(self, limit: int = 50) -> int:
        """
        Scrape problems from LeetCode and store in database
        Returns: Number of problems successfully stored
        """
        from ..database import get_item_bank_collection
        
        problems = self.get_all_problems()[:limit]
        stored_count = 0
        
        collection = get_item_bank_collection()
        
        for problem in problems:
            title_slug = problem['stat']['question__title_slug']
            
            # Check if already exists
            existing = await collection.find_one({"questionId": f"lc_{problem['stat']['question_id']}"})
            if existing:
                continue
            
            # Fetch detailed problem info
            detail = self.get_problem_detail(title_slug)
            if not detail:
                continue
            
            # Convert to our format
            question = self.convert_to_question_metadata(detail)
            if not question:
                continue
            
            # Store in database
            try:
                await collection.insert_one(question.model_dump())
                stored_count += 1
                log_event("leetcode_scraper", "scraper", {
                    "action": "problem_stored",
                    "questionId": question.questionId,
                    "title": detail['title']
                })
            except Exception as e:
                log_event("leetcode_scraper", "scraper", {
                    "action": "storage_error",
                    "questionId": question.questionId,
                    "error": str(e)
                })
        
        return stored_count

