# recommend_controller.py
import random
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

resources = [
    # ML
    {"id": 1, "title": "ML Crash Course (Google)", "subject": "ML", "difficulty": "Easy", "article_link": "https://developers.google.com/machine-learning/crash-course", "youtube_link": "https://www.youtube.com/playlist?list=PLI0hA0K_4o7GvR0E2iM_f_nF7S2T5M3aR"},
    {"id": 2, "title": "Intro to ML (Coursera)", "subject": "ML", "difficulty": "Easy", "article_link": "https://www.coursera.org/learn/machine-learning-with-python", "youtube_link": "https://www.youtube.com/results?search_query=machine+learning+python+coursera"},
    {"id": 3, "title": "Machine Learning (Andrew Ng)", "subject": "ML", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/machine-learning", "youtube_link": "https://www.youtube.com/results?search_query=Andrew+Ng+machine+learning+course"},
    {"id": 4, "title": "Practical ML (Coursera)", "subject": "ML", "difficulty": "Medium", "article_link": "https://www.coursera.org/learn/practical-machine-learning", "youtube_link": "https://www.youtube.com/results?search_query=practical+machine+learning+coursera"},
    {"id": 5, "title": "Deep Learning Specialization", "subject": "ML", "difficulty": "Difficult", "article_link": "https://www.coursera.org/specializations/deep-learning", "youtube_link": "https://www.youtube.com/results?search_query=deep+learning+specialization+coursera"},
    {"id": 6, "title": "Stanford CS229", "subject": "ML", "difficulty": "Difficult", "article_link": "https://cs229.stanford.edu/", "youtube_link": "https://www.youtube.com/results?search_query=Stanford+CS229"},

    # AI
    {"id": 7, "title": "AI For Everyone (Andrew Ng)", "subject": "AI", "difficulty": "Easy", "article_link": "https://www.coursera.org/learn/ai-for-everyone", "youtube_link": "https://www.youtube.com/results?search_query=AI+for+everyone"},
    {"id": 8, "title": "MIT Introduction to AI", "subject": "AI", "difficulty": "Medium", "article_link": "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/", "youtube_link": "https://www.youtube.com/playlist?list=PLB56EAE72D6D3A449"},
    {"id": 9, "title": "Stanford CS221 (AI)", "subject": "AI", "difficulty": "Difficult", "article_link": "http://web.stanford.edu/class/cs221/", "youtube_link": "https://www.youtube.com/results?search_query=Stanford+CS221+AI"},

    # DSA
    {"id": 10, "title": "Data Structures (GeeksforGeeks)", "subject": "DSA", "difficulty": "Easy", "article_link": "https://www.geeksforgeeks.org/data-structures/", "youtube_link": "https://www.youtube.com/results?search_query=data+structures+geeksforgeeks"},
    {"id": 11, "title": "Visual Algorithm Explorer", "subject": "DSA", "difficulty": "Medium", "article_link": "https://visualgo.net/en", "youtube_link": "https://www.youtube.com/results?search_query=Visualgo+algorithms"},
    {"id": 12, "title": "Algorithms, Sedgewick & Wayne", "subject": "DSA", "difficulty": "Difficult", "article_link": "https://algs4.cs.princeton.edu/home/", "youtube_link": "https://www.youtube.com/results?search_query=Sedgewick+algorithms"},

    # Cloud Computing
    {"id": 13, "title": "AWS Getting Started", "subject": "Cloud Computing", "difficulty": "Easy", "article_link": "https://aws.amazon.com/getting-started/", "youtube_link": "https://www.youtube.com/results?search_query=AWS+getting+started"},
    {"id": 14, "title": "Azure Fundamentals", "subject": "Cloud Computing", "difficulty": "Medium", "article_link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "youtube_link": "https://www.youtube.com/results?search_query=Azure+fundamentals+learning+path"},
    {"id": 15, "title": "Kubernetes Certification (CNCF)", "subject": "Cloud Computing", "difficulty": "Difficult", "article_link": "https://www.cncf.io/certification/cka/", "youtube_link": "https://www.youtube.com/results?search_query=CNCF+cloud+native+certified"},

    # Web Development
    {"id": 16, "title": "Codecademy Web Dev", "subject": "Web Development", "difficulty": "Easy", "article_link": "https://www.codecademy.com/learn/paths/front-end-engineer-career-path", "youtube_link": "https://www.youtube.com/results?search_query=Codecademy+front+end+developer"},
    {"id": 17, "title": "FreeCodeCamp Responsive Web Design", "subject": "Web Development", "difficulty": "Medium", "article_link": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "youtube_link": "https://www.youtube.com/results?search_query=FreeCodeCamp+responsive+web+design"},
    {"id": 18, "title": "The Odin Project", "subject": "Web Development", "difficulty": "Difficult", "article_link": "https://www.theodinproject.com/", "youtube_link": "https://www.youtube.com/results?search_query=The+Odin+Project+full+stack"},
    
    # Cyber Security
    {"id": 19, "title": "TryHackMe", "subject": "Cyber Security", "difficulty": "Easy", "article_link": "https://tryhackme.com/", "youtube_link": "https://www.youtube.com/results?search_query=TryHackMe+tutorials"},
    {"id": 20, "title": "Hack The Box Academy", "subject": "Cyber Security", "difficulty": "Medium", "article_link": "https://academy.hackthebox.com/", "youtube_link": "https://www.youtube.com/results?search_query=Hack+The+Box+Academy+walkthroughs"},
    {"id": 21, "title": "Offensive Security (OSCP)", "subject": "Cyber Security", "difficulty": "Difficult", "article_link": "https://www.offensive-security.com/pwk-oscp/", "youtube_link": "https://www.youtube.com/results?search_query=OSCP+review"},
    
    # Data Science
    {"id": 22, "title": "Kaggle Getting Started", "subject": "Data Science", "difficulty": "Easy", "article_link": "https://www.kaggle.com/getting-started", "youtube_link": "https://www.youtube.com/results?search_query=Kaggle+for+beginners"},
    {"id": 23, "title": "Data Science Specialization (JHU)", "subject": "Data Science", "difficulty": "Medium", "article_link": "https://www.coursera.org/specializations/jhu-data-science", "youtube_link": "https://www.youtube.com/results?search_query=Data+Science+Specialization+JHU"},
    {"id": 24, "title": "Fast.ai", "subject": "Data Science", "difficulty": "Difficult", "article_link": "https://course.fast.ai/", "youtube_link": "https://www.youtube.com/results?search_query=fast.ai+course"},
    
    # Networking
    {"id": 25, "title": "Cisco Networking Academy", "subject": "Networking", "difficulty": "Easy", "article_link": "https://www.netacad.com/", "youtube_link": "https://www.youtube.com/results?search_query=Cisco+Networking+Academy"},
    {"id": 26, "title": "CompTIA Network+ Certification", "subject": "Networking", "difficulty": "Medium", "article_link": "https://www.comptia.org/certifications/network", "youtube_link": "https://www.youtube.com/results?search_query=CompTIA+Network+Plus+review"},
    {"id": 27, "title": "CCNA Training (Cisco)", "subject": "Networking", "difficulty": "Difficult", "article_link": "https://learningnetwork.cisco.com/s/ccna-training", "youtube_link": "https://www.youtube.com/results?search_query=Cisco+CCNA+course"},
]

COURSE_SUBJECTS = {
    "B.Tech": ["ML", "AI", "DSA", "Cloud Computing", "Web Development", "Cyber Security", "Data Science", "Networking"],
    "BBA": ["Finance", "Marketing", "Human Resources", "Business Strategy"],
    "B.Sc. Finance": ["Finance", "Economics", "Statistics", "Derivatives", "Risk Management"],
}

mock_students_db = {
    "s1": {"id": "s1", "name": "Siddh Shah", "course": "B.Tech"},
    "s2": {"id": "s2", "name": "Test Student", "course": "BBA"},
    "s3": {"id": "s3", "name": "Financial Student", "course": "B.Sc. Finance"},
}

def generate_student_data(student_id: str, course: str):
    subjects = COURSE_SUBJECTS.get(course, [])
    if not subjects:
        raise HTTPException(status_code=400, detail=f"Course '{course}' not found.")
    
    student_profile = {
        "id": student_id,
        "name": student_id.split('@')[0],
        "course": course,
        "subjects": {subject: random.randint(50, 100) for subject in subjects}
    }
    return student_profile

def get_recommendations_for_subject(subject: str):
    """
    Returns all resources for a given subject, grouped by difficulty.
    """
    subject_resources = [r for r in resources if r["subject"] == subject]
    
    recommendations = {
        "Easy": [],
        "Medium": [],
        "Difficult": []
    }
    for rec in subject_resources:
        # This line is the potential source of the KeyError
        recommendations[rec["difficulty"]].append(rec)
    
    return recommendations

async def select_subject_page(request: Request, student_id: str, templates: Jinja2Templates):
    student_profile = mock_students_db.get(student_id)
    if not student_profile:
        student_data = generate_student_data(student_id, "B.Tech")
    else:
        student_data = generate_student_data(student_id, student_profile["course"])
    
    return templates.TemplateResponse("select_subject.html", {
        "request": request,
        "student_id": student_id,
        "subjects": list(student_data["subjects"].keys())
    })

async def get_recommendations_page(request: Request, student_id: str, subject_name: str, templates: Jinja2Templates):
    student_profile = mock_students_db.get(student_id)
    if not student_profile:
        student_data = generate_student_data(student_id, "B.Tech")
    else:
        student_data = generate_student_data(student_id, student_profile["course"])
        
    subject_recs = get_recommendations_for_subject(subject_name)
    
    return templates.TemplateResponse("recommendations.html", {
        "request": request, 
        "student": student_data, 
        "recommendations": subject_recs,
        "selected_subject": subject_name
    })