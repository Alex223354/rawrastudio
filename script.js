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
    status.textContent = "Enviando...";

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(contactForm),
      });
      const result = await response.json();

      if (result.success) {
        status.textContent = "Gracias por tu mensaje. Te responderemos pronto.";
        contactForm.reset();
      } else {
        status.textContent = "No se pudo enviar el mensaje. Inténtalo de nuevo.";
      }
    } catch (error) {
      status.textContent = "No se pudo enviar el mensaje. Inténtalo de nuevo.";
    } finally {
      submitButton.disabled = false;
    }
  });
}

const heroVideo = document.querySelector(".hero-video");
const statementSection = document.querySelector(".statement");

if (heroVideo && statementSection) {
  // matches marble_done_at in assets/video/build_hero_video.py
  const AUTOSCROLL_DELAY_MS = 3600;
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
