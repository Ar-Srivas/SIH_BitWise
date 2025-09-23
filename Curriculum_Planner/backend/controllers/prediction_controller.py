import joblib
from pathlib import Path

models_dir = Path(__file__).parent.parent / "models"
scaler = joblib.load(models_dir / "scaler.pkl")
model1 = joblib.load(models_dir / "model1.pkl")
# model2 = joblib.load("models\\model2.pkl")

def predict_with_toefl(gre, toefl, lor, cgpa, uni_rating, research):
    gre = float(gre)
    toefl = float(toefl)
    lor = float(lor)
    cgpa = float(cgpa)
    uni_rating = int(uni_rating)
    research = int(research)

    cont_features = [gre, toefl, 3.4, lor, cgpa]
    cont_features = scaler.transform([cont_features])
    cont_features = list(cont_features[0])
    print("cont_features", cont_features)
    cont_features.pop(2)

    std_gre = cont_features[0]
    std_toefl = cont_features[1]
    std_lor = cont_features[2]
    std_cgpa = cont_features[3]

    uni_rating1 = uni_rating == 1
    uni_rating2 = uni_rating == 2
    uni_rating3 = uni_rating == 3
    uni_rating4 = uni_rating == 4
    uni_rating5 = uni_rating == 5

    research1 = research == 1
    research0 = research == 0

    prediction = model1.predict([[std_gre, std_toefl, std_lor, std_cgpa, uni_rating1, uni_rating2, uni_rating3, uni_rating4, uni_rating5, research0, research1]])
    return prediction[0]

# def predict_without_toefl(gre, lor, cgpa, uni_rating, research):
#     gre = float(gre)
#     lor = float(lor)
#     cgpa = float(cgpa)
#     uni_rating = int(uni_rating)
#     research = int(research)

#     cont_features = [gre, 107.41, 3.4, lor, cgpa]
#     cont_features = scaler.transform([cont_features])
#     cont_features = list(cont_features[0])
#     cont_features.pop(1)
#     cont_features.pop(2)

#     std_gre = cont_features[0]
#     std_lor = cont_features[1]
#     std_cgpa = cont_features[2]

#     uni_rating1 = uni_rating == 1
#     uni_rating2 = uni_rating == 2
#     uni_rating3 = uni_rating == 3
#     uni_rating4 = uni_rating == 4
#     uni_rating5 = uni_rating == 5

#     research1 = research == 1
#     research0 = research == 0

#     prediction = model2.predict([[std_gre, std_lor, std_cgpa, uni_rating1, uni_rating2, uni_rating3, uni_rating4, uni_rating5, research0, research1]])
#     return prediction[0]