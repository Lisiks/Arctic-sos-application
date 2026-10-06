document.addEventListener("DOMContentLoaded", (event) => {
    const createForm = document.forms["create-form"];

    createForm.addEventListener("submit", async (event) => {
        if (!createForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(createForm);

        const fetchResult = await fetch("/users", {
            method: "POST",
            body: formData
        });

        if (fetchResult.status == 201) {
            location.href = "/site/users"
        } else if (fetchResult.status == 409) {
            alert("Пользователь с данным именем уже присутствует в БД!")
        } else {
            alert("Пожалуйста, введите данные о сотруднике в соответствии с формой!")
        }
    });
});