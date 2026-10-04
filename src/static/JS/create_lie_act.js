document.addEventListener("DOMContentLoaded", (event) => {
    const createForm = document.forms["create-form"];

    createForm.addEventListener("submit", async (event) => {
        if (!createForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(createForm);

        const pathSegments = location.pathname.split('/').filter(Boolean);
        const messageId = pathSegments[pathSegments.length - 1];

        const fetchResult = await fetch(`/lieacts/${messageId}`, {
            method: "POST",
            body: formData
        });

        const jsonResult = await fetchResult.json();
        if (fetchResult.status == 201) {
            location.href = "/site/lieact"
        } 

        else if (fetchResult.status === 409) {
            if (jsonResult.msg === "This message doesnt exists!") {
                alert("Данное сообщение в настоящий момент недоступно!")
            } else if (jsonResult.msg === "For this message already exists lie act!") {
                alert("Для данного сообщения уже соществует акт о ложном срабатывании!")
            } else if (jsonResult.msg === "Fact operation time smaller, than message call time!") {
                alert("Фактическое время прибытия меньше чем время поступления сообщения!")
            } else if (jsonResult.msg === "On this help message already exists operation act!") {
                alert("На данное сообщение уже свуществует акт об операции!")
            } 
        } else {
            alert("Пожалуйста, введите данные об акте спасения в соответствии с формой!")
        }
    }); 
});