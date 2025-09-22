# recommend_controller.py
import random
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

# NOTE: The templates instance will be passed from the router
# Static resources list is fine, no need to change
resources = [
    {"id": 1, "title": "ML Basics (Google Crash Course)", "subject": "ML", "difficulty": "Easy", "article_link": "https://developers.google.com/machine-learning/crash-course", "youtube_link": "https://www.youtube.com/results?search_query=machine+learning+basics"},
    {"id": 2, "title": "Machine Learning (Andrew Ng)", "subject": "ML", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/machine-learning", "youtube_link": "https://www.youtube.com/results?search_query=Andrew+Ng+machine+learning"},
    {"id": 3, "title": "Deep Learning Specialization", "subject": "ML", "difficulty": "Hard", "article_link": "https://www.coursera.org/specializations/deep-learning", "youtube_link": "https://www.youtube.com/results?search_query=deep+learning+specialization"},
    {"id": 4, "title": "AI For Everyone (Andrew Ng)", "subject": "AI", "difficulty": "Easy", "article_link": "https://www.coursera.org/learn/ai-for-everyone", "youtube_link": "https://www.youtube.com/results?search_query=AI+for+everyone"},
    {"id": 5, "title": "edX Artificial Intelligence Courses", "subject": "AI", "difficulty": "Medium", "article_link": "https://www.edx.org/learn/artificial-intelligence", "youtube_link": "https://www.youtube.com/results?search_query=edx+artificial+intelligence"},
    {"id": 6, "title": "Stanford CS221 (AI)", "subject": "AI", "difficulty": "Hard", "article_link": "http://web.stanford.edu/class/cs221/", "youtube_link": "https://www.youtube.com/results?search_query=Stanford+CS221+AI"},
    {"id": 7, "title": "Data Structures (GeeksforGeeks)", "subject": "DSA", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/data-structures/", "youtube_link": "https://www.youtube.com/results?search_query=data+structures+geeksforgeeks"},
    {"id": 8, "title": "Visual Algorithm Explorer (VisuAlgo)", "subject": "DSA", "difficulty": "Medium", "article_link": "https://visualgo.net/en", "youtube_link": "https://www.youtube.com/results?search_query=Visualgo+algorithms"},
    {"id": 9, "title": "Algorithms, Sedgewick & Wayne (Algs4)", "subject": "DSA", "difficulty": "Hard", "article_link": "https://algs4.cs.princeton.edu/home/", "youtube_link": "https://www.youtube.com/results?search_query=Sedgewick+algorithms"},
    {"id": 10, "title": "DBMS Overview (GeeksforGeeks)", "subject": "DBMS", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/what-is-dbms/", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+overview+geeksforgeeks"},
    {"id": 11, "title": "DBMS Tutorials (TutorialsPoint)", "subject": "DBMS", "difficulty": "Medium", "article_link": "https://www.tutorialspoint.com/dbms/index.htm", "youtube_link": "https://www.youtube.com/results?search_query=DBMS+tutorials"},
    {"id": 12, "title": "Relational Databases & SQL (edX)", "subject": "DBMS", "difficulty": "Hard", "article_link": "https://www.edx.org/course/databases-5-sql", "youtube_link": "https://www.youtube.com/results?search_query=relational+databases+sql+edx"},
    {"id": 13, "title": "Time Series Basics (Analytics Vidhya)", "subject": "Time Series", "difficulty": "Easy", "article_link": "https://www.analyticsvidhya.com/blog/2018/02/introduction-to-time-series-forecasting-with-python/", "youtube_link": "https://www.youtube.com/results?search_query=time+series+basics+analytics+vidhya"},
    {"id": 14, "title": "Time Series Analysis (Coursera)", "subject": "Time Series", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/practical-time-series-analysis", "youtube_link": "https://www.youtube.com/results?search_query=time+series+analysis+coursera"},
    {"id": 15, "title": "Forecasting: Principles and Practice (Book)", "subject": "Time Series", "difficulty": "Hard", "article_link": "https://otexts.com/fpp2/", "youtube_link": "https://www.youtube.com/results?search_query=forecasting+principles+and+practice"},
    {"id": 16, "title": "AWS Getting Started", "subject": "Cloud Computing", "difficulty": "Easy", "article_link": "https://aws.amazon.com/getting-started/", "youtube_link": "https://www.youtube.com/results?search_query=AWS+getting+started"},
    {"id": 17, "title": "Azure Fundamentals learning path", "subject": "Cloud Computing", "difficulty": "Medium", "article_link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "youtube_link": "https://www.youtube.com/results?search_query=Azure+fundamentals+learning+path"},
    {"id": 18, "title": "CNCF Cloud Native Certified", "subject": "Cloud Computing", "difficulty": "Hard", "article_link": "https://www.cncf.io/certification/cka/", "youtube_link": "https://www.youtube.com/results?search_query=CNCF+cloud+native+certified"},
    {"id": 19, "title": "Financial Markets", "subject": "Finance", "difficulty": "Easy", "article_link": "https://www.investopedia.com/terms/f/financial-market.asp", "youtube_link": "https://www.youtube.com/watch?v=Xh0y_M2D4Dk"},
    {"id": 20, "title": "Introduction to Marketing", "subject": "Marketing", "difficulty": "Easy", "article_link": "https://www.ama.org/the-definition-of-marketing-what-is-marketing/", "youtube_link": "https://www.youtube.com/watch?v=D-t3yT1gQ9o"}
]

# Mapping of courses to their core subjects
COURSE_SUBJECTS = {
    "B.Tech": ["ML", "AI", "DSA", "DBMS", "Time Series", "Cloud Computing"],
    "BBA": ["Finance", "Marketing", "Human Resources", "Business Strategy"],
    "B.Sc. Finance": ["Finance", "Economics", "Statistics", "Derivatives", "Risk Management"],
}

# Mock database for existing students
mock_students_db = {
    "s1": {"id": "s1", "name": "Siddh Shah", "course": "B.Tech"},
    "s2": {"id": "s2", "name": "Test Student", "course": "BBA"},
}

def generate_student_data(student_id: str, course: str):
    """
    Generates a student profile with random scores based on their course.
    """
    subjects = COURSE_SUBJECTS.get(course, [])
    if not subjects:
        raise HTTPException(status_code=400, detail=f"Course '{course}' not found.")
    
    student_profile = {
        "id": student_id,
        "name": student_id.split('@')[0], # Use the email prefix as a name
        "course": course,
        "subjects": {subject: random.randint(50, 100) for subject in subjects}
    }
    return student_profile

def get_recommendations_for_subject(student_id: str, subject: str):
    """
    Determines recommendations based on a student's score for a specific subject.
    """
    # Look up the student. If they don't exist, assume a course.
    student_profile = mock_students_db.get(student_id)
    course = student_profile["course"] if student_profile else "B.Tech"
    
    student_data = generate_student_data(student_id, course)
    score = student_data["subjects"].get(subject)
    
    if score is None:
        return []

    if score < 70:
        difficulties = ["Easy"]
    elif 70 <= score < 85:
        difficulties = ["Easy", "Medium"]
    else:  # score >= 85
        difficulties = ["Medium", "Hard"]

    return [r for r in resources if r["subject"] == subject and r["difficulty"] in difficulties]

async def select_subject_page(request: Request, student_id: str, templates: Jinja2Templates):
    # If the student doesn't exist, a profile will be generated for them
    student_profile = mock_students_db.get(student_id)
    course = student_profile["course"] if student_profile else "B.Tech"
    
    student_data = generate_student_data(student_id, course)
    
    return templates.TemplateResponse("select_subject.html", {
        "request": request,
        "student_id": student_id,
        "subjects": list(student_data["subjects"].keys())
    })

async def get_recommendations_page(request: Request, student_id: str, subject_name: str, templates: Jinja2Templates):
    # If the student doesn't exist, a profile will be generated for them
    student_profile = mock_students_db.get(student_id)
    course = student_profile["course"] if student_profile else "B.Tech"
    
    student_data = generate_student_data(student_id, course)
    subject_recs = get_recommendations_for_subject(student_id, subject_name)
    
    return templates.TemplateResponse("recommendations.html", {
        "request": request, 
        "student": student_data, 
        "recommendations": subject_recs, 
        "selected_subject": subject_name
    })