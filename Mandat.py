import requests
from bs4 import BeautifulSoup
from Filter_json import filter_json


class Mandat:
    def __init__(self, year, type_, name):
        self.year = year
        self.type_ = type_
        self.name = name
        self.data_ = None
        self.is_none = False
        self.base_url = "https://mandat.uzbmb.uz"

        if (self.type_ == "Home"):
            try:
                open_url = f"{self.base_url}/Home{self.year}/Index"
                close_url = f"{self.base_url}/Home{self.year}/AfterFilter"
                with (requests.session() as ss):
                    begin_connection = ss.request(method="GET", url=open_url)
                    csrf_filter = BeautifulSoup(begin_connection.text, "html.parser")

                    csrf_token = str(csrf_filter.find_all("input")[0]["value"])

                    params = {
                        "name": self.name,
                        "region": "0",
                        "__RequestVerificationToken": csrf_token
                    }

                    get_data = ss.request(method="POST", url=close_url, data=params)
                    filter_data = BeautifulSoup(get_data.text, "html.parser")
                    keys = ""
                    values = ""
                    data = filter_data.find("table").find_all("tr")
                    for i in data[0].find_all("th"):
                        keys += str(
                            i.text.replace("\n", "").replace("\r", "").replace("                        ", "").replace(
                                "    ", "")) + "#"

                    for i in data[1].find_all("td"):
                        try:
                            values += self.base_url + str(i.find("a")["href"]) + "#"
                        except:
                            datas = str(i.text.replace("\n", "").replace("\r", "").replace("                        ",
                                                                                           "").replace("    ",
                                                                                                       "")) + "#"
                            if (datas == "Ma'lumot topilmadi#"):
                                self.is_none = True
                                break
                            else:
                                values += datas

                    if (self.is_none):
                        self.data_ = []
                        self.data_ = ["Natija", "Hech qanday ma'lumot yo'q ekan"]
                    else:
                        a = filter_json(keys, values)
                        self.data_ = a.get_filter_data().copy()


            except:
                self.data_ = []
                self.data_ = ["Natija", "Sayt ishlamayapti.Keyinroq qayta urunib ko'ring"]


        elif (self.type_ == "Transfer"):

            try:
                open_url = f"{self.base_url}Transfer{self.year}/Transfer"
                close_url = f"{self.base_url}/Transfer{self.year}/AfterFilter"
                with (requests.session() as ss):
                    begin_connection = ss.request(method="GET", url=open_url)
                    csrf_filter = BeautifulSoup(begin_connection.text, "html.parser")

                    csrf_token = str(csrf_filter.find_all("input")[0]["value"])

                    params = {
                        "name": self.name,
                        "region": "0",
                        "__RequestVerificationToken": csrf_token
                    }

                    get_data = ss.request(method="POST", url=close_url, data=params)
                    filter_data = BeautifulSoup(get_data.text, "html.parser")
                    keys = ""
                    values = ""
                    data = filter_data.find("table").find_all("tr")
                    for i in data[0].find_all("th"):
                        keys += str(
                            i.text.replace("\n", "").replace("\r", "").replace("                        ", "").replace(
                                "    ", "")) + "#"

                    for i in data[1].find_all("td"):
                        try:
                            values += self.base_url + str(i.find("a")["href"]) + "#"
                        except:
                            datas = str(i.text.replace("\n", "").replace("\r", "").replace("                        ",
                                                                                           "").replace("    ",
                                                                                                       "")) + "#"
                            if (datas == "Ma'lumot topilmadi#"):
                                self.is_none = True
                                break
                            else:
                                values += datas

                    if (self.is_none):
                        self.data_ = ["Natija", "Hech qanday ma'lumot yo'q ekan"]
                    else:
                        a = filter_json(keys, values)
                        self.data_ = a.get_filter_data().copy()
                        a.clear_data()


            except:
                self.data_ = ["natija", "Hech qanday ma'lumot topilmadi"]

    def get_data(self):

        return self.data_

    def clear_all(self):
        self.data_ = []