 
#install pyTigergraph
#pip install pyTigerGraph

import pyTigerGraph as tg
hostName = "https://<host>"
userName = "<user>"
password = "<password>"
conn = tg.TigerGraphConnection(host=hostName, username=userName, password=password)
graphName = "<graph_name>"

Query_Graph = """ CREATE GRAPH {graphName} ()
USE GRAPH {graphName}
CREATE SCHEMA_CHANGE JOB schema_change_job_{graphName} FOR GRAPH {graphName} {
    'ADD VERTEX Cab_ (PRIMARY_ID cab_id INT , model STRING, mileage FLOAT, fuel STRING, regNo STRING, capacity INT, dest STRING, veh_lat FLOAT, veh_lng FLOAT)  WITH primary_id_as_attribute="true";\n\nADD VERTEX Booking_ (PRIMARY_ID booking_id INT , p_id INT, name STRING, gender STRING, pickup_id INT, pickup_address STRING, pickup_lat FLOAT, pickup_lon FLOAT, drop_off_id INT, drop_off_address STRING, drop_off_lat FLOAT, drop_off_lng FLOAT)  WITH primary_id_as_attribute="true";\n\nADD UNDIRECTED EDGE Booking_Cab_ (FROM Booking_ , TO Cab_);\n\n\nADD VERTEX Driver_ (PRIMARY_ID driver_id INT , name STRING, age INT, gender STRING)  WITH primary_id_as_attribute="true";\n\nADD UNDIRECTED EDGE Driver_Cab_ (FROM Driver_ , TO Cab_);'
}
RUN SCHEMA_CHANGE JOB schema_change_job_{graphName}
DROP JOB schema_change_job_{graphName}
"""

print(conn.gsql(Query_Graph))
        