document.addEventListener("DOMContentLoaded", (event) => {
    const updateForm = document.forms["update-form"];

    updateForm.addEventListener("submit", async (event) => {
        if (!updateForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(updateForm);
        
        const pathSegments = location.pathname.split('/').filter(Boolean);
        const sourceId = pathSegments[pathSegments.length - 1];

        const fetchResult = await fetch(`/sources/${sourceId}`, {
            method: "PATCH",
            body: formData
        });

        if (fetchResult.status == 202) {
            location.href = "/site/sources";
        } else {
            alert("Пожалуйста, введите данные о сотруднике в соответствии с формой!");
        }
    });
});