import redis
import pandas as pd
import pyodbc
import sys
import json
redis_client = redis.Redis()

sql_query = "SELECT [title],[keywords],[id] FROM [zoodfood_db].[dbo].[TreeTags] where level >1"

bi_warehouse_connection_string: str (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=79.175.132.125,1410;"
            "Database=zoodfood_db;"
            "UID=Product;"
            "PWD=ASPgaBFVRpppecMN;"
            "TrustServerCertificate=yes;"
        )
connection = pyodbc.connect(bi_warehouse_connection_string)

#cursor = connection.cursor()
try:
    #cursor.execute(sql_query)
    results = pd.read_sql(sql_query, connection)

    print(f"Results:\n{results}")

    # Perform preprocessing and store data in Redis
    food_dict = {}
    food_node = {}
    #df = pd.DataFrame(results)
    df_filled = results.fillna(value=0)
    for row_index in range(df_filled.shape[0]):
        row = df_filled.iloc[row_index]
        #row[0] = cleanify(row[0])
        if row[1] == 0:
            food_dict[row[0]] = row[0]
        else:
            words = row[1].split(",")
            #words = [cleanify(w) for w in words]
            food_dict[row[0]] = list(filter(None, words))
        food_node[row[0]] = str(row[2])
        redis_client.set(row[0], json.dumps(str(row[2])))
    redis_client.set("food_dict", json.dumps(food_dict))
except Exception as e:
    print(str(e), file=sys.stderr)
finally:
    #cursor.close()
    redis_client.close()
