import { useState } from "react";
import { X } from "lucide-react";

const SANDBOX_NUMBER = "14155238886";
const JOIN_CODE = "your-sandbox-code";

function WhatsAppIcon({ className = "h-8 w-8" }) {
  return (
    <svg
      viewBox="0 0 448 512"
      className={className}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32C101.5 32 1.9 131.6 1.9 254C1.9 293.1 12.1 331.3 31.5 365L0 480L117.7 449.1C150.1 466.8 186.6 476.1 223.8 476.1H223.9C346.2 476.1 448 376.5 448 254C448 194.7 422.9 139 380.9 97.1ZM223.9 438.7H223.8C190.6 438.7 158.1 429.8 129.8 413L123.1 409L53.3 427.3L71.6 359.5L67.2 352.5C48.7 323.1 39 289.2 39 254C39 152.3 121.8 69.5 223.6 69.5C272.9 69.5 319.2 88.7 354 123.6C388.8 158.5 408.1 204.8 408 254.1C408 355.8 325.1 438.7 223.9 438.7ZM325.1 300.5C319.6 297.7 292.3 284.3 287.2 282.4C282.1 280.5 278.4 279.6 274.7 285.2C271 290.8 260.4 303.2 257.2 306.9C254 310.6 250.7 311.1 245.2 308.3C212.6 292 191.2 275.2 169.7 238.3C164 228.5 175.4 229.4 186 208.2C187.8 204.5 186.9 201.3 185.5 198.5C184.1 195.7 173 168.4 168.4 157.3C163.9 146.5 159.3 148 155.9 147.8C152.7 147.6 149 147.6 145.3 147.6C141.6 147.6 135.6 149 130.5 154.6C125.4 160.2 111.1 173.6 111.1 200.9C111.1 228.2 131 254.6 133.7 258.3C136.5 262 172.8 318 228.5 342.1C263.7 357.3 277.5 358.6 295.1 356C305.8 354.4 327.9 342.6 332.5 329.6C337.1 316.6 337.1 305.5 335.7 303.2C334.4 300.7 330.6 299.3 325.1 296.5V300.5Z" />
    </svg>
  );
}

export function WhatsAppWidget() {
  const [open, setOpen] = useState(false);

  const joinUrl = `https://wa.me/${SANDBOX_NUMBER}?text=${encodeURIComponent(
    `join ${JOIN_CODE}`
  )}`;

  return (
    <div className="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-3">
      {open && (
        <div className="w-80 overflow-hidden rounded-2xl border border-blue-100 bg-white shadow-2xl">
          {/* Header */}
          <div className="flex items-center justify-between bg-blue-600 px-4 py-3 text-white">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20">
                <WhatsAppIcon className="h-5 w-5 text-white" />
              </div>

              <div>
                <p className="font-semibold">NIRIKSHAN Bot</p>
                <p className="text-xs text-blue-100">
                  WhatsApp Fraud Check
                </p>
              </div>
            </div>

            <button
              onClick={() => setOpen(false)}
              aria-label="Close"
              className="rounded-full p-1 transition hover:bg-white/20"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <div className="p-4">
            <p className="text-sm leading-6 text-gray-700">
              Forward any suspicious SEBI-related message to our WhatsApp bot
              and get an instant fraud check, in English or Hindi.
            </p>

            <p className="mt-3 text-xs leading-5 text-gray-500">
              Currently running on a test sandbox for this prototype, tap
              below to join and try it.
            </p>

            {/* WhatsApp Button */}
            <a
              href={joinUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 flex items-center justify-center gap-2 rounded-lg bg-[#25D366] px-3 py-2 text-sm font-semibold text-white transition hover:opacity-90"
            >
              <WhatsAppIcon className="h-4 w-4 text-white" />
              Chat on WhatsApp
            </a>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? "Close WhatsApp bot" : "Open WhatsApp bot"}
        className="flex h-[70px] w-[70px] items-center justify-center rounded-full bg-[#25D366] shadow-xl transition-transform duration-200 hover:scale-105"
      >
        {open ? (
          <X className="h-8 w-8 text-white" strokeWidth={2.5} />
        ) : (
          <WhatsAppIcon className="h-10 w-10 text-white" />
        )}
      </button>
    </div>
  );
}