// GET /api/locate — returns the visitor's country code and a suggested currency.
// Uses Cloudflare's automatic geo headers — no external API needed.

const COUNTRY_TO_CURRENCY = {
  US: "USD", PR: "USD", GU: "USD", VI: "USD", AS: "USD", MP: "USD", EC: "USD", SV: "USD", PA: "USD", TL: "USD", ZW: "USD",
  CA: "CAD",
  GB: "GBP", IM: "GBP", JE: "GBP", GG: "GBP",
  AU: "AUD", CX: "AUD", CC: "AUD", NF: "AUD", NR: "AUD", KI: "AUD", TV: "AUD",
  NZ: "NZD", CK: "NZD", NU: "NZD", PN: "NZD", TK: "NZD",
  CH: "CHF", LI: "CHF",
  JP: "JPY",
  CN: "CNY",
  HK: "HKD",
  TW: "TWD",
  SG: "SGD",
  AE: "AED",
  SA: "SAR",
  QA: "QAR",
  KW: "KWD",
  BH: "BHD",
  OM: "OMR",
  IL: "ILS",
  IN: "INR", BT: "INR",
  TH: "THB",
  MY: "MYR",
  ID: "IDR",
  PH: "PHP",
  VN: "VND",
  KR: "KRW",
  KH: "USD",
  LA: "USD",
  MM: "USD",
  BD: "BDT",
  PK: "PKR",
  LK: "LKR",
  NP: "NPR",
  MX: "MXN",
  BR: "BRL",
  AR: "ARS",
  CL: "CLP",
  CO: "COP",
  PE: "PEN",
  UY: "UYU",
  PY: "PYG",
  BO: "BOB",
  VE: "VES",
  CR: "CRC",
  GT: "GTQ",
  HN: "HNL",
  NI: "NIO",
  DO: "DOP",
  CU: "CUP",
  TT: "TTD",
  JM: "JMD",
  BB: "BBD",
  ZA: "ZAR",
  NG: "NGN",
  KE: "KES",
  EG: "EGP",
  MA: "MAD",
  TN: "TND",
  DZ: "DZD",
  ET: "ETB",
  GH: "GHS",
  TZ: "TZS",
  UG: "UGX",
  RW: "RWF",
  TR: "TRY",
  RU: "RUB",
  UA: "UAH",
  BY: "BYN",
  KZ: "KZT",
  GE: "GEL",
  AM: "AMD",
  AZ: "AZN",
  // Eurozone
  AT: "EUR", BE: "EUR", CY: "EUR", DE: "EUR", EE: "EUR", ES: "EUR", FI: "EUR", FR: "EUR", GR: "EUR", IE: "EUR",
  IT: "EUR", LT: "EUR", LU: "EUR", LV: "EUR", MT: "EUR", NL: "EUR", PT: "EUR", SI: "EUR", SK: "EUR", HR: "EUR",
  AD: "EUR", MC: "EUR", SM: "EUR", VA: "EUR", ME: "EUR", XK: "EUR",
  // EU non-euro
  SE: "SEK", DK: "DKK", NO: "NOK", IS: "ISK",
  PL: "PLN", CZ: "CZK", HU: "HUF", RO: "RON", BG: "BGN", AL: "ALL",
  RS: "RSD", BA: "BAM", MK: "MKD", MD: "MDL",
};

const COUNTRY_TO_CITY = {
  US: "New York", CA: "Toronto", MX: "Mexico City", GB: "London", IE: "Dublin",
  FR: "Paris", DE: "Berlin", ES: "Madrid", IT: "Rome", PT: "Lisbon", NL: "Amsterdam",
  BE: "Brussels", AT: "Vienna", CH: "Zurich", SE: "Stockholm", NO: "Oslo", DK: "Copenhagen",
  FI: "Helsinki", PL: "Warsaw", CZ: "Prague", HU: "Budapest", GR: "Athens", TR: "Istanbul",
  RO: "Bucharest", HR: "Split", EE: "Tallinn", LV: "Riga",
  AU: "Sydney", NZ: "Auckland",
  JP: "Tokyo", CN: "Shanghai", HK: "Hong Kong", TW: "Taipei", KR: "Seoul",
  SG: "Singapore", TH: "Bangkok", MY: "Kuala Lumpur", ID: "Jakarta", VN: "Ho Chi Minh City",
  PH: "Manila", IN: "Mumbai",
  AE: "Dubai", SA: "Riyadh", QA: "Doha", IL: "Tel Aviv",
  ZA: "Cape Town", NG: "Lagos", KE: "Nairobi", EG: "Cairo", MA: "Marrakech",
  BR: "São Paulo", AR: "Buenos Aires", CL: "Santiago", CO: "Bogotá", PE: "Lima", UY: "Montevideo",
};

export async function onRequestGet(context) {
  const { request } = context;
  const country = request.cf?.country || request.headers.get("CF-IPCountry") || "";
  const city = request.cf?.city || "";
  const timezone = request.cf?.timezone || "";

  return new Response(
    JSON.stringify({
      country,
      city,
      timezone,
      suggestedCurrency: COUNTRY_TO_CURRENCY[country] || null,
      suggestedCity: COUNTRY_TO_CITY[country] || null,
    }),
    {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300",
        "Access-Control-Allow-Origin": "*",
      },
    }
  );
}
