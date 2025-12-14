// =======================
// ثبت‌نام کاربر
// =======================
const registerForm = document.getElementById("register-form");
const registerMsg = document.getElementById("register-message");

if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    e.preventDefault();

    registerMsg.textContent = "در حال ارسال...";
    registerMsg.className = "mt-2 small text-muted";

    const formData = new FormData(registerForm);
    const data = {
      username: formData.get("username"),
      first_name: formData.get("first_name"),
      last_name: formData.get("last_name"),
      phone_number: formData.get("phone_number"),
      email: formData.get("email"),
      password: formData.get("password"),
    };

    fetch("http://localhost:8000/api/users/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(await res.text());
        return res.json();
      })
      .then(() => {
        registerMsg.textContent = "✅ ثبت‌نام با موفقیت انجام شد";
        registerMsg.className = "mt-2 small text-success";
        registerForm.reset();
      })
      .catch((err) => {
        registerMsg.textContent = "❌ خطا: " + err.message;
        registerMsg.className = "mt-2 small text-danger";
      });
  });
}

// =======================
// لاگین کاربر
// =======================
const loginForm = document.getElementById("login-form");
const loginMsg = document.getElementById("login-message");

if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();

    loginMsg.textContent = "در حال ورود...";
    loginMsg.className = "mt-2 small text-muted";

    const formData = new FormData(loginForm);
    const data = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    fetch("http://localhost:8000/api/users/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(await res.text());
        return res.json();
      })
      .then((json) => {
        localStorage.setItem("access_token", json.access);
        localStorage.setItem("refresh_token", json.refresh);

        loginMsg.textContent = "✅ ورود موفقیت‌آمیز بود";
        window.location.href = "subscriptions.html";
        loginMsg.className = "mt-2 small text-success";
        loginForm.reset();

        loadSubscriptions();
      })
      .catch((err) => {
        loginMsg.textContent = "❌ خطا: " + err.message;
        loginMsg.className = "mt-2 small text-danger";
      });
  });
}

// =======================
// محصولات
// =======================
const productsContainer = document.getElementById("products");

if (productsContainer) {
  fetch("http://localhost:8000/api/products/")
    .then((res) => res.json())
    .then((data) => {
      const products = data.results || data;

      if (!products.length) {
        productsContainer.innerHTML = `
          <div class="alert alert-warning text-center">
            هیچ محصولی ثبت نشده است.
          </div>
        `;
        return;
      }

      products.forEach((product) => {
        const card = document.createElement("div");
        card.className = "col-md-4";

        card.innerHTML = `
          <div class="card product-card shadow-sm h-100">
            <img src="${product.avatar || ''}" class="card-img-top">

            <div class="card-body">
              <h5>${product.title}</h5>
              <p>${(product.description || "").substring(0, 80)}...</p>

              <h6>دسته‌بندی‌ها:</h6>
              <ul>
                ${
                  product.categories?.length
                    ? product.categories.map((c) => `<li>${c.title}</li>`).join("")
                    : "<li>ندارد</li>"
                }
              </ul>

              <h6>فایل‌ها:</h6>
              <ul>
                ${
                  product.files?.length
                    ? product.files
                        .map(
                          (f) =>
                            `<li><a href="${f.file}" target="_blank">${f.title}</a></li>`
                        )
                        .join("")
                    : "<li>ندارد</li>"
                }
              </ul>
            </div>
          </div>
        `;

        productsContainer.appendChild(card);
      });
    })
    .catch(() => {
      productsContainer.innerHTML = `
        <div class="alert alert-danger text-center">
          خطا در دریافت محصولات
        </div>
      `;
    });
}

// =======================
// پکیج‌ها + خرید
// =======================
const packagesContainer = document.getElementById("packages");

if (packagesContainer) {
  fetch("http://localhost:8000/sub/packages/")
    .then((res) => res.json())
    .then((data) => {
      if (!data.length) {
        packagesContainer.innerHTML = `
          <div class="alert alert-info text-center">
            هیچ پکیجی موجود نیست.
          </div>
        `;
        return;
      }

      data.forEach((pkg) => {
        const card = document.createElement("div");
        card.className = "col-md-4";

        card.innerHTML = `
          <div class="card shadow-sm h-100">
            <img src="${pkg.avatar || ''}" class="card-img-top" style="height:200px;object-fit:cover;">
            <div class="card-body">
              <h5>${pkg.title}</h5>
              <p>${pkg.description}</p>
              <p><strong>قیمت:</strong> ${pkg.price} تومان</p>
              <button class="btn btn-primary w-100 buy-package-btn" data-id="${pkg.id}">
                خرید پکیج
              </button>
            </div>
          </div>
        `;

        packagesContainer.appendChild(card);
      });

      document.querySelectorAll(".buy-package-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
          const token = localStorage.getItem("access_token");
          const packageId = this.dataset.id;

          if (!token) {
            const modal = new bootstrap.Modal(
              document.getElementById("login-popup")
            );
            modal.show();
            return;
          }

          // 1) گرفتن گیت‌وی‌ها
          fetch("http://localhost:8000/payment/gateway/")
            .then((res) => res.json())
            .then((gateways) => {
              if (!gateways.length) {
                alert("هیچ درگاه فعالی وجود ندارد");
                return;
              }

              const gatewayId = gateways[0].id;

              // 2) ساخت پرداخت
              return fetch(
                `http://localhost:8000/payment/payment/?gateway=${gatewayId}&package=${packageId}`,
                {
                  method: "GET",
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                }
              );
            })
            .then((res) => (res ? res.json() : null))
            .then((paymentData) => {
              if (!paymentData) return;

              // 3) تأیید پرداخت (status=10)
              return fetch("http://localhost:8000/payment/payment/", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                  token: paymentData.token,
                  status: 10,
                }),
              });
            })
            .then((res) => (res ? res.json() : null))
            .then(() => {
              alert("✅ خرید و فعال‌سازی اشتراک با موفقیت انجام شد");
              loadSubscriptions();
            })
            .catch(() => {
              alert("❌ خطا در فرآیند خرید");
            });
        });
      });
    })
    .catch(() => {
      packagesContainer.innerHTML = `
        <div class="alert alert-danger text-center">
          خطا در دریافت پکیج‌ها
        </div>
      `;
    });
}

// =======================
// پاپ‌آپ لاگین خرید
// =======================
const popupLoginForm = document.getElementById("popup-login-form");
const popupLoginMsg = document.getElementById("popup-login-message");

if (popupLoginForm) {
  popupLoginForm.addEventListener("submit", function (e) {
    e.preventDefault();

    popupLoginMsg.textContent = "در حال ورود...";
    popupLoginMsg.className = "mt-2 small text-muted";

    const formData = new FormData(popupLoginForm);
    const data = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    fetch("http://localhost:8000/api/users/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(await res.text());
        return res.json();
      })
      .then((json) => {
        localStorage.setItem("access_token", json.access);
        localStorage.setItem("refresh_token", json.refresh);

        popupLoginMsg.textContent = "✅ ورود موفقیت‌آمیز بود";
        popupLoginMsg.className = "mt-2 small text-success";
        popupLoginForm.reset();

        const modalEl = document.getElementById("login-popup");
        bootstrap.Modal.getInstance(modalEl).hide();

        loadSubscriptions();
      })
      .catch((err) => {
        popupLoginMsg.textContent = "❌ خطا: " + err.message;
        popupLoginMsg.className = "mt-2 small text-danger";
      });
  });
}

// =======================
// اشتراک‌های من
// =======================
const subsContainer = document.getElementById("subscriptions");

function loadSubscriptions() {
  if (!subsContainer) return;

  const token = localStorage.getItem("access_token");

  if (!token) {
    subsContainer.innerHTML = `
      <div class="alert alert-warning text-center">
        برای مشاهده اشتراک‌ها ابتدا وارد شوید.
      </div>
    `;
    return;
  }

  fetch("http://localhost:8000/sub/subscriptions/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      subsContainer.innerHTML = "";

      if (!Array.isArray(data) || !data.length) {
        subsContainer.innerHTML = `
          <div class="alert alert-info text-center">
            هیچ اشتراک فعالی ندارید.
          </div>
        `;
        return;
      }

      data.forEach((sub) => {
        const card = document.createElement("div");
        card.className = "col-md-4";

        card.innerHTML = `
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5>${sub.package?.title || ""}</h5>
              <p>${sub.package?.description || ""}</p>
              <p><strong>شروع:</strong> ${sub.created_time}</p>
              <p><strong>پایان:</strong> ${sub.expire_time || "نامشخص"}</p>
            </div>
          </div>
        `;

        subsContainer.appendChild(card);
      });
    })
    .catch(() => {
      subsContainer.innerHTML = `
        <div class="alert alert-danger text-center">
          خطا در دریافت اشتراک‌ها
        </div>
      `;
    });
}

loadSubscriptions();
// =======================
// Welcome Animation
// =======================
window.addEventListener("load", () => {
  const box = document.getElementById("welcome-box");
  const text = document.getElementById("welcome-text");

  // اگر کاربر لاگین کرده بود، اسمش رو بگیر
  const username = localStorage.getItem("username");

  if (username) {
    text.textContent = `سلام ${username} عزیز! خوش اومدی 🌟`;
  } else {
    text.textContent = "سلام! خوش اومدی به سایت من 🌟";
  }

  // نمایش انیمیشن
  setTimeout(() => {
    box.classList.add("show");
  }, 300);

  // محو شدن بعد از 3 ثانیه
  setTimeout(() => {
    box.classList.remove("show");
  }, 3000);
});
// =======================
// چشم‌های کاراکتر موس را دنبال کنند
// =======================
document.addEventListener("mousemove", (e) => {
  const pupils = document.querySelectorAll(".pupil");

  pupils.forEach((pupil) => {
    const rect = pupil.getBoundingClientRect();
    const eyeX = rect.left + rect.width / 2;
    const eyeY = rect.top + rect.height / 2;

    const angle = Math.atan2(e.clientY - eyeY, e.clientX - eyeX);
    const x = Math.cos(angle) * 6;
    const y = Math.sin(angle) * 6;

    pupil.style.transform = `translate(${x}px, ${y}px)`;
  });
});
// =======================
// بستن چشم‌ها هنگام وارد کردن رمز
// =======================
document.addEventListener("DOMContentLoaded", () => {
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  const character = document.querySelector(".cartoon-character");

  if (!character || passwordInputs.length === 0) return;

  passwordInputs.forEach((input) => {
    input.addEventListener("focus", () => {
      character.classList.add("closed");
    });

    input.addEventListener("blur", () => {
      character.classList.remove("closed");
    });
  });
});