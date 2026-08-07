export type Band = "Safe" | "Low Risk" | "Medium Risk" | "High Risk";

export type Match = {
  title: string;
  date: string;
  distance: number;
  source_url: string;
};

export type AnalysisResult = {
  text_risk: number;
  auth_trust: number;
  claims_sebi_origin: boolean;
  trust_score: number;
  band: Band;
  matches: Match[];
};

export type Mode = "text" | "audio" | "video";
export type Lang = "en" | "hi";

export const MAX_FILE_MB = 25;

export const ACCEPTED: Record<Exclude<Mode, "text">, { exts: string[]; label: string }> = {
  audio: { exts: [".mp3", ".wav", ".m4a", ".ogg"], label: "MP3, WAV, M4A, OGG" },
  video: { exts: [".mp4", ".mov", ".webm"], label: "MP4, MOV, WEBM" },
};

export const EXAMPLES: { id: string; label: Record<Lang, string>; text: string }[] = [
  {
    id: "fake-circular",
    label: { en: "Fake SEBI circular", hi: "नकली सेबी परिपत्र" },
    text: "SEBI Circular No. SEBI/MIRSD/2026/4521 - You have an unclaimed refund, click here and enter your net banking password to claim.",
  },
  {
    id: "genuine",
    label: { en: "Genuine SEBI notice", hi: "असली सेबी सूचना" },
    text: "SEBI Master Circular for Know Your Client (KYC) norms for the securities market, consolidating provisions for intermediaries. Available at sebi.gov.in/legal/circulars.",
  },
  {
    id: "whatsapp",
    label: { en: "WhatsApp scam", hi: "व्हाट्सएप घोटाला" },
    text: "Join our VIP stock group! Guaranteed 300% return in 7 days on this SEBI-approved multibagger. Pay registration fee to this UPI ID immediately, limited seats.",
  },
];

const demoHigh: AnalysisResult = {
  text_risk: 0.996,
  auth_trust: 0.412,
  claims_sebi_origin: true,
  trust_score: 25,
  band: "High Risk",
  matches: [
    {
      title: "Redressal of investor grievances through the SEBI Complaint Redressal (SCORES) Platform",
      date: "2023-09-20",
      distance: 0.76,
      source_url: "https://www.sebi.gov.in/legal/circulars",
    },
    {
      title: "Facility to remedy erroneous transfers in demat accounts",
      date: "2023-08-08",
      distance: 0.74,
      source_url: "https://www.sebi.gov.in/legal/circulars",
    },
  ],
};

const demoSafe: AnalysisResult = {
  text_risk: 0.012,
  auth_trust: 0.988,
  claims_sebi_origin: true,
  trust_score: 96,
  band: "Safe",
  matches: [
    {
      title: "SEBI Master Circular - KYC Norms for the Securities Market",
      date: "2024-05-15",
      distance: 0.99,
      source_url: "https://www.sebi.gov.in/legal/master-circulars",
    },
  ],
};

const demoMedium: AnalysisResult = {
  text_risk: 0.58,
  auth_trust: 0.61,
  claims_sebi_origin: false,
  trust_score: 54,
  band: "Medium Risk",
  matches: [],
};

/** Very small heuristic used only to pick a plausible demo payload offline. */
export function demoResultFor(input: string): AnalysisResult {
  const t = input.toLowerCase();
  const scammy = /(password|otp|click here|guaranteed|upi|urgent|refund|multibagger|limited seats)/.test(t);
  const official = /(master circular|sebi\.gov\.in|kyc norms|consolidating)/.test(t);
  if (scammy) return demoHigh;
  if (official) return demoSafe;
  return demoMedium;
}

export function bandOfScore(score: number): Band {
  if (score >= 85) return "Safe";
  if (score >= 65) return "Low Risk";
  if (score >= 40) return "Medium Risk";
  return "High Risk";
}

export const GUIDANCE: Record<Band, Record<Lang, string[]>> = {
  Safe: {
    en: [
      "Content aligns with verified SEBI records — you may proceed normally.",
      "Still verify the sender's identity before acting on financial instructions.",
      "Cross-check the matched circular at sebi.gov.in/legal/circulars.",
    ],
    hi: [
      "सामग्री सत्यापित सेबी रिकॉर्ड से मेल खाती है — आप सामान्य रूप से आगे बढ़ सकते हैं।",
      "वित्तीय निर्देशों पर कार्य करने से पहले भेजने वाले की पहचान जांचें।",
      "मिलान किए गए परिपत्र की पुष्टि sebi.gov.in/legal/circulars पर करें।",
    ],
  },
  "Low Risk": {
    en: [
      "No strong phishing signals detected, but the match is partial.",
      "Confirm the circular number directly on the SEBI website.",
      "Never share OTP, password, or bank details over any channel.",
    ],
    hi: [
      "कोई मजबूत फ़िशिंग संकेत नहीं मिला, लेकिन मिलान आंशिक है।",
      "परिपत्र संख्या की पुष्टि सीधे सेबी वेबसाइट पर करें।",
      "OTP, पासवर्ड या बैंक विवरण कभी साझा न करें।",
    ],
  },
  "Medium Risk": {
    en: [
      "Treat this communication as unverified until confirmed.",
      "Do not click links; navigate to sebi.gov.in manually instead.",
      "Ask your registered broker to confirm through official channels.",
    ],
    hi: [
      "पुष्टि होने तक इस संदेश को असत्यापित मानें।",
      "लिंक पर क्लिक न करें; सीधे sebi.gov.in पर जाएं।",
      "अपने पंजीकृत ब्रोकर से आधिकारिक माध्यम से पुष्टि कराएं।",
    ],
  },
  "High Risk": {
    en: [
      "Do not click any links in this message.",
      "Do not share your OTP, password, or bank details.",
      "Block this sender's number or email address.",
      "Verify any claimed circular directly at sebi.gov.in/legal/circulars.",
    ],
    hi: [
      "इस संदेश में किसी भी लिंक पर क्लिक न करें।",
      "अपना OTP, पासवर्ड या बैंक विवरण साझा न करें।",
      "इस भेजने वाले का नंबर या ईमेल ब्लॉक करें।",
      "किसी भी दावा किए गए परिपत्र की पुष्टि sebi.gov.in/legal/circulars पर करें।",
    ],
  },
};

export const T = {
  tagline: {
    en: "Regulatory verification and threat scoring for suspicious investor communications.",
    hi: "संदिग्ध निवेशक संदेशों के लिए नियामक सत्यापन और जोखिम स्कोरिंग।",
  },
  engine: { en: "Message Analysis Engine", hi: "संदेश विश्लेषण इंजन" },
  analyze: { en: "Analyze Message", hi: "संदेश का विश्लेषण करें" },
  analyzing: { en: "Analyzing…", hi: "विश्लेषण जारी…" },
  checkAnother: { en: "Check Another", hi: "दूसरा जांचें" },
  tryExample: { en: "Try an example", hi: "उदाहरण आज़माएं" },
  verdict: { en: "Verdict", hi: "निर्णय" },
  trustScore: { en: "Overall Trust Score", hi: "कुल विश्वास स्कोर" },
  breakdown: { en: "Analysis Breakdown", hi: "विश्लेषण विवरण" },
  phishing: { en: "Phishing Language Risk", hi: "फ़िशिंग भाषा जोखिम" },
  authenticity: { en: "Authenticity Match", hi: "प्रामाणिकता मिलान" },
  claims: { en: "Claims SEBI Origin", hi: "सेबी मूल का दावा" },
  yes: { en: "Yes", hi: "हाँ" },
  no: { en: "No", hi: "नहीं" },
  matched: { en: "Matched Official Circulars", hi: "मिलान किए गए आधिकारिक परिपत्र" },
  noMatch: { en: "No matching circular found", hi: "कोई मेल खाता परिपत्र नहीं मिला" },
  noMatchBody: {
    en: "This communication does not correspond to any circular in the reference database. Absence of a match is itself a signal — genuine regulatory notices are almost always published.",
    hi: "यह संदेश संदर्भ डेटाबेस के किसी परिपत्र से मेल नहीं खाता। मिलान न होना स्वयं एक संकेत है — असली नियामक सूचनाएँ लगभग हमेशा प्रकाशित होती हैं।",
  },
  document: { en: "Reference document", hi: "संदर्भ दस्तावेज़" },
  date: { en: "Date", hi: "दिनांक" },
  relevance: { en: "Relevance", hi: "प्रासंगिकता" },
  whatToDo: { en: "Recommended next steps", hi: "अनुशंसित अगले कदम" },
  helpline: {
    en: "If you have been targeted, report it: SEBI Investor Helpline 1800 266 7575",
    hi: "यदि आप निशाना बने हैं, तो रिपोर्ट करें: सेबी निवेशक हेल्पलाइन 1800 266 7575",
  },
  helplineLink: { en: "File a complaint on SCORES", hi: "SCORES पर शिकायत दर्ज करें" },
  demoNote: {
    en: "Demo mode — live analysis requires the local backend. Showing an example result; see the demo video for the working system.",
    hi: "डेमो मोड — लाइव विश्लेषण के लिए स्थानीय बैकएंड आवश्यक है। यह एक उदाहरण परिणाम है; कार्यशील सिस्टम के लिए डेमो वीडियो देखें।",
  },
  emptyInput: { en: "Enter a message to analyze.", hi: "विश्लेषण के लिए एक संदेश दर्ज करें।" },
  emptyFile: { en: "Select a file to analyze.", hi: "विश्लेषण के लिए एक फ़ाइल चुनें।" },
  dropzone: { en: "Drag and drop, or browse", hi: "खींचें और छोड़ें, या ब्राउज़ करें" },
  hintEnter: { en: "Press Enter to analyze, Shift + Enter for a new line.", hi: "विश्लेषण के लिए Enter दबाएँ, नई पंक्ति के लिए Shift + Enter।" },
} as const;

export const LOADING_STEPS: Record<Lang, string[]> = {
  en: [
    "Reading the message…",
    "Comparing against the SEBI circular database…",
    "Scoring phishing language patterns…",
  ],
  hi: [
    "संदेश पढ़ा जा रहा है…",
    "सेबी परिपत्र डेटाबेस से तुलना…",
    "फ़िशिंग भाषा पैटर्न का आकलन…",
  ],
};
