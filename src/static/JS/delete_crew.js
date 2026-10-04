document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const deletedCrewId = event.target.getAttribute("deletedCrewId");

        if (deletedCrewId === null) {
            return;
        }

        const deleteConfirm = confirm("Вы увереня, что хотите удалить данного сотрудника?")

        if (!deleteConfirm) {
            return;
        }

        const deleteQueryResult = await fetch(`/crews/${deletedCrewId}`, {method: "DELETE"});

        location.reload(true);
    });
});