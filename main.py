import json
from typing import List

from fastapi import FastAPI, Query


import pandas as pd
from redis import Redis

from tree_tag import match_lists

r = Redis()



app = FastAPI()
@app.get("/batch")
def tag_batch(items: List[str] = Query(None),
              des: List[str] = Query(None)):
    """Match list of foods to their matched"""

    result_list = []
    id_list = []
    json_foods = json.loads(r.get("food_dict"))
    titles = list(json_foods.keys())
    keywords = list(json_foods.values())
    #for i in list(items):
    for i in zip(items,des):
        res1 = match_lists(i[0], titles, keywords,i[1:])
        for r11 in list(res1):
            result_list.append("".join(r11[0]))
            id_list.append(json.loads(r.get(titles[r11[1]])))
            
    return {"matched_items": result_list, "items_id": id_list}
