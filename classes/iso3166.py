import sqlite3


class ISO3166:
    """
    Class to get country codes for ISO-3166-2 in alpha2, alpha3 and numeric format.
    """

    def __init__(self):
        self.__raw = self.get_from_db()
        self.__keys = ['name', 'alpha_2', 'alpha_3', 'numeric']
        self.countries = []
        for country in self.__raw:
            country_dic = {}
            for key in self.__keys:
                country_dic[key] = country[country_dic.__len__()]
            self.countries.append(country_dic)

    def filter_by_alpha2(self, alpha2):
        return list(country for country in self.countries if country['alpha_2'] == alpha2)[0]

    def renew_data(self):
        pass

    def get_from_db(self):
        db = sqlite3.connect("./sqlite/iso3166.db")
        c = db.cursor()
        c.execute("SELECT * FROM countries")
        return c.fetchall()
