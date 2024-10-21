
import streamlit as st

import numpy as np
import csv

from models import DINA, DINO, ACDM
from estimate import MLE


st.title('Math CDA')

option = st.selectbox(
    "Model",
    ("ACDM", "DINA", "DINO"),
)

TargetModel = {
    "DINA": DINA,
    "DINO": DINO,
    "ACDM": ACDM
}[option]

slip_val = st.slider("slip", 0.0, 0.5, 0.2, 0.05)
guess_val = st.slider("guess", 0.0, 0.5, 0.4, 0.05)

model = TargetModel(
    slip=np.array([slip_val] * 12),
    guess=np.array([guess_val] * 12)
)

with open("data/q_matrix.csv", "r") as f:
    reader = csv.reader(f)
    skill_name = next(reader)[1:]
    qm = np.array([[int(i) for i in row[1:]] for row in reader])
    print("Q-matrix Loaded: ", qm.shape)

# with open("data/student_answers.csv", "r") as f:
#     reader = csv.reader(f)
#     student_id = next(reader)[1:]
#     x = np.array([[int(i) for i in row[1:]] for row in reader])
#     print("Student Answer Loaded: ", x.shape)


# for i in range(len(student_id)):
#     print(student_id[i], ":", [skill_name[j] for j in range(len(skill_name)) if alpha[i][j] == 1])


st.subheader("Q-Matrix")
st.table(qm)

checks = st.columns(6)
l = []
for i in range(6):
    with checks[i]:
        l.append(st.checkbox(str(i)))

checks2 = st.columns(6)
for i in range(6, 12):
    with checks2[i - 6]:
        l.append(st.checkbox(str(i)))

x = np.array([l])
alpha = MLE(model, qm, x)

st.subheader("Estimated Skill Vector")
st.write(alpha)


