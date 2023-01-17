import http.client
import json
from time import sleep


class Broker:

    def __init__(self):
        self.connection = http.client.HTTPSConnection("demo-api-capital.backend-capital.com")
        self.__session = self.__create_session()
        self.__account_balance = self.__session["BALANCE"]
        self.__cst_token = self.__session["CST_TOKEN"]
        self.__security_token = self.__session["X_SECURITY_TOKEN"]
        self.open_positions = self.__populate_open_positions()

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


    def __populate_open_positions(self):
        payload = ''
        headers = {
          'X-SECURITY-TOKEN': self.__security_token,
          'CST': self.__cst_token
        }
        self.connection.request("GET", "/api/v1/positions", payload, headers)
        res = self.connection.getresponse()
        data = res.read()
        open_positions = []
        for pos in json.loads(data.decode("utf-8"))["positions"]:
            position = {
                "ticker": pos["market"]["epic"],
                "name": pos["market"]["instrumentName"],
                "type": pos["market"]["instrumentType"],
                "date": pos["position"]["createdDate"],
                "dealId": pos["position"]["dealId"],
                "size": pos["position"]["size"],
                "direction": pos["position"]["direction"],
                "priceLevel": pos["position"]["level"]
            }
            open_positions.append(position)
        return open_positions

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
        self.connection.getresponse().read()

    def show_open_positions(self):
        for position in self.open_positions:
            for k, v in position.items():
                print(f"{k}: {v}")
            print("---------------")
        print(f"{len(self.open_positions)} open positions.")

    def close_position(self, dealId: str):
        payload = ''
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token
        }
        self.connection.request("DELETE", f"/api/v1/positions/{dealId}", payload, headers)
        self.connection.getresponse().read()

    def close_all_positions(self):
        payload = ''
        headers = {
            'X-SECURITY-TOKEN': self.__security_token,
            'CST': self.__cst_token
        }
        while len(self.open_positions) > 0:
            for position in self.open_positions:
                dealId = position["dealId"]
                self.connection.request("DELETE", f"/api/v1/positions/{dealId}", payload, headers)
                self.connection.getresponse().read()
                self.open_positions.remove(position)
                sleep(0.5)

def test_func():
    while True:
        sleep(0.5)
        obj = Broker()
        choice = input(">>>")
        if choice == "n":
            obj.create_position("SILVER", "BUY", 1.0, 22.0, 25.0)
        elif choice == "s":
            obj.show_open_positions()
        elif choice == "c":
            dealId = input("dealId >>>")
            obj.close_position(dealId)
        elif choice == "ca":
            obj.close_all_positions()
        elif choice == "q":
            break
        else:
            continue

