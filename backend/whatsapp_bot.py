import os
import tempfile
import requests
from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from langdetect import detect_langs, LangDetectException

router = APIRouter()

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


def detect_language(text: str) -> str:
    try:
        langs = detect_langs(text)
        top = langs[0]
        if top.lang == "hi" and top.prob >= 0.80:
            return "hi"
        if top.lang == "en" and top.prob >= 0.80:
            return "en"
        return "hi"
    except LangDetectException:
        return "hi"


def format_text_reply(data: dict, lang: str) -> str:
    band = data["band"]
    score = data["trust_score"]
    top_match = data["matches"][0] if data["matches"] else None

    if lang == "hi":
        header = {
            "High Risk": "⚠️ *उच्च जोखिम*",
            "Medium Risk": "🟠 *मध्यम जोखिम*",
            "Low Risk": "🔵 *कम जोखिम*",
            "Safe": "✅ *सुरक्षित*",
        }.get(band, band)
        reply = f"{header}\nभरोसा स्कोर: {score}/100\n\n"
        if band in ("High Risk", "Medium Risk"):
            reply += "यह संदेश धोखाधड़ी हो सकता है। कोई लिंक न खोलें, कोई निजी जानकारी न दें।\n"
            reply += "SEBI हेल्पलाइन: 1800 266 7575\nशिकायत दर्ज करें: https://scores.sebi.gov.in\n"
        else:
            reply += "यह संदेश असली SEBI परिपत्र से मेल खाता प्रतीत होता है।\n"
        if top_match:
            reply += f"\nमिलान: {top_match['title']}"
            if top_match.get("source_url"):
                reply += f"\n🔗 {top_match['source_url']}"
    else:
        header = {
            "High Risk": "⚠️ *HIGH RISK*",
            "Medium Risk": "🟠 *MEDIUM RISK*",
            "Low Risk": "🔵 *LOW RISK*",
            "Safe": "✅ *SAFE*",
        }.get(band, band)
        reply = f"{header}\nTrust Score: {score}/100\n\n"
        if band in ("High Risk", "Medium Risk"):
            reply += "This message shows signs of fraud. Do not click links or share personal details.\n"
            reply += "SEBI Helpline: 1800 266 7575\nFile a complaint: https://scores.sebi.gov.in\n"
        else:
            reply += "This message appears consistent with a genuine SEBI circular.\n"
        if top_match:
            reply += f"\nMatched: {top_match['title']}"
            if top_match.get("source_url"):
                reply += f"\n🔗 {top_match['source_url']}"

    return reply


def format_audio_reply(result: dict, lang: str) -> str:
    verdict = result.get("verdict", "UNKNOWN")
    confidence_pct = round(result.get("confidence", 0) * 100, 1)

    if verdict == "REAL":
        label_en, label_hi = "Likely Genuine Voice", "संभवतः असली आवाज़"
    elif verdict == "FAKE":
        label_en, label_hi = "Likely Synthetic / Cloned Voice", "संभवतः नकली / क्लोन आवाज़"
    else:
        label_en, label_hi = "Unable to Determine", "निर्धारित नहीं हो सका"

    if lang == "hi":
        reply = f"🎙️ *{label_hi}*\nविश्वास स्तर: {confidence_pct}%\n\n(यह सुविधा अभी परीक्षण चरण में है।)"
    else:
        reply = f"🎙️ *{label_en}*\nConfidence: {confidence_pct}%\n\n(This feature is still experimental.)"

    return reply


def download_twilio_media(media_url: str, suffix: str) -> str:
    response = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    response.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(response.content)
    tmp.close()
    return tmp.name


@router.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(""),
    NumMedia: str = Form("0"),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None),
):
    from backend.main import analyze, analyze_audio_file

    resp = MessagingResponse()
    msg = resp.message()

    num_media = int(NumMedia)

    if num_media > 0 and MediaContentType0:
        if MediaContentType0.startswith("audio"):
            tmp_path = None
            try:
                suffix = ".ogg" if "ogg" in MediaContentType0 else ".mp3"
                tmp_path = download_twilio_media(MediaUrl0, suffix)
                result = analyze_audio_file(tmp_path)
                lang = detect_language(Body) if Body.strip() else "en"
                msg.body(format_audio_reply(result, lang))
            except Exception:
                msg.body("Sorry, I couldn't process that voice note. Please try again or send text instead.")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return PlainTextResponse(str(resp), media_type="application/xml")

        elif MediaContentType0.startswith("video"):
            msg.body("Video analysis on WhatsApp isn't available yet. Please send text or a voice note for now.")
            return PlainTextResponse(str(resp), media_type="application/xml")

        else:
            msg.body("Sorry, this file type isn't supported yet. Please send text or a voice note.")
            return PlainTextResponse(str(resp), media_type="application/xml")

    text = Body.strip()
    if not text:
        msg.body("Please send a message, or forward a suspicious SEBI-related text, to check it.")
        return PlainTextResponse(str(resp), media_type="application/xml")

    lang = detect_language(text)
    try:
        data = analyze(text)
        msg.body(format_text_reply(data, lang))
    except Exception:
        msg.body("Something went wrong analyzing that message. Please try again shortly.")

    return PlainTextResponse(str(resp), media_type="application/xml")