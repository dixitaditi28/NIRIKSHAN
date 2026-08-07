import { AlertTriangle, CheckCircle2, Info, ShieldAlert, type LucideIcon } from "lucide-react";
import type { Band, Lang } from "@/lib/nirikshan";

export type BandStyle = {
  icon: LucideIcon;
  text: string;
  bg: string;
  border: string;
  bar: string;
  label: Record<Lang, string>;
  headline: Record<Lang, string>;
};

export const BAND_STYLES: Record<Band, BandStyle> = {
  Safe: {
    icon: CheckCircle2,
    text: "text-success",
    bg: "bg-success/15",
    border: "border-success",
    bar: "bg-success",
    label: { en: "Safe", hi: "सुरक्षित" },
    headline: {
      en: "Content aligns closely with verified SEBI records.",
      hi: "सामग्री सत्यापित सेबी रिकॉर्ड से निकटता से मेल खाती है।",
    },
  },
  "Low Risk": {
    icon: Info,
    text: "text-info",
    bg: "bg-info/15",
    border: "border-info",
    bar: "bg-info",
    label: { en: "Low Risk", hi: "कम जोखिम" },
    headline: {
      en: "Mostly consistent with official communications, with minor gaps.",
      hi: "अधिकतर आधिकारिक संदेशों के अनुरूप, कुछ अंतर के साथ।",
    },
  },
  "Medium Risk": {
    icon: AlertTriangle,
    text: "text-warning",
    bg: "bg-warning/15",
    border: "border-warning",
    bar: "bg-warning",
    label: { en: "Medium Risk", hi: "मध्यम जोखिम" },
    headline: {
      en: "Unverified. Some signals do not match known regulatory sources.",
      hi: "असत्यापित। कुछ संकेत ज्ञात नियामक स्रोतों से मेल नहीं खाते।",
    },
  },
  "High Risk": {
    icon: ShieldAlert,
    text: "text-danger",
    bg: "bg-danger/15",
    border: "border-danger",
    bar: "bg-danger",
    label: { en: "High Risk", hi: "उच्च जोखिम" },
    headline: {
      en: "Strong phishing signals detected. Do not act on this message.",
      hi: "मजबूत फ़िशिंग संकेत मिले। इस संदेश पर कार्य न करें।",
    },
  },
};