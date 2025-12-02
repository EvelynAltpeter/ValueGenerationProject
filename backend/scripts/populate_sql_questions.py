"""
Populate SQL questions for SQL Core track
LeetCode SQL problems may not be available through the API, so we create sample ones
"""

import asyncio
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))

from app.database import MongoDB, get_item_bank_collection
from app.models.domain import QuestionMetadata, SkillTrack, DifficultyBand


SQL_QUESTIONS = [
    {
        "questionId": "sql_001",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Given a table 'Employees' with columns (id, name, department, salary), write a SQL query to find employees earning more than $80,000.

Table: Employees
+----+--------+------------+--------+
| id | name   | department | salary |
+----+--------+------------+--------+
| 1  | John   | IT         | 75000  |
| 2  | Jane   | HR         | 85000  |
| 3  | Bob    | IT         | 95000  |
+----+--------+------------+--------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.easy,
        "tags": ["database", "sql", "select", "where"],
        "subskill": "data_structures",
        "referenceSolution": "SELECT * FROM Employees WHERE salary > 80000;",
        "timeLimitSeconds": 300
    },
    {
        "questionId": "sql_002",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find the second highest salary from the Employees table.

Table: Employees
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.medium,
        "tags": ["database", "sql", "subquery", "limit"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT MAX(salary) AS SecondHighestSalary FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_003",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find duplicate emails in the Person table.

Table: Person
+----+--------+
| id | email  |
+----+--------+
| 1  | a@b.com|
| 2  | c@d.com|
| 3  | a@b.com|
+----+--------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.easy,
        "tags": ["database", "sql", "group-by", "having"],
        "subskill": "data_structures",
        "referenceSolution": "SELECT email FROM Person GROUP BY email HAVING COUNT(email) > 1;",
        "timeLimitSeconds": 300
    },
    {
        "questionId": "sql_004",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to rank scores in descending order. If two scores are the same, they should have the same ranking.

Table: Scores
+----+-------+
| id | score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
+----+-------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.medium,
        "tags": ["database", "sql", "window-function", "rank"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank FROM Scores;",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_005",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find customers who never order anything.

Table: Customers
+----+-------+
| id | name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+

Table: Orders
+----+------------+
| id | customerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.easy,
        "tags": ["database", "sql", "left-join", "null"],
        "subskill": "data_structures",
        "referenceSolution": "SELECT name AS Customers FROM Customers LEFT JOIN Orders ON Customers.id = Orders.customerId WHERE Orders.id IS NULL;",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_006",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to get the nth highest salary from the Employee table.

Table: Employee
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+

Find the 2nd highest salary.""",
        "questionType": "coding",
        "difficulty": DifficultyBand.hard,
        "tags": ["database", "sql", "offset", "limit"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET 1;",
        "timeLimitSeconds": 500
    },
    {
        "questionId": "sql_007",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find employees who earn more than their managers.

Table: Employee
+----+-------+--------+-----------+
| id | name  | salary | managerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | NULL      |
| 4  | Max   | 90000  | NULL      |
+----+-------+--------+-----------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.medium,
        "tags": ["database", "sql", "self-join"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT e1.name AS Employee FROM Employee e1 JOIN Employee e2 ON e1.managerId = e2.id WHERE e1.salary > e2.salary;",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_008",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to delete duplicate emails, keeping only the one with the smallest id.

Table: Person
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.easy,
        "tags": ["database", "sql", "delete", "group-by"],
        "subskill": "data_structures",
        "referenceSolution": "DELETE p1 FROM Person p1 JOIN Person p2 WHERE p1.email = p2.email AND p1.id > p2.id;",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_009",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find the department with the highest average salary.

Table: Employee
+----+--------+------------+--------+
| id | name   | department | salary |
+----+--------+------------+--------+
| 1  | Joe    | IT         | 85000  |
| 2  | Jim    | Sales      | 90000  |
| 3  | Henry  | IT         | 80000  |
| 4  | Sam    | Sales      | 95000  |
+----+--------+------------+--------+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.medium,
        "tags": ["database", "sql", "aggregate", "group-by"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT department, AVG(salary) as avg_salary FROM Employee GROUP BY department ORDER BY avg_salary DESC LIMIT 1;",
        "timeLimitSeconds": 400
    },
    {
        "questionId": "sql_010",
        "trackId": SkillTrack.sql_core_v1,
        "prompt": """Write a SQL query to find consecutive numbers that appear at least three times consecutively.

Table: Logs
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
+----+-----+""",
        "questionType": "coding",
        "difficulty": DifficultyBand.hard,
        "tags": ["database", "sql", "window-function", "advanced"],
        "subskill": "algorithms",
        "referenceSolution": "SELECT DISTINCT l1.num AS ConsecutiveNums FROM Logs l1 JOIN Logs l2 ON l1.id = l2.id - 1 JOIN Logs l3 ON l1.id = l3.id - 2 WHERE l1.num = l2.num AND l2.num = l3.num;",
        "timeLimitSeconds": 600
    }
]


async def populate_sql_questions():
    """Add SQL questions to the database"""
    print("🚀 Connecting to MongoDB...")
    await MongoDB.connect_db()
    
    collection = get_item_bank_collection()
    added_count = 0
    
    for q_data in SQL_QUESTIONS:
        # Check if already exists
        existing = await collection.find_one({"questionId": q_data["questionId"]})
        if existing:
            print(f"⏭️  Skipping {q_data['questionId']} (already exists)")
            continue
        
        # Create question object
        question = QuestionMetadata(**q_data)
        
        # Insert into database
        await collection.insert_one(question.model_dump())
        added_count += 1
        print(f"✅ Added {q_data['questionId']}: {q_data['prompt'][:50]}...")
    
    print(f"\n✨ Successfully added {added_count} SQL questions!")
    print(f"📊 Total SQL questions now in database")
    
    # Show stats
    total_sql = await collection.count_documents({"trackId": "sql_core_v1"})
    print(f"   SQL Core: {total_sql} questions")
    
    await MongoDB.close_db()


if __name__ == "__main__":
    asyncio.run(populate_sql_questions())

