import os

with open(os.path.join("./", "Procfile"), "w") as f:
    line = "web: sh setup.sh && streamlit run app4.py"
    f.write(line)
