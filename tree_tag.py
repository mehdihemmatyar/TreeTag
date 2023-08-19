from fuzzywuzzy import process, fuzz
import rapidfuzz
import openai


def first_matches(item: str, keywords, scorer=rapidfuzz.fuzz.partial_ratio, th=80):
    """this is the base algorithm for matching

    :param item: food
    :type item: str
    :param keywords: keywords of treetag
    :type keywords: list[str]
    :param scorer: function  of matching
    :type scorer: fuzzi
    :param th: threshold for decsion
    :type th: int
    :return: list of mathced items"""
    candidates = list()
    for index, items in enumerate(keywords):
        if isinstance(items, list):
            pro_candid = process.extractOne(item, items, scorer=scorer, score_cutoff=th)
            if (
                pro_candid != None
                and len(pro_candid[0]) > 2
                and int(pro_candid[1]) >= th
            ):
                th = int(pro_candid[1])
                candidates.append((pro_candid[0], index))

        elif item not in ['', ' ', '  ', '   ']:
            can_score = int(scorer(item, items))
            if can_score >= th:
                th = can_score
                candidates.append((items, index))
    return candidates


def best_match(item, can, titles) -> str:
    """this is algorithm choice final item from output of first match

    :param item: food
    :type item: str
    :param can: first match output
    :type can: list[str]
    :param titles: tree tag titles
    :type titles: lsit[str]
    :return: mathced item form titles"""
    finla_th = 0
    final_index = 0
    new_final_th = 0
    for i in can:
        te = rapidfuzz.fuzz.token_sort_ratio(item, i[0])
        if te > finla_th:
            finla_th = te
            final_c = i[0]
            final_index = i[1]
        elif te == finla_th:
            te_title = rapidfuzz.fuzz.token_sort_ratio(item, titles[i[1]])
            if te_title > new_final_th:
    
                new_final_th = te_title
                final_c = i[0]
                final_index = i[1]

    return final_index


def match_lists(item, titles, keywords,msg1):

    if item in titles:
        return [[item,titles.index(item)]]
    first_can = first_matches(
        item=item, keywords=keywords, scorer=rapidfuzz.fuzz.WRatio, th=90
    )
    if len(first_can) == 0:
        print("open Ai request sent... ")
        openai.api_key = "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"
        messages = [ {"role": "system", "content":
                    "You are a intelligent assistant."} ]

        message = f"""
        اسم این محصول را در کوتاه ترین عبارت بگو
        مواد تشکیل دهنده:
        {msg1}
        """
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content
        first_can = first_matches(
        item=reply, keywords=keywords, scorer=rapidfuzz.fuzz.WRatio, th=90
    )
    #final_can = best_match(item=item, can=first_can, titles=titles)

    return first_can
