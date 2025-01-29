# Rent Bike

## Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
## Setup Environment
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Run Streamlit
streamlit dashboard.py
