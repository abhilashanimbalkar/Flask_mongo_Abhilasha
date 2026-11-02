# Flask + MongoDB Atlas

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and put in your Atlas connection string
   (Atlas: Database > Connect > Drivers; also add your IP under Network Access).
3. `python Abhilasha.py` and open http://127.0.0.1:5000

## Routes
- `GET /api` - returns the JSON list read from `data.json`
- `GET/POST /` - form; inserts into MongoDB Atlas
  - success: redirects to `/success` ("Data submitted successfully")
  - error: re-renders the same page with the error message (no redirect)
- `GET /success` - success page
