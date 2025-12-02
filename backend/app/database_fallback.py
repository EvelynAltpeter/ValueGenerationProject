"""
In-memory fallback database for demo purposes when MongoDB is not available
"""

from typing import Dict, List, Any


class InMemoryCollection:
    """Simulates MongoDB collection with in-memory storage"""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.counter = 0
    
    async def insert_one(self, document: Dict):
        """Insert a document"""
        doc_id = str(self.counter)
        self.counter += 1
        self.data[doc_id] = document
        return type('InsertResult', (), {'inserted_id': doc_id})()
    
    async def find_one(self, query: Dict):
        """Find one document matching query"""
        for doc in self.data.values():
            if self._matches(doc, query):
                return dict(doc)
        return None
    
    def find(self, query: Dict = None):
        """Find all documents matching query"""
        return InMemoryCursor(self.data, query or {})
    
    async def update_one(self, query: Dict, update: Dict, upsert: bool = False):
        """Update one document"""
        # Try to find existing document
        for doc_id, doc in self.data.items():
            if self._matches(doc, query):
                if '$set' in update:
                    doc.update(update['$set'])
                if '$addToSet' in update:
                    for key, value in update['$addToSet'].items():
                        if key not in doc:
                            doc[key] = []
                        # Handle both single values and lists
                        if isinstance(value, list):
                            for v in value:
                                if v not in doc[key]:
                                    doc[key].append(v)
                        elif value not in doc[key]:
                            doc[key].append(value)
                return
        
        if upsert:
            # Insert new document with $set values
            new_doc = {}
            # Include query fields that are not operators
            for key, value in query.items():
                if not key.startswith('$'):
                    new_doc[key] = value
            if '$set' in update:
                new_doc.update(update['$set'])
            if '$addToSet' in update:
                for key, value in update['$addToSet'].items():
                    if isinstance(value, list):
                        new_doc[key] = value
                    else:
                        new_doc[key] = [value]
            await self.insert_one(new_doc)
    
    async def count_documents(self, query: Dict):
        """Count documents matching query"""
        count = 0
        for doc in self.data.values():
            if self._matches(doc, query):
                count += 1
        return count
    
    async def create_index(self, *args, **kwargs):
        """No-op for in-memory"""
        pass
    
    def _matches(self, doc: Dict, query: Dict) -> bool:
        """Check if document matches query"""
        for key, value in query.items():
            if key.startswith('$'):
                # Handle special operators
                if key == '$in':
                    continue
                return True
            
            if key not in doc:
                return False
            
            if isinstance(value, dict):
                # Handle nested queries
                if '$in' in value:
                    if doc[key] not in value['$in']:
                        return False
                else:
                    return False
            elif isinstance(doc[key], list):
                # If field is a list, check if value is in the list
                if value not in doc[key]:
                    return False
            elif doc[key] != value:
                return False
        
        return True


class InMemoryCursor:
    """Simulates MongoDB cursor"""
    
    def __init__(self, data: Dict, query: Dict):
        self.results = [
            doc for doc in data.values()
            if self._matches(doc, query)
        ]
        self.index = 0
    
    def _matches(self, doc: Dict, query: Dict) -> bool:
        """Check if document matches query"""
        for key, value in query.items():
            if key.startswith('$'):
                continue
            
            if key not in doc:
                return False
            
            if isinstance(value, dict) and '$in' in value:
                if not isinstance(doc[key], list):
                    if doc[key] not in value['$in']:
                        return False
                else:
                    # Check if any value in doc[key] is in the $in list
                    if not any(v in value['$in'] for v in doc[key]):
                        return False
            elif isinstance(doc[key], list):
                # If field is a list, check if query value is in the list
                if value not in doc[key]:
                    return False
            elif doc[key] != value:
                return False
        
        return True
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.results):
            raise StopAsyncIteration
        result = self.results[self.index]
        self.index += 1
        return result


class InMemoryDatabase:
    """Simulates MongoDB database"""
    
    def __init__(self):
        self.collections: Dict[str, InMemoryCollection] = {}
    
    def __getattr__(self, name: str):
        """Get or create collection"""
        if name not in self.collections:
            self.collections[name] = InMemoryCollection()
        return self.collections[name]


class FallbackMongoDB:
    """Fallback MongoDB client using in-memory storage"""
    
    client = None
    database = InMemoryDatabase()
    
    @classmethod
    async def connect_db(cls):
        """Initialize in-memory database"""
        print("⚠️  MongoDB not detected - using in-memory storage for demo")
        print("✅ In-memory database initialized")
    
    @classmethod
    async def close_db(cls):
        """No-op for in-memory"""
        print("✅ In-memory database closed")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.database

