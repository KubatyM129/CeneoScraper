import requests
import json
from bs4 import BeautifulSoup
# product_code = input("Podaj kod produktu\n")

def extract_tag(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except AttributeError:
        return None
    except TypeError:
        return ""

product_code = "96693065"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")
opinions = page_dom.select("div.js_product-review")
all_opinions = []
for opinion in opinions:
    single_opinion = {
        "opinion_id": extract_tag(opinion, "data-entry-id", None),
        "author": extract_tag(opinion, "span.user-post__author-name"),
        "recommendation": extract_tag(opinion, "span.user-post__author-recomendation > em"),
        "rating": extract_tag(opinion, "span.user-post__score-count"),
        "verified": extract_tag(opinion, "div.review-pz"),
        "post_date": extract_tag(opinion, "span.user-post__published > time:nth-child(1)", "datetime"),
        "purchase_date": extract_tag(opinion, "span.user-post__published > time:nth-child(2)", "datetime"),
        "vote_up": extract_tag(opinion, "button.vote-yes", "data-total-vote"),
        "vote_down": extract_tag(opinion, "button.vote-no", "data-total-vote"),
        "content": extract_tag(opinion, "div.user-post__text"),
        "cons": extract_tag(opinion, "div.review-feature__title--negatives ~ div.review-feature__item", None, True),
        "pros": extract_tag(opinion, "div.review-feature__title--positives ~ div.review-feature__item", None, True),
    }
    all_opinions.append(single_opinion)
print(all_opinions)
with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)