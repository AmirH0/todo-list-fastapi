// frontend/js/auth.js

const API_BASE = "http://127.0.0.1:8000"; // ادرس بک‌اندت (در صورت نیاز تغییر بده)

const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const alertBox = document.getElementById("alert");

function showAlert(message, type = "error") {
    alertBox.classList.remove("hidden", "bg-red-100", "bg-green-100", "text-red-700", "text-green-700");
    if (type === "error") {
        alertBox.classList.add("bg-red-100", "text-red-700");
    } else {
        alertBox.classList.add("bg-green-100", "text-green-700");
    }
    alertBox.textContent = message;
    setTimeout(() => alertBox.classList.add("hidden"), 4000);
}

// تب‌ها
loginTab.addEventListener("click", () => {
    loginTab.classList.add("bg-indigo-600", "text-white");
    registerTab.classList.remove("bg-indigo-600", "text-white");
    registerTab.classList.add("bg-gray-100");
    registerForm.classList.add("hidden");
    loginForm.classList.remove("hidden");
});

registerTab.addEventListener("click", () => {
    registerTab.classList.add("bg-indigo-600", "text-white");
    loginTab.classList.remove("bg-indigo-600", "text-white");
    loginTab.classList.add("bg-gray-100");
    loginForm.classList.add("hidden");
    registerForm.classList.remove("hidden");
});

// لینک‌ها بین فرم‌ها
document.getElementById("toRegister").addEventListener("click", () => registerTab.click());
document.getElementById("toLogin").addEventListener("click", () => loginTab.click());

// ثبت‌نام
registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("regUsername").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value;
    const passwordConfirm = document.getElementById("regPasswordConfirm").value;

    if (password !== passwordConfirm) {
        showAlert("رمز و تأیید آن یکسان نیست.", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/users/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            showAlert(err.detail || "خطا در ثبت‌نام", "error");
            return;
        }

        const data = await res.json();
        showAlert("ثبت‌نام موفق! می‌تونی وارد شی.", "success");
        // بعد از ثبت‌نام اتومات سوئیچ به تب ورود
        setTimeout(() => loginTab.click(), 800);
    } catch (error) {
        showAlert("ارتباط با سرور برقرار نشد.", "error");
        console.error(error);
    }
});

// لاگین
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
        const res = await fetch(`${API_BASE}/users/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            showAlert(err.detail || "خطا در ورود", "error");
            return;
        }

        const data = await res.json();
        // پاسخ ما: { access_token, token_type }
        if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            showAlert("ورود موفق! در حال انتقال...", "success");
            setTimeout(() => {
                window.location.href = "todos.html";
            }, 600);
        } else {
            showAlert("توکن دریافت نشد.", "error");
        }
    } catch (error) {
        showAlert("ارتباط با سرور برقرار نشد.", "error");
        console.error(error);
    }
});
