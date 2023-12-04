from flask import Flask, request, jsonify,send_file
from flask_cors import CORS, cross_origin

from palm import get_answer
import pyTigerGraph as tg
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/upload_csv',methods=['POST'])
def upload_csv():
    files = request.files.getlist('upload_csv')
    if not files:
        return 'No files part'
    datasets =""
    for file in files:
        if file.filename == '':
            return 'No selected file'

        # Read CSV data using pandas
        try:
            df = pd.read_csv(file)
            extracted_data = df.head(6)
            datasets += extracted_data.to_string(index=False)

        except pd.errors.EmptyDataError:
            return f'Uploaded file {file.filename} is empty or not a valid CSV file'

    res = {
        "datasets" : datasets
    }
    return res

@app.route('/post_prompt', methods=['POST'])
def post_data():
    # Extract data from the request
    data = request.get_json()
    topic = data['title']
    datasets = data['datasets']

    prompt = 'Topic:'+topic + '\n'+'Dataset:\n'+datasets


    # Process the data
    print(f"{prompt}")
    answer = get_answer(data)
    res = { 
            "answer" : answer
            
        } 
    print(res)
    # Send a response
    return jsonify(res) 


@app.route('/download_script', methods=['GET','POST'])
def download_script():
    if request.method == 'POST':
        data = request.get_json()
        schema_code = data["schemaCode"]
        schema_code = repr(schema_code)
        # graphName = ""
        print(schema_code)
        
        # print(Query_Graph)
        py_content = f''' 
#install pyTigergraph
#pip install pyTigerGraph

import pyTigerGraph as tg
hostName = "https://<host>"
userName = "<user>"
password = "<password>"
conn = tg.TigerGraphConnection(host=hostName, username=userName, password=password)
graphName = "<graph_name>"

Query_Graph = """ CREATE GRAPH {{graphName}} ()
USE GRAPH {{graphName}}
CREATE SCHEMA_CHANGE JOB schema_change_job_{{graphName}} FOR GRAPH {{graphName}} {{
    {schema_code}
}}
RUN SCHEMA_CHANGE JOB schema_change_job_{{graphName}}
DROP JOB schema_change_job_{{graphName}}
"""

print(conn.gsql(Query_Graph))
        '''
        with open('uploaded_script.py', 'w') as f:
            try:
                f.write(py_content)
            except:
                return "GOT Error"

        return send_file('uploaded_script.py', as_attachment=True, download_name='uploaded_script.py')

    elif request.method == 'GET':
        # You can customize the filename and content type as needed
        filename = 'uploaded_script.py'
        script_content = None

        # You can read the script content from the file or from your storage
        with open(filename, 'r') as f:
            script_content = f.read()

        # Using BytesIO to create an in-memory file-like object
        # script_file = BytesIO(script_content)

        return send_file(filename, as_attachment=True, download_name=filename)



@app.route('/create_schema',methods=['POST'])
def create_schema():
    data = request.get_json()
    hostName = data["hostname"]
    userName = data["userName"]
    password = data["password"]
    conn = tg.TigerGraphConnection(host=hostName, username=userName, password=password)
    res = "connected"
    Query_Graph = f"""
    CREATE GRAPH {data["graphName"]} ()
    USE GRAPH {data["graphName"]}
    CREATE SCHEMA_CHANGE JOB schema_change_job_{data["graphName"]} FOR GRAPH {data["graphName"]} {{
        {data["schemaCode"]}
    }}
    RUN SCHEMA_CHANGE JOB schema_change_job_{data["graphName"]}
    DROP JOB schema_change_job_{data["graphName"]}
    """
    try:
        print(conn.gsql(Query_Graph))
        res = {"response":"Success"}
        return jsonify(res)
    except:
        res = {"response":"Error"}
        return res
    
    # return res
    # return connected
    
if __name__ == '__main__':

    app.run(debug=True)