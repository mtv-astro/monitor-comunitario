const form = document.querySelector("#registration-form");
const formStatus = document.querySelector("#form-status");
const storedUserText = document.querySelector("#stored-user-text");
const lookupInput = document.querySelector("#lookup-user-id");
const loadNotificationsButton = document.querySelector("#load-notifications");
const notificationsList = document.querySelector("#notifications-list");

const consentBanner = document.querySelector("#consent-banner");
const consentBannerText = document.querySelector("#consent-banner-text");
const consentPreferences = document.querySelector("#consent-preferences");
const consentAnalyticsInput = document.querySelector("#consent-analytics");
const consentAdsInput = document.querySelector("#consent-ads");
const acceptConsentButton = document.querySelector("#accept-consent");
const rejectConsentButton = document.querySelector("#reject-consent");
const customizeConsentButton = document.querySelector("#customize-consent");
const saveConsentButton = document.querySelector("#save-consent");
const openConsentSettingsButton = document.querySelector("#open-consent-settings");

const storedUserKey = "monitor-comunitario:user";
const consentKey = "monitor-comunitario:consent";

let publicConfig = {
  ads_enabled: false,
  ads_provider: "placeholder",
  adsense_client_id: "",
  adsense_default_slot: "",
  analytics_enabled: false,
  analytics_provider: "none",
  google_analytics_id: "",
  consent_required: true,
  consent_version: "unknown",
};

function setStatus(message, isError = false) {
  formStatus.textContent = message;
  formStatus.classList.toggle("error", isError);
}

function setStoredUser(user) {
  window.localStorage.setItem(storedUserKey, JSON.stringify(user));
  renderStoredUser();
}

function getStoredUser() {
  const rawValue = window.localStorage.getItem(storedUserKey);

  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue);
  } catch {
    return null;
  }
}

function renderStoredUser() {
  const storedUser = getStoredUser();

  if (!storedUser) {
    storedUserText.textContent = "Nenhum cadastro salvo neste navegador.";
    return;
  }

  storedUserText.textContent = `Cadastro #${storedUser.id} — ${storedUser.name}, ${storedUser.municipality}`;
  lookupInput.value = storedUser.id;
}

function formToPayload(formElement) {
  const data = new FormData(formElement);

  return {
    name: String(data.get("name") || "").trim(),
    phone: String(data.get("phone") || "").trim(),
    municipality: String(data.get("municipality") || "").trim(),
    neighborhood: String(data.get("neighborhood") || "").trim(),
    street: String(data.get("street") || "").trim(),
    number: String(data.get("number") || "").trim(),
    zipcode: String(data.get("zipcode") || "").trim(),
    accept_municipality_wide_alerts: data.get("accept_municipality_wide_alerts") === "on",
  };
}

async function createUser(payload) {
  const response = await fetch("/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const body = await response.json();

  if (!response.ok) {
    throw new Error(body.detail || "Não foi possível salvar o cadastro.");
  }

  return body;
}

function renderNotifications(notifications) {
  notificationsList.innerHTML = "";

  if (!notifications.length) {
    const emptyState = document.createElement("div");
    emptyState.className = "empty-state";
    emptyState.textContent = "Nenhum alerta encontrado para este cadastro.";
    notificationsList.appendChild(emptyState);
    return;
  }

  for (const notification of notifications) {
    const card = document.createElement("article");
    card.className = "notification-card";

    const title = document.createElement("strong");
    title.textContent = notification.title;

    const date = document.createElement("small");
    date.textContent = new Date(notification.created_at).toLocaleString("pt-BR");

    const message = document.createElement("p");
    message.textContent = notification.message;

    card.append(title, date, message);
    notificationsList.appendChild(card);
  }
}

async function loadNotifications(userId) {
  notificationsList.innerHTML = "<div class=\"empty-state\">Carregando avisos...</div>";

  const response = await fetch(`/users/${userId}/notifications?limit=10`);
  const body = await response.json();

  if (!response.ok) {
    throw new Error(body.detail || "Não foi possível buscar avisos.");
  }

  renderNotifications(body);
}

async function loadPublicConfig() {
  try {
    const response = await fetch("/public/config");
    publicConfig = await response.json();
  } catch {
    publicConfig = {
      ...publicConfig,
      consent_required: true,
    };
  }
}

function getStoredConsent() {
  const rawValue = window.localStorage.getItem(consentKey);

  if (!rawValue) {
    return null;
  }

  try {
    const consent = JSON.parse(rawValue);

    if (consent.version !== publicConfig.consent_version) {
      return null;
    }

    return consent;
  } catch {
    return null;
  }
}

function persistConsent({ analytics, ads }) {
  const consent = {
    version: publicConfig.consent_version,
    necessary: true,
    analytics: Boolean(analytics),
    ads: Boolean(ads),
    saved_at: new Date().toISOString(),
  };

  window.localStorage.setItem(consentKey, JSON.stringify(consent));
  return consent;
}

function updateGoogleConsent(consent) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  window.gtag("consent", "update", {
    ad_storage: consent.ads ? "granted" : "denied",
    ad_user_data: consent.ads ? "granted" : "denied",
    ad_personalization: consent.ads ? "granted" : "denied",
    analytics_storage: consent.analytics ? "granted" : "denied",
  });
}

function setGoogleConsentDefaults() {
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  window.gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
  });
}

function injectScript({ id, src, async = true, crossOrigin = null }) {
  if (document.querySelector(`#${id}`)) {
    return;
  }

  const script = document.createElement("script");
  script.id = id;
  script.src = src;
  script.async = async;

  if (crossOrigin) {
    script.crossOrigin = crossOrigin;
  }

  document.head.appendChild(script);
}

function loadGoogleAnalytics(consent) {
  if (!publicConfig.analytics_enabled || !consent.analytics) {
    return;
  }

  if (
    publicConfig.analytics_provider !== "google_analytics" ||
    !publicConfig.google_analytics_id
  ) {
    return;
  }

  const tagId = publicConfig.google_analytics_id;

  injectScript({
    id: "google-analytics-script",
    src: `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(tagId)}`,
  });

  window.gtag("js", new Date());
  window.gtag("config", tagId);
}

function markAdSlots(message) {
  document.querySelectorAll(".ad-status").forEach((element) => {
    element.textContent = message;
  });
}

function loadGoogleAdsense(consent) {
  if (!publicConfig.ads_enabled || !consent.ads) {
    markAdSlots("Anúncio desativado ou aguardando consentimento.");
    return;
  }

  if (
    publicConfig.ads_provider !== "google_adsense" ||
    !publicConfig.adsense_client_id ||
    !publicConfig.adsense_default_slot
  ) {
    markAdSlots("Publicidade ativada por flag, mas sem provedor configurado.");
    return;
  }

  const clientId = publicConfig.adsense_client_id;

  injectScript({
    id: "google-adsense-script",
    src: `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(
      clientId,
    )}`,
    crossOrigin: "anonymous",
  });

  document.querySelectorAll(".ad-slot").forEach((slot) => {
    if (slot.querySelector(".adsbygoogle")) {
      return;
    }

    const adElement = document.createElement("ins");
    adElement.className = "adsbygoogle";
    adElement.style.display = "block";
    adElement.setAttribute("data-ad-client", clientId);
    adElement.setAttribute("data-ad-slot", publicConfig.adsense_default_slot);
    adElement.setAttribute("data-ad-format", "auto");
    adElement.setAttribute("data-full-width-responsive", "true");

    slot.appendChild(adElement);

    try {
      window.adsbygoogle = window.adsbygoogle || [];
      window.adsbygoogle.push({});
    } catch {
      markAdSlots("Publicidade ativada, mas o provedor ainda não respondeu.");
    }
  });

  markAdSlots("Publicidade ativada conforme consentimento.");
}

function applyConsent(consent) {
  updateGoogleConsent(consent);
  loadGoogleAnalytics(consent);
  loadGoogleAdsense(consent);
}

function showConsentBanner(force = false) {
  if (!consentBanner) {
    return;
  }

  const storedConsent = getStoredConsent();
  const needsMarketingConsent = publicConfig.ads_enabled || publicConfig.analytics_enabled;

  if (!force && storedConsent) {
    applyConsent(storedConsent);
    return;
  }

  if (!needsMarketingConsent) {
    const necessaryConsent = persistConsent({ analytics: false, ads: false });
    applyConsent(necessaryConsent);

    if (!force) {
      hideConsentBanner();
      return;
    }

    consentBannerText.textContent =
      "No momento, usamos apenas armazenamento local necessário para lembrar seu cadastro.";
    consentPreferences.hidden = true;
    saveConsentButton.hidden = true;
    customizeConsentButton.hidden = true;
    rejectConsentButton.hidden = true;
    acceptConsentButton.textContent = "Ok";
    consentBanner.classList.add("is-visible");
    return;
  }

  consentBannerText.textContent =
    "Ads e analytics só serão carregados conforme sua escolha.";
  customizeConsentButton.hidden = false;
  rejectConsentButton.hidden = false;
  acceptConsentButton.textContent = "Aceitar";
  consentBanner.classList.add("is-visible");
}

function hideConsentBanner() {
  consentBanner?.classList.remove("is-visible");
}

function saveConsentFromPreferences() {
  const consent = persistConsent({
    analytics: publicConfig.analytics_enabled && consentAnalyticsInput.checked,
    ads: publicConfig.ads_enabled && consentAdsInput.checked,
  });

  applyConsent(consent);
  hideConsentBanner();
}

function customizeConsent() {
  consentPreferences.hidden = false;
  saveConsentButton.hidden = false;
  acceptConsentButton.hidden = true;
}

function acceptAllConsent() {
  const consent = persistConsent({
    analytics: publicConfig.analytics_enabled,
    ads: publicConfig.ads_enabled,
  });

  applyConsent(consent);
  hideConsentBanner();
}

function rejectOptionalConsent() {
  const consent = persistConsent({
    analytics: false,
    ads: false,
  });

  applyConsent(consent);
  hideConsentBanner();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const legalTermsInput = document.querySelector("#accept_legal_terms");

  if (!legalTermsInput.checked) {
    setStatus("Para cadastrar, aceite os Termos de Uso e a Política de Privacidade.", true);
    return;
  }

  const payload = formToPayload(form);

  if (!payload.name || !payload.phone || !payload.municipality) {
    setStatus("Informe nome, telefone e município.", true);
    return;
  }

  setStatus("Salvando cadastro...");

  try {
    const user = await createUser(payload);
    setStoredUser(user);
    setStatus(`Cadastro salvo com sucesso. Seu ID é #${user.id}.`);
    await loadNotifications(user.id);
  } catch (error) {
    setStatus(error.message, true);
  }
});

loadNotificationsButton.addEventListener("click", async () => {
  const userId = Number(lookupInput.value);

  if (!userId) {
    notificationsList.innerHTML = "<div class=\"empty-state\">Informe o ID do cadastro.</div>";
    return;
  }

  try {
    await loadNotifications(userId);
  } catch (error) {
    notificationsList.innerHTML = `<div class="empty-state">${error.message}</div>`;
  }
});

acceptConsentButton?.addEventListener("click", acceptAllConsent);
rejectConsentButton?.addEventListener("click", rejectOptionalConsent);
customizeConsentButton?.addEventListener("click", customizeConsent);
saveConsentButton?.addEventListener("click", saveConsentFromPreferences);
openConsentSettingsButton?.addEventListener("click", () => showConsentBanner(true));

async function boot() {
  setGoogleConsentDefaults();
  await loadPublicConfig();

  renderStoredUser();
  showConsentBanner();

  const storedUser = getStoredUser();

  if (storedUser?.id) {
    loadNotifications(storedUser.id).catch(() => {
      notificationsList.innerHTML = "";
    });
  }
}

boot();
