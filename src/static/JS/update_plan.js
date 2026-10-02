document.addEventListener("DOMContentLoaded", (event) => {
    const createForm = document.forms["update-form"];

    createForm.addEventListener("submit", async (event) => {
        if (!createForm.checkValidity()) {
            return;
        }
        event.preventDefault();

     
        const formData = new FormData(createForm);

        const pathSegments = location.pathname.split('/').filter(Boolean);
        const messageId = pathSegments[pathSegments.length - 1];

        const fetchResult = await fetch(`/plans/${messageId}`, {
            method: "PATCH",
            body: formData
        });
        const jsonResult = await fetchResult.json()

        if (fetchResult.status == 202) {
            location.href = "/site/plans"
        } else if (fetchResult.status == 409) {
            
            if (jsonResult.msg === "Lifesaving devices cannot be used for this operation, because it has small reach zone for this operation!") {
                alert("Зона досягаемости выбранного судна слишком мала для проведения операции!");
            
            } else if (jsonResult.msg === "Lifesaving devices doesnt ready!") {
                alert("Выбранное судно не находится в состоянии готовности!");
            
            } else if (jsonResult.msg === "This help message already done!") {
                alert("На данное сообщение уже существует отчет о выполнении операции!");
            
            } else if (jsonResult.msg === "Bad weather for helecopter!") {
                alert("Вертолет не подходит для полетов в такую погоду!");
                
            } else if (jsonResult.msg === "Planning time smaller, than message call time!") {
                alert("Время ожидаемого спасения меньше, чем время прихода сообщения!");
            } else if (jsonResult.msg === "This help message doesnt exists!") {
                alert("Данного сообщения больше не существует!");

            } else if (jsonResult.msg === "For this message already exists plan!") {
                alert("Для данного сообщения уже есть план реагирования!");

            } else if (jsonResult.msg === "This lifesabing device doesnt exists!") {
                alert("Выбранное судно спасения отсутствует в БД!");
            } 

        } else {
            alert("Пожалуйста, введите данные о плане спасения в соответствии с формой!")
        }
    });
});