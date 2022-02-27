import pandas as pd


# TODO create design pattern for Academy emulation
ztm_api = pd.read_csv("ztm.csv")

def search_courses(keyword: str, column: str) -> pd.core.frame.DataFrame:
    # TODO ****** ADD DOCS ******

    acros = ["ui", "ux", "api", "html", "css", "sql", "js"]

    try:

        if keyword.lower() in acros:
            keyword = keyword.upper()
        else:
            keyword = keyword.title()
        keyword_mask = ztm_api[column].apply(lambda x: keyword in x)
        courses = ztm_api[keyword_mask]

        if courses.empty:
            return f"'{keyword}' doesn't match any search results. Try being more specific."
        return courses

    except AttributeError:
        return f"Invalid keyword: {keyword} is of type {type(keyword)}. Keyword must be str."


if __name__ == "__main__":
    print(search_courses("andrei", "taught by"))
