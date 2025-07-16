# main.py
from fastapi import FastAPI, Body, Path, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # Thêm dòng này
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Tổng hợp API",
    description="API được tạo từ danh sách các URL yêu cầu, đã kích hoạt CORS.",
    version="1.0.1",
)

# --- Cấu hình CORS ---
# Thêm đoạn này để cho phép các trang web khác gọi đến API của bạn
origins = [
    "*",  # Cho phép tất cả các nguồn gốc. Để an toàn hơn, bạn nên thay bằng tên miền frontend của mình
    # Ví dụ: "https://your-frontend-app.com", "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

# --- Pydantic Models for Request Bodies ---
class OrderPayload(BaseModel):
    symbol: str = Field(..., example="FPT")
    quantity: int = Field(..., example=100)
    price: float = Field(..., example=120000)
    side: str = Field(..., example="BUY")

class AuthPayload(BaseModel):
    username: str = Field(..., example="user@example.com")
    password: str = Field(..., example="your_strong_password")

class SlackMessagePayload(BaseModel):
    channel: str = Field(..., example="#general")
    text: str = Field(..., example="Hello, world!")

# --- API Endpoints ---
# (Toàn bộ các endpoint giữ nguyên như cũ)

# 1. Active Orders
@app.get("/attive/orders", tags=["Entrade"])
async def get_active_orders(accountNo: str = Query(..., description="Số tài khoản phụ")):
    """Lấy danh sách lệnh đang hoạt động."""
    return {"endpoint": "/attive/orders", "accountNo": accountNo, "message": "Lấy danh sách lệnh thành công"}

# 2. Trading Token (Entrade)
@app.post("/dnse-order-service/trading-token", tags=["Entrade"])
async def get_trading_token():
    """Lấy trading token."""
    return {"endpoint": "/dnse-order-service/trading-token", "token": "mock_trading_token_string"}

# 3. Create Order (Entrade) - POST
@app.post("/dnse-order-service/v2/orders", tags=["Entrade"])
async def create_order(order: OrderPayload):
    """Tạo một lệnh mới."""
    return {"endpoint": "/dnse-order-service/v2/orders", "status": "Lệnh đã được tạo", "data": order.dict()}

# 4. Get/Update/Delete Order by ID (Entrade)
@app.get("/dnse-order-service/v2/orders/{order_id}", tags=["Entrade"])
async def get_order_by_id(order_id: str = Path(..., description="ID của lệnh"), accountNo: str = Query(..., description="Số tài khoản phụ")):
    """Lấy thông tin một lệnh cụ thể."""
    return {"endpoint": f"/dnse-order-service/v2/orders/{order_id}", "order_id": order_id, "accountNo": accountNo}

@app.put("/dnse-order-service/v2/orders/{order_id}", tags=["Entrade"])
async def update_order(order_id: str = Path(..., description="ID của lệnh"), accountNo: str = Query(..., description="Số tài khoản phụ"), order_update: OrderPayload = Body(...)):
    """Cập nhật (sửa) một lệnh."""
    return {"endpoint": f"/dnse-order-service/v2/orders/{order_id}", "status": "Lệnh đã được cập nhật", "order_id": order_id, "accountNo": accountNo, "update_data": order_update.dict()}

@app.delete("/dnse-order-service/v2/orders/{order_id}", tags=["Entrade"])
async def cancel_order(order_id: str = Path(..., description="ID của lệnh"), accountNo: str = Query(..., description="Số tài khoản phụ")):
    """Hủy một lệnh."""
    return {"endpoint": f"/dnse-order-service/v2/orders/{order_id}", "status": "Lệnh đã được hủy", "order_id": order_id, "accountNo": accountNo}

# 5. List Orders (Entrade) - GET
@app.get("/dnse-order-service/v2/orders", tags=["Entrade"])
async def list_orders(accountNo: str = Query(..., description="Số tài khoản phụ")):
    """Lấy danh sách các lệnh."""
    return {"endpoint": "/dnse-order-service/v2/orders", "accountNo": accountNo, "message": "Lấy danh sách lệnh thành công"}

# 6. Auth (Entrade User Service)
@app.post("/dnse-user-service/api/auth", tags=["Entrade"])
async def authenticate_user(payload: AuthPayload):
    """Xác thực người dùng."""
    return {"endpoint": "/dnse-user-service/api/auth", "status": "Xác thực thành công", "user": payload.username}

# 7. Get User Info (Entrade User Service)
@app.get("/dnse-user-service/api/me", tags=["Entrade"])
async def get_user_me():
    """Lấy thông tin người dùng hiện tại."""
    return {"endpoint": "/dnse-user-service/api/me", "user_info": {"id": "user123", "name": "Nguyễn Văn A"}}

# 8. SJC Homepage
@app.get("/sjc", tags=["SJC"])
async def sjc_homepage():
    """Endpoint mô phỏng trang chủ SJC."""
    return {"endpoint": "/sjc", "message": "Chào mừng đến SJC"}

# 9. SJC Price Service
@app.get("/sjc/GoldPrice/Services/PriceService.ashx", tags=["SJC"])
async def get_sjc_gold_price():
    """Lấy giá vàng từ SJC."""
    return {"endpoint": "/sjc/GoldPrice/Services/PriceService.ashx", "data": "Dữ liệu giá vàng ở đây"}

# 10. SJC Price Chart
@app.get("/sjc/bieu-do-gia-vang", tags=["SJC"])
async def get_sjc_price_chart():
    """Lấy dữ liệu biểu đồ giá vàng SJC."""
    return {"endpoint": "/sjc/bieu-do-gia-vang", "data": "Dữ liệu biểu đồ ở đây"}

# 11. Slack Post Message
@app.post("/slack/api/chat.postMessage", tags=["Slack"])
async def slack_post_message(payload: SlackMessagePayload):
    """Gửi tin nhắn đến Slack."""
    return {"endpoint": "/slack/api/chat.postMessage", "ok": True, "message": f"Tin nhắn đã được gửi đến kênh {payload.channel}"}

# 12. Slack File Upload
@app.post("/slack/api/files_upload", tags=["Slack"])
async def slack_upload_file(file: UploadFile = File(...), channel: str = Body(...)):
    """Tải file lên Slack."""
    return {"endpoint": "/slack/api/files_upload", "ok": True, "file_details": {"filename": file.filename, "content_type": file.content_type, "channel": channel}}

# 13. TCBS Homepage
@app.get("/tcinvest.tcbs.com.vn", tags=["TCBS"])
async def tcbs_homepage():
    """Endpoint mô phỏng trang chủ TCBS."""
    return {"endpoint": "/tcinvest.tcbs.com.vn", "message": "Chào mừng đến TCBS TCIvest"}

# 14 & 15. Vietcap Trading
@app.get("/trading.vietcap.com.vn/", tags=["Vietcap"])
async def vietcap_homepage():
    """Endpoint mô phỏng trang chủ Vietcap."""
    return {"endpoint": "/trading.vietcap.com.vn/"}

@app.get("/trading.vietcap.com.vn/api/", tags=["Vietcap"])
async def vietcap_api_root():
    """Endpoint mô phỏng API gốc của Vietcap."""
    return {"endpoint": "/trading.vietcap.com.vn/api/"}

# 16. Vietcap GraphQL
@app.api_route("/trading.vietcap.com.vn/data-mt/graphql", methods=["GET", "POST"], tags=["Vietcap"])
async def vietcap_graphql_endpoint(query: Optional[Dict[str, Any]] = None):
    """Endpoint mô phỏng GraphQL của Vietcap."""
    return {"endpoint": "/trading.vietcap.com.vn/data-mt/graphql", "message": "GraphQL endpoint", "received_query": query}

# 17. VnStocks Docs
@app.get("/vnstocks/docs/tai-lieu/lich-su-phien-ban", tags=["VnStocks"])
async def get_vnstocks_changelog():
    """Endpoint mô phỏng trang tài liệu VnStocks."""
    return {"endpoint": "/vnstocks/docs/tai-lieu/lich-su-phien-ban", "version": "1.0.0"}

# 18. MSN
@app.get("/msn", tags=["Khác"])
async def msn_homepage():
    """Endpoint mô phỏng trang MSN."""
    return {"endpoint": "/msn", "message": "Chào mừng đến MSN"}

# 19. Vietcombank Exchange Rates
@app.get("/vietcombank/api/exchangerates/exportexcel", tags=["Vietcombank"])
async def get_vcb_exchange_rates(date: str = Query(..., description="Ngày xuất dữ liệu, định dạng YYYY-MM-DD")):
    """Lấy tỷ giá Vietcombank theo ngày."""
    return {"endpoint": "/vietcombank/api/exchangerates/exportexcel", "date": date, "message": f"Đang xuất file Excel tỷ giá cho ngày {date}"}
