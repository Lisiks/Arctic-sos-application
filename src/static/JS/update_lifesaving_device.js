document.addEventListener("DOMContentLoaded", (event) => {
    const updateForm = document.forms["update-form"];

    updateForm.addEventListener("submit", async (event) => {
        if (!updateForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(updateForm);
        
        const pathSegments = location.pathname.split('/').filter(Boolean);
        const lifesavindDevice = pathSegments[pathSegments.length - 1];


        const fetchResult = await fetch(`/lifesavingdevices/${lifesavindDevice}`, {
            method: "PATCH",
            body: formData
        });

        if (fetchResult.status == 202) {
            location.href = "/site/lifesavingdevises";
        } else {
            alert("Пожалуйста, введите данные о спасательном средстве в соответствии с формой!");
        }
    });
});