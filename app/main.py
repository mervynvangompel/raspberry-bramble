# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="Dog Feeding Tracker")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("DB_NAME", "dogfeeding"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        cursor_factory=RealDictCursor
    )

# Pydantic models
class Feeding(BaseModel):
    cups: float
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class FeedingResponse(BaseModel):
    id: int
    cups: float
    notes: Optional[str]
    timestamp: datetime

# Initialize database
@app.on_event("startup")
def startup():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedings (
            id SERIAL PRIMARY KEY,
            cups DECIMAL(4,2) NOT NULL,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Endpoints
@app.post("/feedings", response_model=FeedingResponse)
def create_feeding(feeding: Feeding):
    conn = get_db_connection()
    cur = conn.cursor()
    
    timestamp = feeding.timestamp or datetime.now()
    
    cur.execute(
        "INSERT INTO feedings (cups, notes, timestamp) VALUES (%s, %s, %s) RETURNING *",
        (feeding.cups, feeding.notes, timestamp)
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return result

@app.get("/feedings", response_model=List[FeedingResponse])
def get_feedings(limit: int = 50):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT * FROM feedings ORDER BY timestamp DESC LIMIT %s",
        (limit,)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results

@app.get("/feedings/stats")
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            DATE(timestamp) as date,
            SUM(cups) as total_cups,
            COUNT(*) as feeding_count
        FROM feedings
        WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"stats": results}

@app.get("/health")
def health():
    return {"status": "healthy"}
