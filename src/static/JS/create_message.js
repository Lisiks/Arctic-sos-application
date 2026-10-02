document.addEventListener("DOMContentLoaded", (event) => {
    const createForm = document.forms["create-form"];

    createForm.addEventListener("submit", async (event) => {
        if (!createForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(createForm);

        const fetchResult = await fetch("/messages", {
            method: "POST",
            body: formData
        });

        if (fetchResult.status == 201) {
            location.href = "/site/messages"
        } else {
            alert("Пожалуйста, введите данные о сообщении в соответствии с формой!")
        }
    });
});