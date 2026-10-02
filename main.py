"""
🦅 SAQR ZERO DAY — High-Performance SMTP Async Relay (Port 465 SSL Direct)
سيرفر الإرسال السحابي فائق السرعة عبر منفذ SSL 465 المباشر
"""

import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="🦅 SAQR ZERO DAY SMTP RELAY",
    description="Direct SSL 465 Async Relay",
    version="2.1.0",
)

SECRET_TOKEN = "SAQR_SECRET_RELAY_KEY_2026"


class VerifyPayload(BaseModel):
  email: str
  password: str


class EmailPayload(BaseModel):
  sender_email: str
  sender_password: str
  recipient: str
  subject: str
  body: str


def build_ssl_context() -> ssl.SSLContext:
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  return ctx


@app.get("/")
async def root():
  return {
      "status": "online",
      "engine": "SAQR ZERO DAY Port 465 Relay",
      "health": "excellent",
  }


@app.post("/verify")
async def verify_account(
    data: VerifyPayload, x_relay_auth: str = Header(None)
):
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
        port=465,
        use_tls=True,
        timeout=12,
        tls_context=build_ssl_context(),
    )
    await smtp_client.connect()
    await smtp_client.login(clean_email, clean_pass)
    await smtp_client.quit()
    return {"success": True, "message": "Account verified successfully"}
  except aiosmtplib.SMTPAuthenticationError:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_APP_PASSWORD"
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Connection Error: {str(e)[:150]}",
    )


@app.post("/send")
async def send_email(data: EmailPayload, x_relay_auth: str = Header(None)):
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
    # الاتصال المباشر المشفر عبر منفذ 465
    smtp_client = aiosmtplib.SMTP(
        hostname="smtp.gmail.com",
        port=465,
        use_tls=True,
        timeout=15,
        tls_context=build_ssl_context(),
    )
    await smtp_client.connect()
    await smtp_client.login(sender, clean_pass)
    await smtp_client.send_message(message)
    await smtp_client.quit()
    return {"success": True, "message": "Delivered successfully via SSL 465"}
  except aiosmtplib.SMTPAuthenticationError:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_APP_PASSWORD"
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Dispatch Error: {str(e)[:150]}",
    )
