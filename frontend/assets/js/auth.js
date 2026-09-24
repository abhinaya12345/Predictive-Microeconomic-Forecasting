// auth.js - handles login/signup/forgot/verify/reset
import { showToast } from "./utils.js";
import { signup, login, forgotPassword, verifyCode, resetPassword } from "./api.js";

// Helper: attach form submit
export function bindAuthForms() {
  // signup
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("su_name")?.value.trim();
      const email = document.getElementById("su_email")?.value.trim();
      const password = document.getElementById("su_password")?.value.trim();

      try {
        const data = await signup({ name, email, password });
        localStorage.setItem("bi_token", data.token);
        localStorage.setItem("bi_email", email);
        showToast("Signup successful ✅");
        window.location.href = "Set Up Your Business.html";
      } catch (err) {
        showToast(err.message || "Signup failed");
      }
    });
  }

  // login
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("li_email")?.value.trim();
      const password = document.getElementById("li_password")?.value.trim();

      try {
        const data = await login({ email, password });
        localStorage.setItem("bi_token", data.token);
        localStorage.setItem("bi_email", email);
        showToast("Login successful ✅");
        window.location.href = "Set Up Your Business.html";
      } catch (err) {
        showToast(err.message || "Login failed");
      }
    });
  }

  // forgot password
  const forgotForm = document.getElementById("forgotForm");
  if (forgotForm) {
    forgotForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("fp_email")?.value.trim();
      try {
        const data = await forgotPassword({ email });
        localStorage.setItem("bi_reset_email", email);

        // demo: backend returns code in response (for testing)
        localStorage.setItem("bi_reset_code_demo", data.demo_code || "");
        showToast("Verification code sent ✅ (demo)");
        window.location.href = "verification.html";
      } catch (err) {
        showToast(err.message || "Request failed");
      }
    });
  }

  // verify code page
  const verifyForm = document.getElementById("verifyForm");
  if (verifyForm) {
    verifyForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = localStorage.getItem("bi_reset_email") || "";
      const code = document.getElementById("ver_code")?.value.trim();
      try {
        await verifyCode({ email, code });
        showToast("Code verified ✅");
        window.location.href = "reset-password.html";
      } catch (err) {
        showToast(err.message || "Invalid code");
      }
    });
  }

  // reset password page
  const resetForm = document.getElementById("resetForm");
  if (resetForm) {
    resetForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = localStorage.getItem("bi_reset_email") || "";
      const code = document.getElementById("rp_code")?.value.trim();
      const new_password = document.getElementById("rp_newpass")?.value.trim();

      try {
        await resetPassword({ email, code, new_password });
        showToast("Password reset ✅");
        window.location.href = "login.html";
      } catch (err) {
        showToast(err.message || "Reset failed");
      }
    });
  }
}
