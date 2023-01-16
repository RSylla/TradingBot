import http.client
import json

class Broker:

    def __init__(self):
        self.connection = http.client.HTTPSConnection("demo-api-capital.backend-capital.com")
        self.__session = self.__create_session()
        self.__account_balance = self.__session["BALANCE"]
        self.__cst_token = self.__session["CST_TOKEN"]
        self.__security_token = self.__session["X_SECURITY_TOKEN"]
        self.open_positions = []

    def __create_session(self):
        payload = json.dumps({
            "identifier": "raivo.sylla@gmail.com",
            "password": "@S3ctumS3mpra"
        })
        headers = {
            'X-CAP-API-KEY': '6NwR2oqK2tsHauJZ',
            'Content-Type': 'application/json'
        }
        self.connection.request("POST", "/api/v1/session", payload, headers)
        response = self.connection.getresponse()
        read_response = response.read()
        header = response.headers
        data = json.loads(read_response.decode("utf-8"))

        cst_token = header['CST']
        security_token = header['X-SECURITY-TOKEN']
        account_balance = float(data["accountInfo"]["balance"])

        output = {"CST_TOKEN": cst_token,
                  "X_SECURITY_TOKEN": security_token,
                  "BALANCE": account_balance}
        return output

    def get_account_balance(self):
        return self.__account_balance

    def create_position(self, ticker: str, direction: str, qty: float, stop: float, profit: float):
        position = {
            "epic": ticker,
            "direction": direction,
            "size": qty,
            "guaranteedStop": True,
            "stopLevel": stop,
            "profitLevel": profit
        }
        payload = json.dumps(position)
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token,
            'Content-Type': 'application/json'
        }
        self.connection.request("POST", "/api/v1/positions", payload, headers)
        res = self.connection.getresponse()
        data = res.read()
        dealReference = json.loads(data.decode("utf-8"))["dealReference"]

        self.connection.request("GET", f"/api/v1/confirms/{dealReference}", "", headers)
        res = self.connection.getresponse()
        response = res.read()
        data = json.loads(response.decode("utf-8"))
        dealId = data["affectedDeals"][0]["dealId"]

        position["dealId"] = dealId
        self.open_positions.append(position)


    def get_all_positions(self):
        payload = ''
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token
        }
        self.connection.request("GET", "/api/v1/positions", payload, headers)
        res = self.connection.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def close_position(self, dealId: str):
        payload = ''
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token
        }
        self.connection.request("DELETE", f"/api/v1/positions/{dealId}", payload, headers)

    def close_all_positions(self):
        payload = ''
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token
        }
        self.connection.request("GET", "/api/v1/positions", payload, headers)
        res = self.connection.getresponse()
        data = res.read()
        print(data)

        for position in data["positions"]
            dealId = position["dealId"]
            self.connection.request("DELETE", f"/api/v1/positions/{dealId}", payload, headers)
            self.open_positions.remove(position)




obj = Broker()

# print(obj.get_account_balance())
# obj.create_position("SILVER", "BUY", 1.0, 22.0, 25.0)
# obj.get_all_positions()
# obj.close_position()

obj.close_all_positions()


