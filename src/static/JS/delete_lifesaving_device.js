document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const deletedCrewId = event.target.getAttribute("lifesavindDeviceId");

        if (deletedCrewId === null) {
            return;
        }

        const deleteConfirm = confirm("Вы увереня, что хотите удалить данного сотрудника?")

        if (!deleteConfirm) {
            return;
        }

        const deleteQueryResult = await fetch(`/lifesavingdevices/${deletedCrewId}`, {method: "DELETE"});

        if (deleteQueryResult.status == 409) {
            alert("Невозможно удалить данное спастельное средство, т.к. в базе содержаться сведения о его экипаже!")
        } else {
            location.reload(true);
        }

       
    });
});