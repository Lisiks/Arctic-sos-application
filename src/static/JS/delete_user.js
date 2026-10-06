document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const deletedCrewId = event.target.getAttribute("deletedUserId");

        if (deletedCrewId === null) {
            return;
        }

        const deleteConfirm = confirm("Вы уверенны, что хотите удалить данного сотрудника?")

        if (!deleteConfirm) {
            return;
        }

        const deleteQueryResult = await fetch(`/users/${deletedCrewId}`, {method: "DELETE"});

        if (deleteQueryResult.status === 403) {
            alert("Вы не можете удалить суперпользователя (себя) из системы!")
        } else {
            location.reload(true);
        }

        
    });
});