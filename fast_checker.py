from googlesearch import search
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_web_content(query):
    try:
        urls = list(search(query, num_results=10))

        print("\n========== DEBUG ==========")
        print("QUERY:", query)
        print("FOUND URLS:", urls)

        combined_text = ""

        for url in urls:
            try:
                print("FETCHING:", url)

                response = requests.get(
                    url,
                    timeout=10,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                soup = BeautifulSoup(response.text, "html.parser")

                paragraphs = soup.find_all("p")

                text = " ".join(
                    p.get_text(strip=True)
                    for p in paragraphs[:20]
                )

                combined_text += text + " "

            except Exception as e:
                print("FETCH ERROR:", e)

        print("TEXT LENGTH:", len(combined_text))
        print("===========================\n")

        return combined_text[:20000]

    except Exception as e:
        print("SEARCH ERROR:", e)
        return ""


def calculate_similarity(ai_answer, trusted_text):

    if not trusted_text:
        return 0

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [ai_answer, trusted_text]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)