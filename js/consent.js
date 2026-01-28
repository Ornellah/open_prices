function setConsent(value) {
    document.cookie = "cookie_consent=" + value + "; path=/; max-age=31536000";
  }
  
function getConsent() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('cookie_consent='))
    ?.split('=')[1];
}

function showCookieBanner() {
  const consent = getConsent();
  if (consent) return;

  const banner = document.createElement("div");
  banner.id = "cookie-banner";
  banner.style = "position:fixed; bottom:0; width:100%; background:#fff; padding:15px; border-top:1px solid #ddd; z-index:9999;";

  banner.innerHTML = `
    Ce site utilise Google Analytics.
    <button id="cookie-accept">Accepter</button>
    <button id="cookie-decline">Refuser</button>
  `;

  document.body.appendChild(banner);

  document.getElementById("cookie-accept").onclick = () => {
    setConsent("granted");
    banner.remove();
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "cookie_consent_granted" });
  };

  document.getElementById("cookie-decline").onclick = () => {
    setConsent("denied");
    banner.remove();
  };
}

window.addEventListener("DOMContentLoaded", showCookieBanner);  