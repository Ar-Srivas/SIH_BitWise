from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Hardcoded Student Dataset
students = [
    {"id": "DS07", "name": "Siddh Shah", "course": "Data Science", 
     "subjects": {"ML": 82, "AI": 78, "DSA": 75, "DBMS": 68, "Time Series": 90, "Cloud Computing": 85}},
]

# Updated Resource Dataset with generic YouTube links
resources = [
    # ML
    {"id": 1, "title": "ML Basics (Google Crash Course)", "subject": "ML", "difficulty": "Easy", "article_link": "https://developers.google.com/machine-learning/crash-course", "youtube_link": "https://www.youtube.com/results?search_query=machine+learning+basics"},
    {"id": 2, "title": "Machine Learning (Andrew Ng)", "subject": "ML", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/machine-learning", "youtube_link": "https://www.youtube.com/results?search_query=Andrew+Ng+machine+learning"},
    {"id": 3, "title": "Deep Learning Specialization", "subject": "ML", "difficulty": "Hard", "article_link": "https://www.coursera.org/specializations/deep-learning", "youtube_link": "https://www.youtube.com/results?search_query=deep+learning+specialization"},

    # AI
    {"id": 4, "title": "AI For Everyone (Andrew Ng)", "subject": "AI", "difficulty": "Easy", "article_link": "https://www.coursera.org/learn/ai-for-everyone", "youtube_link": "https://www.youtube.com/results?search_query=AI+for+everyone"},
    {"id": 5, "title": "edX Artificial Intelligence Courses", "subject": "AI", "difficulty": "Medium", "article_link": "https://www.edx.org/learn/artificial-intelligence", "youtube_link": "https://www.youtube.com/results?search_query=edx+artificial+intelligence"},
    {"id": 6, "title": "Stanford CS221 (AI)", "subject": "AI", "difficulty": "Hard", "article_link": "http://web.stanford.edu/class/cs221/", "youtube_link": "https://www.youtube.com/results?search_query=Stanford+CS221+AI"},

    # DSA
    {"id": 7, "title": "Data Structures (GeeksforGeeks)", "subject": "DSA", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/data-structures/", "youtube_link": "https://www.youtube.com/results?search_query=data+structures+geeksforgeeks"},
    {"id": 8, "title": "Visual Algorithm Explorer (VisuAlgo)", "subject": "DSA", "difficulty": "Medium", "article_link": "https://visualgo.net/en", "youtube_link": "https://www.youtube.com/results?search_query=Visualgo+algorithms"},
    {"id": 9, "title": "Algorithms, Sedgewick & Wayne (Algs4)", "subject": "DSA", "difficulty": "Hard", "article_link": "https://algs4.cs.princeton.edu/home/", "youtube_link": "https://www.youtube.com/results?search_query=Sedgewick+algorithms"},
    
    # DBMS
    {"id": 10, "title": "DBMS Overview (GeeksforGeeks)", "subject": "DBMS", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/what-is-dbms/", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+overview+geeksforgeeks"},
    {"id": 11, "title": "DBMS Tutorials (TutorialsPoint)", "subject": "DBMS", "difficulty": "Medium", "article_link": "https://www.tutorialspoint.com/dbms/index.htm", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+tutorials"},
    {"id": 12, "title": "Relational Databases & SQL (edX)", "subject": "DBMS", "difficulty": "Hard", "article_link": "https://www.edx.org/course/databases-5-sql", "youtube_link": "https://www.youtube.com/results?search_query=relational+databases+sql+edx"},

    # Time Series
    {"id": 13, "title": "Time Series Basics (Analytics Vidhya)", "subject": "Time Series", "difficulty": "Easy", "article_link": "https://www.analyticsvidhya.com/blog/2018/02/introduction-to-time-series-forecasting-with-python/", "youtube_link": "https://www.youtube.com/results?search_query=time+series+basics+analytics+vidhya"},
    {"id": 14, "title": "Time Series Analysis (Coursera)", "subject": "Time Series", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/practical-time-series-analysis", "youtube_link": "https://www.youtube.com/results?search_query=time+series+analysis+coursera"},
    {"id": 15, "title": "Forecasting: Principles and Practice (Book)", "subject": "Time Series", "difficulty": "Hard", "article_link": "https://otexts.com/fpp2/", "youtube_link": "https://www.youtube.com/results?search_query=forecasting+principles+and+practice"},

    # Cloud Computing
    {"id": 16, "title": "AWS Getting Started", "subject": "Cloud Computing", "difficulty": "Easy", "article_link": "https://aws.amazon.com/getting-started/", "youtube_link": "https://www.youtube.com/results?search_query=AWS+getting+started"},
    {"id": 17, "title": "Azure Fundamentals learning path", "subject": "Cloud Computing", "difficulty": "Medium", "article_link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "youtube_link": "https://www.youtube.com/results?search_query=Azure+fundamentals+learning+path"},
    {"id": 18, "title": "CNCF — Cloud Native Certified", "subject": "Cloud Computing", "difficulty": "Hard", "article_link": "https://www.cncf.io/certification/cka/", "youtube_link": "https://www.youtube.com/results?search_query=CNCF+cloud+native+certified"},
]

# Recommendation Logic
def recommend(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return []
    recs = []
    for subject, score in student["subjects"].items():
        if score < 70:
            recs.extend([r for r in resources if r["subject"] == subject and r["difficulty"] in ["Easy", "Medium"]])
        elif 70 <= score < 85:
            recs.extend([r for r in resources if r["subject"] == subject])
        else:
            recs.extend([r for r in resources if r["subject"] == subject and r["difficulty"] in ["Medium", "Hard"]])
    return recs

# Routes
@app.get("/", response_class=HTMLResponse)
async def select_subject_page(request: Request):
    return templates.TemplateResponse("select_subject.html", {"request": request})

@app.get("/recommend/{student_id}/{subject_name}", response_class=HTMLResponse)
async def get_recommendations_by_subject(request: Request, student_id: str, subject_name: str):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return HTMLResponse("Student not found.", status_code=404)
        
    all_recs = recommend(student_id)
    subject_recs = [rec for rec in all_recs if rec["subject"] == subject_name]
    
    return templates.TemplateResponse(
        "recommendations.html",
        {"request": request, "student": student, "recommendations": subject_recs, "selected_subject": subject_name}
    )