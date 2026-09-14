document.getElementById("year").textContent = new Date().getFullYear();

const navToggle = document.querySelector(".nav-toggle");
const mainNav = document.querySelector(".main-nav");

if (navToggle && mainNav) {
  navToggle.addEventListener("click", () => {
    mainNav.classList.toggle("open");
  });

  mainNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => mainNav.classList.remove("open"));
  });
}

const contactForm = document.getElementById("contact-form");

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    let status = contactForm.querySelector(".form-status");
    if (!status) {
      status = document.createElement("p");
      status.className = "form-status";
      contactForm.appendChild(status);
    }

    status.textContent = "Gracias por tu mensaje. Te responderemos pronto.";
    contactForm.reset();
  });
}

const COOKIE_CONSENT_KEY = "rawra_cookie_consent";
const cookieBanner = document.getElementById("cookie-banner");

if (cookieBanner) {
  const consent = localStorage.getItem(COOKIE_CONSENT_KEY);

  if (!consent) {
    requestAnimationFrame(() => cookieBanner.classList.add("visible"));
  }

  const hideBanner = (value) => {
    localStorage.setItem(COOKIE_CONSENT_KEY, value);
    cookieBanner.classList.remove("visible");
  };

  document.getElementById("cookie-accept").addEventListener("click", () => hideBanner("accepted"));
  document.getElementById("cookie-reject").addEventListener("click", () => hideBanner("rejected"));
}
