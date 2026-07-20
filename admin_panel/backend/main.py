from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import os

app = FastAPI(title="ALL-IN-One-IPTV Admin Panel")

# Secret Configuration (In production, load from environment)
SECRET_KEY = os.environ.get("ENV_PLAYLIST_KEY", "supersecretadminpass")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Mock Database ---
users_db = {
    "admin": {"username": "admin", "password": "password123", "role": "admin"}
}
m3u_tokens = {} # Store mapping of Token -> User Config (Allowed Countries, etc.)

# --- Models ---
class UserConfig(BaseModel):
    username: str
    allowed_countries: list[str]

# --- Routes ---

@app.get("/")
def read_root():
    return {"status": "Admin API Online"}

@app.post("/api/auth/login")
def login(username: str):
    # Simplified login for blueprint
    if username not in users_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
        
    access_token_expires = timedelta(hours=24)
    expire = datetime.utcnow() + access_token_expires
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": encoded_jwt, "token_type": "bearer"}

@app.post("/api/admin/generate_playlist_token")
def generate_token(config: UserConfig, token: str = Depends(oauth2_scheme)):
    # Verify Admin (RBAC Mock)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    # Generate unique playlist access token for this user
    import uuid
    unique_token = str(uuid.uuid4())
    m3u_tokens[unique_token] = config.dict()
    
    return {"playlist_url": f"http://YOUR_SERVER_IP:8000/api/playlist/{unique_token}.m3u"}

@app.get("/api/playlist/{token}.m3u")
def serve_user_playlist(token: str):
    if token not in m3u_tokens:
        raise HTTPException(status_code=404, detail="Invalid or Revoked Token")
        
    user_config = m3u_tokens[token]
    
    # In production, read output/checked_combined_by_country.m3u 
    # and filter ONLY the countries specified in user_config['allowed_countries']
    
    return f"#EXTM3U\n#EXTINF:-1,Welcome {user_config['username']}\nhttp://dummy/stream.ts"

@app.get("/api/telemetry/health")
def get_scraper_health():
    # Provide real-time data for the Next.js Dashboard
    return {
        "active_streams": 1450,
        "dead_links_dropped": 320,
        "last_sync": "10 minutes ago"
    }
