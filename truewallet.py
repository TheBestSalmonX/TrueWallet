import requests, re, json

class TrueWallet:

    HOST = "https://gift.truemoney.com/campaign/vouchers/"
    PATH_VERIFY = "/verify?moblie="
    PATH_REDEEM = "/redeem"

    def __init__(self, firstName, phoneNumber):
        self.firstName = firstName
        self.phoneNumber = phoneNumber
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-type": "application/json",
            "Origin": "https://gift.truemoney.com",
            "Connection": "keep-alive",
            "TE": "Trailers"
        }
        self.data = {
            "mobile": self.phoneNumber
        }

    def CheckPhoneNumberInCampaign(self, url):
        gift_code = self.ReplaceGiftCodeURL(url)
        url_gift_code = self.HOST + gift_code + self.PATH_VERIFY + self.phoneNumber
        return requests.get(url_gift_code).json()

    def ReplaceGiftCodeURL(self, url):
        gift_code = re.compile("(?:gift\:\/|gift\.truemoney\.com)\/campaign\/([?=a-zA-Z0-9]+)?")
        gift_code = gift_code.findall(url)
        gift_code = gift_code[0][len("?v="):].strip()
        return gift_code

    def RedeemGiftCode(self, url):
        gift_code = self.ReplaceGiftCodeURL(url)
        url_gift_code = self.HOST + gift_code + self.PATH_REDEEM
        return json.loads(requests.post(url_gift_code, headers=self.headers, json=self.data).text)["data"]["tickets"]

if __name__ == "__main__":
    client = TrueWallet(firstName="FIRST_NAME", phoneNumber="PHONE_NUMBER")
    url_truewallet_gift = "URL_TRUEWALLET_GIFT"

    checkInfo = client.CheckPhoneNumberInCampaign(url_truewallet_gift)
    print(checkInfo)
    if checkInfo["data"]["owner_profile"]["full_name"].startswith(client.firstName):
        print("You received a gift recently.")
    elif checkInfo["status"]["code"] == "VOUCHER_OUT_OF_STOCK":
        print("Coupons are sold out.")
    elif checkInfo["status"]["code"] != "TARGET_USER_REDEEMED":
        result = client.RedeemGiftCode(url_truewallet_gift)
        for user in result:
            if user["full_name"].startswith(client.firstName):
                print("You get paid" + user["amount_baht"] + "Bath.")
