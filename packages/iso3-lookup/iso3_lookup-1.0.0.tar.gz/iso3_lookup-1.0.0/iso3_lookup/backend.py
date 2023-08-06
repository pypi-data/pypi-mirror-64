from pathlib import Path
import pickle
import requests
from rapidfuzz import fuzz

PATH = Path(__file__).parent.joinpath("data").joinpath("stored.pickle")
URL = (
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes"
    "/master/all/all.json"
)


class Lookup:
    def __init__(self):
        if self.internet_on():
            self.refresh_data()
        self.data = self.get_stored_data()

    @staticmethod
    def internet_on():
        """
        Check if the internet connection is active and working.
        """
        try:
            requests.get("http://216.58.192.142", timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            return False

    @staticmethod
    def refresh_data():
        """
        Collect and save new data from github.
        """
        data = requests.get(URL).json()
        with open(PATH, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def get_stored_data():
        """
        Read data from local file.
        """
        with open(PATH, "rb") as f:
            data = pickle.load(f)
        return data

    def find_and_return_max(
        self, name_of_given_text: str, text_to_match: str, name_of_return_text: str
    ) -> str:
        """
        Find the `name_of_given_text` value in the data that is most like `text_to_match`
        and return the associated `name_of_return_text`.
        Attributes
        ----------
        name_of_return_text : str
            name of the dictionary item to compare to (alpha-3, country, etc)
        text_to_match: str
            string of text to match values against.
        name_of_return_text: str
            name of the dictionary item to return (alpha-3, country, etc)

        Returns
        -------
        str
            Value in the data that best matches.
        """
        current_max, current_return_text = 0, None
        for loop_dict in self.data:
            ratio = fuzz.partial_ratio(
                loop_dict[name_of_given_text].lower(), text_to_match.lower()
            )
            if ratio > current_max:
                current_return_text = loop_dict[name_of_return_text]
                current_max = ratio
        return current_return_text
