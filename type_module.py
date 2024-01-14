from typing import TypedDict, Callable

class Council(TypedDict):
  council: str # Name of council (e.g. Maribyrnong; Merri-bek)
  regex_dict: dict # Dictionary of regex types and regexes
  scraper: Callable # Function that returns a link to the agenda
  