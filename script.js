document.getElementById("year").textContent = new Date().getFullYear();

// ---- Language switch (ES/EN) ----
const LANG_KEY = "rawra_lang";

const translatableEls = document.querySelectorAll("[data-en]");
translatableEls.forEach((el) => {
  if (!el.dataset.es) el.dataset.es = el.textContent;
});

const placeholderEls = document.querySelectorAll("[data-en-placeholder]");
placeholderEls.forEach((el) => {
  if (!el.dataset.esPlaceholder) {
    el.dataset.esPlaceholder = el.getAttribute("placeholder") || "";
  }
});

function currentLang() {
  return localStorage.getItem(LANG_KEY) || "es";
}

function applyLanguage(lang) {
  translatableEls.forEach((el) => {
    el.textContent = lang === "en" ? el.dataset.en : el.dataset.es;
  });
  placeholderEls.forEach((el) => {
    el.setAttribute(
      "placeholder",
      lang === "en" ? el.dataset.enPlaceholder : el.dataset.esPlaceholder
    );
  });
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-lang-btn]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.langBtn === lang);
  });
  localStorage.setItem(LANG_KEY, lang);
}

document.querySelectorAll("[data-lang-btn]").forEach((btn) => {
  btn.addEventListener("click", () => applyLanguage(btn.dataset.langBtn));
});

applyLanguage(currentLang());

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

const FORM_MESSAGES = {
  sending: { es: "Enviando...", en: "Sending..." },
  success: {
    es: "Gracias por tu mensaje. Te responderemos pronto.",
    en: "Thanks for your message. We'll get back to you soon.",
  },
  error: {
    es: "No se pudo enviar el mensaje. Inténtalo de nuevo.",
    en: "Couldn't send the message. Please try again.",
  },
};

if (contactForm) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    let status = contactForm.querySelector(".form-status");
    if (!status) {
      status = document.createElement("p");
      status.className = "form-status";
      contactForm.appendChild(status);
    }

    const submitButton = contactForm.querySelector("button[type=submit]");
    submitButton.disabled = true;
    status.textContent = FORM_MESSAGES.sending[currentLang()];

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(contactForm),
      });
      const result = await response.json();

      if (result.success) {
        status.textContent = FORM_MESSAGES.success[currentLang()];
        contactForm.reset();
      } else {
        status.textContent = FORM_MESSAGES.error[currentLang()];
      }
    } catch (error) {
      status.textContent = FORM_MESSAGES.error[currentLang()];
    } finally {
      submitButton.disabled = false;
    }
  });
}

const heroVideo = document.querySelector(".hero-video");
const statementSection = document.querySelector(".statement");

if (heroVideo && statementSection) {
  // matches total_duration in assets/video/build_hero_video.py -- scrolls
  // right as the reel finishes its first full play, before it loops
  const AUTOSCROLL_DELAY_MS = 12000;
  setTimeout(() => {
    if (window.scrollY < 50) {
      statementSection.scrollIntoView({ behavior: "smooth" });
    }
  }, AUTOSCROLL_DELAY_MS);
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
