import wikipedia
from ddgs import DDGS


def clean_query(query):

    remove_words = [
        "explain",
        "what is",
        "define",
        "describe",
        "tell me about",
        "give me"
    ]

    query = query.lower()

    for word in remove_words:
        query = query.replace(word, "")

    return query.strip()


def get_wiki_evidence(query):

    evidence = ""

    try:

        query = clean_query(query)

        results = wikipedia.search(query)

        for topic in results[:10]:

            try:

                evidence += wikipedia.summary(
                    topic,
                    sentences=8
                )

                evidence += "\n\n"

            except:
                pass

    except:
        pass

    return evidence


def get_web_evidence(query):

    evidence = ""

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=15
                )
            )

            for r in results:

                evidence += r.get("title", "")
                evidence += "\n"

                evidence += r.get("body", "")
                evidence += "\n\n"

    except Exception as e:

        print("WEB ERROR:", e)

    return evidence


def get_combined_evidence(query):

    wiki_text = get_wiki_evidence(query)

    web_text = get_web_evidence(query)

    return wiki_text + "\n\n" + web_text