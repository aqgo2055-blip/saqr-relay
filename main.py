"""
🦅 SAQR ZERO DAY — High-Performance SMTP Async Relay Microservice
سيرفر الإرسال السحابي فائق السرعة عبر منفذ الويب الآمن (HTTPS)
"""

import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="🦅 SAQR ZERO DAY SMTP RELAY",
    description="High-Speed Async Relay for Gmail & SMTP Dispatching",
    version="2.0.0",
)

# الرمز السري المشفر لحماية السيرفر الخاص بك
SECRET_TOKEN = "SAQR_SECRET_RELAY_KEY_2026"


# نموذج بيانات فحص الحساب
class VerifyPayload(BaseModel):
  email: str
  password: str


# نموذج بيانات إرسال الرسالة
class EmailPayload(BaseModel):
  sender_email: str
  sender_password: str
  recipient: str
  subject: str
  body: str


def build_ssl_context() -> ssl.SSLContext:
  """سياق تشفير SSL خفيف وسريع يتجاوز أي قيود في شهادات السيرفرات"""
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  return ctx


@app.get("/")
async def root():
  return {
      "status": "online",
      "engine": "SAQR ZERO DAY Async SMTP Relay",
      "health": "excellent",
  }


@app.post("/verify")
async def verify_account(
    data: VerifyPayload, x_relay_auth: str = Header(None)
):
  """فحص صحة حساب البريد وكلمة مرور التطبيقات بشكل فوري وحقيقي"""
  if x_relay_auth != SECRET_TOKEN:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )

  clean_pass = (
      str(data.password or "")
      .strip()
      .replace(" ", "")
      .replace("\n", "")
      .replace("\r", "")
  )
  clean_email = str(data.email or "").strip().lower()

  try:
    smtp_client = aiosmtplib.SMTP(
        hostname="smtp.gmail.com",
        port=587,
        timeout=10,
        tls_context=build_ssl_context(),
    )
    await smtp_client.connect()
    await smtp_client.starttls()
    await smtp_client.login(clean_email, clean_pass)
    await smtp_client.quit()
    return {"success": True, "message": "Account verified successfully"}
  except aiosmtplib.SMTPAuthenticationError:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="INVALID_APP_PASSWORD",
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Connection Error: {str(e)[:150]}",
    )


@app.post("/send")
async def send_email(data: EmailPayload, x_relay_auth: str = Header(None)):
  """إرسال فوري فائق السرعة عبر aiosmtplib بدون أي مهلة انتظار أو حظر"""
  if x_relay_auth != SECRET_TOKEN:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )

  clean_pass = (
      str(data.sender_password or "")
      .strip()
      .replace(" ", "")
      .replace("\n", "")
      .replace("\r", "")
  )
  sender = str(data.sender_email or "").strip()
  recipient = str(data.recipient or "").strip()

  # بناء محتوى الرسالة
  message = MIMEMultipart("alternative")
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = data.subject

  part_text = MIMEText(data.body, "plain", "utf-8")
  part_html = MIMEText(
      f"<div dir='auto'"
      f" style='font-family:sans-serif;'>{data.body.replace(chr(10), '<br>')}</div>",
      "html",
      "utf-8",
  )
  message.attach(part_text)
  message.attach(part_html)

  try:
    smtp_client = aiosmtplib.SMTP(
        hostname="smtp.gmail.com",
        port=587,
        timeout=12,
        tls_context=build_ssl_context(),
    )
    await smtp_client.connect()
    await smtp_client.starttls()
    await smtp_client.login(sender, clean_pass)
    await smtp_client.send_message(message)
    await smtp_client.quit()
    return {"success": True, "message": "Delivered successfully"}
  except aiosmtplib.SMTPAuthenticationError:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="INVALID_APP_PASSWORD",
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Dispatch Error: {str(e)[:150]}",
    )
