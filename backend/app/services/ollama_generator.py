"""
Ollama Question Generator Service
Generates questions for Python, SQL, and JavaScript tracks using Ollama
"""

import json
import httpx
from typing import List, Dict, Any
from ..models.domain import DifficultyBand, SkillTrack


OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.1:8b"  # Change to any model you have


class OllamaGenerator:
    """Generate test questions using Ollama"""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.base_url = OLLAMA_BASE_URL
    
    async def generate_question(
        self,
        track: SkillTrack,
        difficulty: DifficultyBand,
        question_type: str = "mcq"
    ) -> Dict[str, Any]:
        """Generate a single question using Ollama"""
        
        track_name = {
            SkillTrack.python_core_v1: "Python",
            SkillTrack.sql_core_v1: "SQL",
            SkillTrack.javascript_core_v1: "JavaScript"
        }.get(track, "Python")
        
        difficulty_desc = {
            DifficultyBand.easy: "easy (basic concepts, simple syntax)",
            DifficultyBand.medium: "medium (intermediate concepts, moderate complexity)",
            DifficultyBand.hard: "hard (advanced concepts, complex problem-solving)"
        }.get(difficulty, "medium")
        
        subskill = {
            DifficultyBand.easy: "data_structures",
            DifficultyBand.medium: "algorithms",
            DifficultyBand.hard: "code_quality"
        }.get(difficulty, "algorithms")
        
        if question_type == "mcq":
            prompt = f"""Generate a {difficulty_desc} multiple-choice question about {track_name} programming.

Requirements:
- The question should test practical {track_name} knowledge
- Include 4 answer options (only one correct)
- Focus on: {subskill}
- Make it realistic and useful for assessing programming proficiency

Respond with a valid JSON object in this exact format:
{{
  "prompt": "the question text",
  "options": ["option1", "option2", "option3", "option4"],
  "answerKey": "the correct option text (must match one of the options exactly)",
  "tags": ["relevant", "tags"],
  "timeLimitSeconds": 120
}}"""
        else:  # coding
            prompt = f"""Generate a {difficulty_desc} coding problem about {track_name} programming.

Requirements:
- The problem should require writing actual {track_name} code
- It should be solvable in 10-15 minutes
- Focus on: {subskill}
- Provide a clear problem description
- Include a reference solution

Respond with a valid JSON object in this exact format:
{{
  "prompt": "the problem description with clear requirements",
  "referenceSolution": "complete working code solution",
  "tags": ["relevant", "tags"],
  "timeLimitSeconds": 600
}}"""
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract the generated text
                generated_text = result.get("response", "")
                
                # Parse JSON from the response
                # Sometimes Ollama returns markdown code blocks, so we need to extract JSON
                if "```json" in generated_text:
                    start = generated_text.find("```json") + 7
                    end = generated_text.find("```", start)
                    generated_text = generated_text[start:end].strip()
                elif "```" in generated_text:
                    start = generated_text.find("```") + 3
                    end = generated_text.find("```", start)
                    generated_text = generated_text[start:end].strip()
                
                question_data = json.loads(generated_text)
                
                # Build the complete question metadata
                question_id_prefix = {
                    SkillTrack.python_core_v1: "py",
                    SkillTrack.sql_core_v1: "sql",
                    SkillTrack.javascript_core_v1: "js"
                }.get(track, "py")
                
                # Generate a unique ID (in production, use better ID generation)
                import hashlib
                prompt_hash = hashlib.md5(question_data["prompt"].encode()).hexdigest()[:8]
                question_id = f"{question_id_prefix}-{difficulty.value}-{prompt_hash}"
                
                question_metadata = {
                    "questionId": question_id,
                    "trackId": track.value,
                    "prompt": question_data["prompt"],
                    "questionType": question_type,
                    "difficulty": difficulty.value,
                    "tags": question_data.get("tags", []),
                    "subskill": subskill,
                    "timeLimitSeconds": question_data.get("timeLimitSeconds", 120 if question_type == "mcq" else 600)
                }
                
                if question_type == "mcq":
                    question_metadata["options"] = question_data.get("options", [])
                    question_metadata["answerKey"] = question_data.get("answerKey", "")
                else:
                    question_metadata["referenceSolution"] = question_data.get("referenceSolution", "")
                
                return question_metadata
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from Ollama response: {e}")
            print(f"Response was: {generated_text[:500]}")
            raise
        except Exception as e:
            print(f"Error generating question with Ollama: {e}")
            raise
    
    async def generate_question_set(
        self,
        track: SkillTrack,
        questions_per_difficulty: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate a set of questions for a track"""
        questions = []
        
        difficulties = [DifficultyBand.easy, DifficultyBand.medium, DifficultyBand.hard]
        
        for difficulty in difficulties:
            # Generate MCQ questions
            for i in range(questions_per_difficulty):
                try:
                    question = await self.generate_question(track, difficulty, "mcq")
                    questions.append(question)
                    print(f"Generated {track.value} {difficulty.value} MCQ #{i+1}")
                except Exception as e:
                    print(f"Failed to generate question: {e}")
                    continue
            
            # Generate 1-2 coding questions per difficulty
            coding_count = 2 if difficulty == DifficultyBand.hard else 1
            for i in range(coding_count):
                try:
                    question = await self.generate_question(track, difficulty, "coding")
                    questions.append(question)
                    print(f"Generated {track.value} {difficulty.value} Coding #{i+1}")
                except Exception as e:
                    print(f"Failed to generate coding question: {e}")
                    continue
        
        return questions

