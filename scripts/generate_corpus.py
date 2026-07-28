import csv
import os
import random

OUTPUT_FILE = "data/synthetic/text/corpus.csv"
random.seed(42)

NAMES = ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
         "Anjali Gupta", "Suresh Iyer", "Kavita Nair", "Manoj Verma", "Deepa Joshi"]

BROKERS = ["Zerodha", "Groww", "Upstox", "Angel One", "ICICI Direct", "HDFC Securities",
           "Kotak Securities", "Motilal Oswal", "5paisa", "Sharekhan"]

SCHEMES = ["SBI Bluechip Fund", "HDFC Top 100 Fund", "Axis Midcap Fund", "ICICI Prudential Value Fund",
           "Nippon India Small Cap Fund", "Mirae Asset Large Cap Fund", "UTI Nifty Index Fund"]

AMOUNTS = ["₹50,000", "₹1,00,000", "₹2,50,000", "₹75,000", "₹5,00,000", "₹25,000", "₹10,00,000"]

FAKE_CIRCULAR_NOS = ["SEBI/HO/2026/CIR/889", "SEBI/MIRSD/2026/4521", "SEBI/IMD/2026/7734",
                     "SEBI/CFD/2026/2298", "SEBI/HO/2026/CIR/5510"]

URGENCY_PHRASES_EN = ["Act now before it's too late", "Limited time offer, expires in 24 hours",
                      "This is your final notice", "Immediate action required",
                      "Only 3 slots remaining", "Offer valid till midnight tonight"]

URGENCY_PHRASES_HI = ["अभी कार्रवाई करें, समय समाप्त हो रहा है", "यह प्रस्ताव केवल 24 घंटे के लिए वैध है",
                      "यह आपकी अंतिम सूचना है", "तत्काल कार्रवाई आवश्यक है",
                      "केवल 3 स्थान शेष हैं", "यह प्रस्ताव आज मध्यरात्रि तक ही मान्य है"]

PHISHING_TEMPLATES_EN = [
    "Your {broker} account shows a pending dividend credit of ₹{amount} that requires verification. Click the link below and enter your net banking password to complete the process.",
    "A tax refund of ₹{amount} has been processed to your {broker} linked account. Please confirm your bank login details through the secure link to receive the amount.",
    "URGENT: SEBI Circular No. {circular} announces a special investor refund scheme. Transfer a processing fee of {amount} to claim your compensation of ₹5,00,000. {urgency}. Contact our SEBI-authorized agent immediately at the number provided.",
    "Congratulations {name}! You have been selected for a guaranteed 300% return scheme through {broker} partnership. Deposit {amount} today and double your money in 7 days. {urgency}",
    "This is to inform you that your demat account with {broker} will be suspended due to KYC mismatch. Click the link below and enter your login credentials and OTP immediately to avoid permanent suspension. {urgency}",
    "Insider tip: {scheme} is about to announce a bonus issue tomorrow. Buy now before the announcement using our exclusive trading signal. Send {amount} to unlock the premium tip group. {urgency}",
    "Dear Investor, as per SEBI directive {circular}, all pending dividend payments will be processed only after verification. Please share your bank account number, IFSC code and Aadhaar number to receive your pending amount of {amount}.",
    "SEBI Registered Advisor {name} guarantees assured returns of 15% monthly on your investment in {scheme}. This is a risk-free government-backed scheme. Invest {amount} now. {urgency}",
    "Your {broker} trading account shows unclaimed IPO allotment worth {amount}. Complete verification by clicking the link and entering your net banking password to claim your shares.",
    "Breaking: SEBI has approved a new wealth doubling scheme under circular {circular} exclusively for existing investors. Limited slots available. Pay a one-time registration fee of {amount} to enroll. {urgency}",
]

GENUINE_TEMPLATES_EN = [
    "Dear Investor, this is to inform you that the Net Asset Value (NAV) of {scheme} as on the last business day was updated on our website. For detailed portfolio holdings, please visit the AMC's official website.",
    "SEBI Circular {circular} dated today provides updated guidelines on the framework for transmission of securities in case of death of the sole holder. All Registrars to an Issue and Share Transfer Agents are advised to comply with the revised timelines.",
    "Your {broker} account statement for the current month has been generated and is available for download in the reports section of your dashboard. Please review your holdings and contact customer support for any discrepancies.",
    "This is a reminder that the KYC details linked to your demat account are due for periodic update as per regulatory requirements. Please visit your nearest {broker} branch or complete the update online through the official portal.",
    "As per SEBI regulations, all mutual fund houses are required to disclose portfolio holdings on a monthly basis. The updated factsheet for {scheme} for this month is now available on the AMC website.",
    "Dear {name}, your SIP installment of {amount} for {scheme} has been successfully processed. Your updated unit balance and folio statement will be sent to your registered email within 2 business days.",
    "SEBI has issued Circular {circular} regarding the certification requirements for distribution of Specialized Investment Funds. Intermediaries are advised to review the updated compliance framework.",
    "Your annual account maintenance charges for your demat account with {broker} will be debited as per the standard schedule. Please ensure sufficient balance in your linked bank account.",
    "This is to notify you that the settlement of trades executed on T+1 basis will be credited to your {broker} account by the end of the next trading day, in line with the revised settlement cycle norms.",
    "The Board of Directors has approved a corporate action involving a stock split in the ratio of 2:1, effective from the record date. Shareholders holding shares as on the record date will receive the additional shares in their demat account automatically.",
    "Dear {name}, a dividend of {amount} per share has been declared and will be credited directly to your registered bank account within 30 days from the date of declaration, subject to applicable tax deduction.",
    "The company has released its quarterly financial results, reporting a year-on-year growth in revenue. The detailed results and management commentary are available on the stock exchange website and the company's investor relations page.",
    "As per SEBI Circular {circular}, all listed companies are required to disclose related party transactions on a half-yearly basis. The disclosure for this period has been submitted to the stock exchanges.",
    "Your request for pledge creation on securities held with {broker} has been processed successfully. The pledged units are now reflected in your demat holdings statement under the encumbered securities section.",
    "This is to inform you that the record date for determining eligibility for the bonus issue announced by the company has been fixed. Please ensure your holdings are updated in your demat account before this date.",
    "SEBI Circular {circular} outlines the revised framework for processing of investor complaints through the SCORES platform, including timelines for resolution by market intermediaries.",
]

PHISHING_TEMPLATES_HI = [
    "आपके {broker} खाते में ₹{amount} का लाभांश जमा होना लंबित है, इसकी पुष्टि आवश्यक है। नीचे दिए गए लिंक पर क्लिक करें और अपना नेट बैंकिंग पासवर्ड दर्ज करके प्रक्रिया पूरी करें।",
    "आपके {broker} से जुड़े खाते में ₹{amount} का टैक्स रिफंड प्रोसेस किया गया है। कृपया राशि प्राप्त करने के लिए सुरक्षित लिंक के माध्यम से अपनी बैंक लॉगिन जानकारी की पुष्टि करें।",
    "अत्यावश्यक: सेबी परिपत्र संख्या {circular} के अनुसार एक विशेष निवेशक धनवापसी योजना की घोषणा की गई है। अपना मुआवजा ₹5,00,000 प्राप्त करने के लिए {amount} की प्रोसेसिंग फीस ट्रांसफर करें। {urgency} तुरंत हमारे सेबी-अधिकृत एजेंट से संपर्क करें।",
    "बधाई हो {name}! आपको {broker} की साझेदारी से 300% गारंटीड रिटर्न योजना के लिए चुना गया है। आज ही {amount} जमा करें और 7 दिनों में अपना पैसा दोगुना करें। {urgency}",
    "आपको सूचित किया जाता है कि KYC बेमेल के कारण {broker} में आपका डीमैट खाता निलंबित कर दिया जाएगा। स्थायी निलंबन से बचने के लिए नीचे दिए गए लिंक पर क्लिक करें और अपना लॉगिन विवरण और OTP तुरंत दर्ज करें। {urgency}",
    "इनसाइडर टिप: {scheme} कल एक बोनस इश्यू की घोषणा करने वाला है। घोषणा से पहले हमारे विशेष ट्रेडिंग सिग्नल का उपयोग करके अभी खरीदें। प्रीमियम टिप समूह को अनलॉक करने के लिए {amount} भेजें। {urgency}",
    "प्रिय निवेशक, सेबी निर्देश {circular} के अनुसार, सभी लंबित लाभांश भुगतान केवल सत्यापन के बाद संसाधित किए जाएंगे। अपनी लंबित राशि {amount} प्राप्त करने के लिए कृपया अपना बैंक खाता नंबर, IFSC कोड और आधार नंबर साझा करें।",
    "सेबी पंजीकृत सलाहकार {name} {scheme} में आपके निवेश पर 15% मासिक गारंटीड रिटर्न की गारंटी देते हैं। यह एक जोखिम-मुक्त सरकारी समर्थित योजना है। अभी {amount} निवेश करें। {urgency}",
    "आपके {broker} ट्रेडिंग खाते में {amount} मूल्य का अनक्लेम्ड IPO आवंटन दिखाया गया है। अपने शेयर दावा करने के लिए लिंक पर क्लिक करें और अपना नेट बैंकिंग पासवर्ड दर्ज करके सत्यापन पूरा करें।",
    "ब्रेकिंग: सेबी ने परिपत्र {circular} के तहत मौजूदा निवेशकों के लिए विशेष रूप से एक नई धन दोगुनी योजना को मंजूरी दी है। सीमित स्थान उपलब्ध हैं। नामांकन के लिए {amount} की एकमुश्त पंजीकरण शुल्क का भुगतान करें। {urgency}",
]

GENUINE_TEMPLATES_HI = [
    "प्रिय निवेशक, आपको सूचित किया जाता है कि {scheme} का निवल परिसंपत्ति मूल्य (NAV) पिछले कारोबारी दिन के अनुसार हमारी वेबसाइट पर अपडेट किया गया था। विस्तृत पोर्टफोलियो होल्डिंग्स के लिए, कृपया AMC की आधिकारिक वेबसाइट पर जाएं।",
    "आज दिनांकित सेबी परिपत्र {circular} एकमात्र धारक की मृत्यु के मामले में प्रतिभूतियों के हस्तांतरण के ढांचे पर अद्यतन दिशानिर्देश प्रदान करता है। सभी रजिस्ट्रार और शेयर ट्रांसफर एजेंटों को संशोधित समय-सीमा का पालन करने की सलाह दी जाती है।",
    "आपका {broker} खाता विवरण इस महीने के लिए तैयार किया गया है और आपके डैशबोर्ड के रिपोर्ट सेक्शन में डाउनलोड के लिए उपलब्ध है। कृपया अपनी होल्डिंग्स की समीक्षा करें और किसी भी विसंगति के लिए ग्राहक सहायता से संपर्क करें।",
    "यह एक अनुस्मारक है कि आपके डीमैट खाते से जुड़े KYC विवरण नियामक आवश्यकताओं के अनुसार आवधिक अद्यतन के लिए देय हैं। कृपया अपनी निकटतम {broker} शाखा में जाएं या आधिकारिक पोर्टल के माध्यम से ऑनलाइन अपडेट पूरा करें।",
    "सेबी नियमों के अनुसार, सभी म्यूचुअल फंड हाउसों को मासिक आधार पर पोर्टफोलियो होल्डिंग्स का खुलासा करना आवश्यक है। {scheme} के लिए इस महीने की अद्यतन फैक्टशीट अब AMC वेबसाइट पर उपलब्ध है।",
    "प्रिय {name}, {scheme} के लिए आपकी {amount} की SIP किस्त सफलतापूर्वक संसाधित हो गई है। आपका अद्यतन यूनिट बैलेंस और फोलियो स्टेटमेंट 2 कार्य दिवसों के भीतर आपके पंजीकृत ईमेल पर भेजा जाएगा।",
    "सेबी ने विशेष निवेश फंड के वितरण के लिए प्रमाणन आवश्यकताओं के संबंध में परिपत्र {circular} जारी किया है। मध्यस्थों को अद्यतन अनुपालन ढांचे की समीक्षा करने की सलाह दी जाती है।",
    "आपके {broker} डीमैट खाते के लिए वार्षिक खाता रखरखाव शुल्क मानक अनुसूची के अनुसार डेबिट किया जाएगा। कृपया सुनिश्चित करें कि आपके लिंक किए गए बैंक खाते में पर्याप्त शेष राशि हो।",
    "आपको सूचित किया जाता है कि T+1 आधार पर निष्पादित व्यापार का निपटान संशोधित निपटान चक्र मानदंडों के अनुसार अगले कारोबारी दिन के अंत तक आपके {broker} खाते में जमा कर दिया जाएगा।",
    "निदेशक मंडल ने 2:1 के अनुपात में स्टॉक विभाजन से जुड़ी एक कॉर्पोरेट कार्रवाई को मंजूरी दे दी है, जो रिकॉर्ड तिथि से प्रभावी होगी। रिकॉर्ड तिथि पर शेयर रखने वाले शेयरधारकों को अतिरिक्त शेयर स्वतः उनके डीमैट खाते में प्राप्त होंगे।",
    "प्रिय {name}, प्रति शेयर {amount} का लाभांश घोषित किया गया है और घोषणा की तारीख से 30 दिनों के भीतर, लागू कर कटौती के अधीन, सीधे आपके पंजीकृत बैंक खाते में जमा किया जाएगा।",
    "कंपनी ने अपने तिमाही वित्तीय परिणाम जारी किए हैं, जिसमें वार्षिक आधार पर राजस्व में वृद्धि दर्ज की गई है। विस्तृत परिणाम और प्रबंधन टिप्पणी स्टॉक एक्सचेंज वेबसाइट और कंपनी के निवेशक संबंध पृष्ठ पर उपलब्ध हैं।",
    "सेबी परिपत्र {circular} के अनुसार, सभी सूचीबद्ध कंपनियों को अर्ध-वार्षिक आधार पर संबंधित पक्ष लेनदेन का खुलासा करना आवश्यक है। इस अवधि के लिए खुलासा स्टॉक एक्सचेंजों को प्रस्तुत कर दिया गया है।",
    "{broker} के पास रखी गई प्रतिभूतियों पर प्रतिज्ञा निर्माण के लिए आपका अनुरोध सफलतापूर्वक संसाधित हो गया है। गिरवी रखी गई इकाइयां अब आपके डीमैट होल्डिंग्स स्टेटमेंट में एन्कम्बर्ड सिक्योरिटीज सेक्शन के तहत दिखाई दे रही हैं।",
    "आपको सूचित किया जाता है कि कंपनी द्वारा घोषित बोनस इश्यू के लिए पात्रता निर्धारित करने हेतु रिकॉर्ड तिथि तय कर दी गई है। कृपया सुनिश्चित करें कि इस तिथि से पहले आपकी होल्डिंग्स आपके डीमैट खाते में अद्यतन हों।",
    "सेबी परिपत्र {circular} SCORES प्लेटफॉर्म के माध्यम से निवेशक शिकायतों के प्रसंस्करण के लिए संशोधित ढांचे को रेखांकित करता है, जिसमें बाजार मध्यस्थों द्वारा समाधान की समय-सीमा शामिल है।",
]


def fill_template(template, urgency_pool):
    return template.format(
        name=random.choice(NAMES),
        broker=random.choice(BROKERS),
        scheme=random.choice(SCHEMES),
        amount=random.choice(AMOUNTS),
        circular=random.choice(FAKE_CIRCULAR_NOS),
        urgency=random.choice(urgency_pool)
    )


def generate_examples(templates, urgency_pool, count):
    examples = []
    seen = set()
    attempts = 0
    while len(examples) < count and attempts < count * 20:
        template_idx = random.randrange(len(templates))
        template = templates[template_idx]
        text = fill_template(template, urgency_pool)
        if text not in seen:
            seen.add(text)
            examples.append((text, template_idx))
        attempts += 1
    return examples

def generate_corpus():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    rows = []

    en_phishing = generate_examples(PHISHING_TEMPLATES_EN, URGENCY_PHRASES_EN, 200)
    for text, idx in en_phishing:
        rows.append([text, "phishing", "English", f"en_phishing_{idx}"])

    en_genuine = generate_examples(GENUINE_TEMPLATES_EN, [""], 200)
    for text, idx in en_genuine:
        rows.append([text, "genuine", "English", f"en_genuine_{idx}"])

    hi_phishing = generate_examples(PHISHING_TEMPLATES_HI, URGENCY_PHRASES_HI, 200)
    for text, idx in hi_phishing:
        rows.append([text, "phishing", "Hindi", f"hi_phishing_{idx}"])

    hi_genuine = generate_examples(GENUINE_TEMPLATES_HI, [""], 200)
    for text, idx in hi_genuine:
        rows.append([text, "genuine", "Hindi", f"hi_genuine_{idx}"])

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label", "language", "template_id"])
        writer.writerows(rows)

    print(f"Generated {len(rows)} total examples across {len(set(r[3] for r in rows))} unique templates")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_corpus()