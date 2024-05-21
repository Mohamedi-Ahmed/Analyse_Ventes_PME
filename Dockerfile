FROM python:3

WORKDIR /project_data

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Execution du script Python
CMD [ "python", "app/app.py" ]
