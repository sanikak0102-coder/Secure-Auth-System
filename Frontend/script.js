document.addEventListener("DOMContentLoaded", function () {

    console.log("JS Loaded");

    // ===== LOGIN =====
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            const captcha = grecaptcha.getResponse();

            if (!captcha) {
                alert("Please complete CAPTCHA");
                return;
            }

            if (!email.includes("@")) {
                alert("Enter a valid email");
                return;
            }

            try {
                const response = await fetch("http://127.0.0.1:5000/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password, captcha })
                });

                const data = await response.json();

                if (response.status === 200) {
                    alert("Login Successful ✅");
                    localStorage.setItem("token", data.token);
                    window.location.href = "dashboard.html";
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error(error);
                alert("Server error");
            }
        });
    }

    // ===== REGISTER =====
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const username = document.getElementById("username").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();
            const role = document.getElementById("role").value;

            try {
                const response = await fetch("http://127.0.0.1:5000/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, email, password, role })
                });

                const data = await response.json();

                if (response.status === 200) {
                    alert("Registered Successfully ✅");
                    window.location.href = "login.html";
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error(error);
                alert("Server error");
            }
        });
    }

    // ===== DASHBOARD =====
    if (window.location.pathname.includes("dashboard.html")) {

        const token = localStorage.getItem("token");

        if (!token) {
            alert("Please login first");
            window.location.href = "login.html";
            return;
        }

        const payload = JSON.parse(atob(token.split('.')[1]));
        const role = payload.role;
        const adminSection = document.getElementById("adminSection");

        const usersDiv = document.getElementById("usersList");
        const title = document.getElementById("dashboardTitle");

        // 👇 SHOW/HIDE ADMIN SECTION
        if (role === "admin") {
            if (adminSection) {
                adminSection.style.display = "block";
            }
        } else {
            if (adminSection) {
                adminSection.style.display = "none";
            }
        }

        // 👑 ADMIN
        if (role === "admin") {

            title.innerText = "👑 Admin Dashboard";

            fetch("http://127.0.0.1:5000/users", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token
                }
            })
            .then(res => res.json())
            .then(data => {

                if (!usersDiv) return;

                usersDiv.innerHTML = "<h3>All Users:</h3>";

                data.forEach(user => {
                    usersDiv.innerHTML += `
                        <p>${user.username} - ${user.email} (${user.role})</p>
                    `;
                });
            })
            .catch(err => {
                console.error(err);
                alert("Error loading users");
            });

        } 
        // 👤 NORMAL USER
        else {
            if (usersDiv) {
                title.innerText = "👤 User Dashboard";
                usersDiv.innerHTML = "<h3>Welcome User 👤</h3>";
            }
        }
    }

    // ===== PASSWORD TOGGLE =====
    const togglePassword = document.querySelector(".toggle-password");
    const passwordInput = document.getElementById("password");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            passwordInput.type =
                passwordInput.type === "password" ? "text" : "password";
        });
    }

}); // ✅ DOMContentLoaded END


// ===== LOGOUT =====
window.logout = function () {
    localStorage.removeItem("token");
    alert("Logged out");
    window.location.href = "login.html";
};