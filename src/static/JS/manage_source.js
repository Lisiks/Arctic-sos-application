document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const deletedSourceId = event.target.getAttribute("deleteSourceId");

        if (deletedSourceId === null) {
            return;
        }

        const deleteConfirm = confirm("Вы уверенны, что хотите удалить данный источник?")

        if (!deleteConfirm) {
            return;
        }

        const deleteQueryResult = await fetch(`/sources/${deletedSourceId}`, {method: "DELETE"});

        if (deleteQueryResult.status === 409) {
            alert("Вы не можете удалить данный источник, т.к. в системе уже зарегистрированы сообщения от него!")
        } else {
            location.reload(true);
        }
    });

    document.addEventListener("click", async (event) => {
        const checkedSourceId = event.target.getAttribute("checkSourceId");

        if (checkedSourceId === null) {
            return;
        }

        const checkConfirm = confirm("Вы уверенны, что хотите пометить данный источник как проверенный?")

        if (!checkConfirm) {
            return;
        }

        const checkQueryResult = await fetch(`/sources/check/${checkedSourceId}`, {method: "PATCH"});

        if (checkQueryResult.status === 202) {
            location.reload(true);
        } else {
            alert("Что-то пошло не так!")
        }
    });
});