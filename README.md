# TrueWallet

## Usage
```python
if __name__ == "__main__":
    client = TrueWallet(firstName="", phoneNumber="PHONENUMBER")
    url_truewallet_gift = "https://gift.truemoney.com/campaign/?v=zeOCGJgWglji9hkodp"

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
```

## Author
Nuttasit Pangthum / [@FinX](https://www.facebook.com/finx.cf)
