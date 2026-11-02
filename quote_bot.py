import os
import asyncio
import random
import logging
from telethon import TelegramClient
from g4f.client import Client as G4FClient

# Logging Setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment Variables မှ အချက်အလက်များ ယူခြင်း
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = TelegramClient('quote_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
g4f_client = G4FClient()

SIGNATURES = ["#Vira", "#yamone", "#Y", "#vin", "#ma_moe"]

def generate_trained_quote():
    examples = """
    ဥပမာ စာတိုပုံစံများ -
    - "အချစ်ဆိုတာ နာကျင်ရမှန်း ကျွန်တော်သိပ်သိတာပေါ့ ဒါမဲ့ မင်းမို့လို့ကို နာကျင်မှုတေ လစ်လျှူရှုပီး ချစ်နေတာပါ.."
    - "11:11 လွမ်းတယ်ယနေ့ မနေ့ကထက် ပိုလွမ်းသည်။"
    - "မချစ်တော့လို့ စွန့်လွှတ်ခဲ့ခြင်းမဟုတ်ပါဘူး.. ကိုယ်ရှိနေခြင်းက သူ့အတွက် ဝန်ထုပ်ဝန်ပိုးဖြစ်နေမှာစိုးလို့ ဆုပ်ကိုင်ထားတဲ့ လက်ကို အသာလေး လွှတ်ပေးခဲ့ယုံပါ...."
    - "ထွက်သွားမှာဆိုးလို့ ကိုယ့်မှာမေတ္တာသုတ်တောင် မရွတ်ခဲ့ပါဘူး အချစ်ရာ..."
    - "11:11 ဘဝရဲ့လက်တွဲဖော်ကို သည်းခံတတ်တဲ့သူကိုရွေးပါ"
    - "နေကောင်းအောင်နေနော်.. ထမင်းလဲအချိန်မှန်စား.. မဆက်သွယ်တော့တာ မချစ်တော့လို့ မဟုတ်ဘူးနော်"
    """

    selected_sig = random.choice(SIGNATURES)
    
    prompt = f"""
    သင်သည် Telegram အချစ်/အလွမ်း/ရင်ဖွင့် စာတို Channel တစ်ခု၏ Content Creator ဖြစ်သည်။
    ပေးထားသော ဥပမာ စာတိုများ၏ Style၊ Tone ကို အတိအကျ အတုယူ၍ စာတိုအသစ် ၁ ခု ရေးပေးပါ။

    {examples}

    စည်းကမ်းများ -
    ၁။ စာတိုသည် သဘာဝကျကျ ရင်ထဲက ထွက်လာသော စကားပြောဟန် ဖြစ်ရမည်။
    ၂။ တစ်ခါတစ်ရံ စာတိုအစ သို့မဟုတ် အလယ်တွင် '11:11' သို့မဟုတ် အချိန် (ဥပမာ - '12:00', '1:17') ထည့်ပေးပါ။
    ၃။ အပို စာများ လုံးဝ မပါရ။
    ၄။ စာတို အဆုံးတွင် {selected_sig} ကို အတိအကျ ထည့်ပေးပါ။
    """

    try:
        response = g4f_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a heartbroken, deep-emotional Myanmar telegram quote generator."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"G4F AI Generation Error: {e}")
        return None

async def main():
    logging.info("Telethon Bot Started...")
    while True:
        quote = generate_trained_quote()
        if quote:
            try:
                await client.send_message(CHANNEL_ID, quote)
                logging.info("Successfully sent quote via Telethon!")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
        
        # ၁ နာရီခွဲ တစ်ကြိမ် (၅၄၀၀ စက္ကန့်) စောင့်ရန်
        await asyncio.sleep(5400)

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
