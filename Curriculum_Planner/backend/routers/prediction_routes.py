from fastapi import APIRouter
from backend.controllers.prediction_controller import predict_with_toefl
from pydantic import BaseModel

class StudentDetails(BaseModel):
    gre: float
    toefl: float
    lor: float
    cgpa: float
    uni_rating: int
    research: int

router=APIRouter()

@router.post("/predict")
async def predict(request: StudentDetails):
    try:
        prediction = predict_with_toefl(
            gre = request.gre,
            toefl = request.toefl,
            lor = request.lor,
            cgpa = request.cgpa,
            uni_rating = request.uni_rating,
            research = request.research
        )
        print(prediction)
        return {"prediction": prediction}
    except Exception as e:
        print("prediction router error: ", e)
        return {"prediction": "i dont know"}