from fastapi import FastAPI, Query, Body from typing import Optional import requests

app = FastAPI(title="VNStock REST API", version="1.0")

DNSE

@app.get("/api/dnse/auth") def dnse_auth(): url = "https://services.entrade.com.vn/dnse-user-service/api/auth" return requests.get(url).json()

@app.get("/api/dnse/user-info") def dnse_user_info(): url = "https://services.entrade.com.vn/dnse-user-service/api/me" return requests.get(url).json()

@app.get("/api/dnse/accounts") def dnse_accounts(): url = "https://services.entrade.com.vn/dnse-order-service/accounts" return requests.get(url).json()

@app.get("/api/dnse/account-balance/{sub_account}") def dnse_account_balance(sub_account: str): url = f"https://services.entrade.com.vn/dnse-order-service/account-balances/{sub_account}" return requests.get(url).json()

@app.get("/api/dnse/email-otp") def dnse_email_otp(): url = "https://services.entrade.com.vn/dnse-auth-service/api/email-otp" return requests.get(url).json()

@app.get("/api/dnse/trading-token") def dnse_trading_token(): url = "https://services.entrade.com.vn/dnse-order-service/trading-token" return requests.get(url).json()

@app.get("/api/dnse/loan-packages/{sub_account}") def dnse_loan_packages(sub_account: str): url = f"https://services.entrade.com.vn/dnse-order-service/accounts/{sub_account}/loan-packages" return requests.get(url).json()

@app.get("/api/dnse/orders") def dnse_orders(): url = "https://services.entrade.com.vn/dnse-order-service/v2/orders" return requests.get(url).json()

@app.get("/api/dnse/orders/derivative") def dnse_derivative_orders(): url = "https://services.entrade.com.vn/dnse-order-service/derivative/orders" return requests.get(url).json()

@app.get("/api/dnse/deals") def dnse_deals(): url = "https://services.entrade.com.vn/dnse-deal-service/deals" return requests.get(url).json()

@app.get("/api/dnse/derivative-deals") def dnse_derivative_deals(): url = "https://services.entrade.com.vn/dnse-derivative-core/deals" return requests.get(url).json()

TCBS

@app.get("/api/tcbs/overview") def get_tcbs_overview(): url = "https://apipubaws.tcbs.com.vn" return {"status_code": requests.get(url).status_code}

FMarket

@app.get("/api/fmarket/funds") def get_fmarket_funds(): url = "https://api.fmarket.vn/res/products" return requests.get(url).json()

Vietcombank

@app.get("/api/vcb/exchange-rate") def get_exchange_rate(date: str = Query(..., description="Format: dd/mm/yyyy")): url = f"https://www.vietcombank.com.vn/api/exchangerates/exportexcel?date={date}" return {"status_code": requests.get(url).status_code, "preview": requests.get(url).text[:300]}

Gold

@app.get("/api/gold/sjc") def get_gold_sjc(): url = "https://sjc.com.vn/GoldPrice/Services/PriceService.ashx" return requests.get(url).text

@app.get("/api/gold/btmc") def get_gold_btmc(): url = "http://api.btmc.vn/api/BTMCAPI/getpricebtmc?key=public" return requests.get(url).json()

MSN

@app.get("/api/msn/finance/resolve") def msn_finance_resolve(): url = "https://assets.msn.com/resolver/api/resolve/v3/config" return requests.get(url).json()

@app.get("/api/msn/autosuggest") def msn_autosuggest(query: str): url = f"https://services.bingapis.com/contentservices-finance.csautosuggest/api/v1/Query?q={query}" return requests.get(url).json()

Notifications

@app.post("/api/notify/slack") def notify_slack(token: str = Body(...), channel: str = Body(...), text: str = Body(...)): url = "https://slack.com/api/chat.postMessage" headers = {"Authorization": f"Bearer {token}"} data = {"channel": channel, "text": text} return requests.post(url, headers=headers, data=data).json()

@app.post("/api/notify/telegram") def notify_telegram(token: str = Body(...), chat_id: str = Body(...), msg: str = Body(...)): url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}" return requests.get(url).json()

@app.post("/api/notify/lark") def notify_lark(token: str = Body(...), body: dict = Body(...)): url = f"https://botbuilder.larksuite.com/api/trigger-webhook/{token}" return requests.post(url, json=body).json()
