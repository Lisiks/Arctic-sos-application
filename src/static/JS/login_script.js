document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.forms["login-form"];

    loginForm.addEventListener("submit", async (event) => {
        if (!loginForm.checkValidity()) {
            return;
        }

        event.preventDefault();

        const formData = new FormData(loginForm);

        const fetchResult = await fetch("/users/login",
            {
                method: "POST",
                body: formData
            }
        )
        if (fetchResult.status == 200) {
            location.href = "/site/messages"
        } else {
            alert("Ошибка входа: неверный логин или пароль!")
        }
    });
})