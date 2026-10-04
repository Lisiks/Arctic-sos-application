document.addEventListener("DOMContentLoaded", () => {
    const pageInput = document.forms["pagination-form"].page;
    const tableBody = document.getElementById("table-body");

    const lastPageButton = document.getElementById("last-page-button");
    const nextPageButton = document.getElementById("next-page-button");

    lastPageButton.addEventListener("click", () => {
        if (pageInput.value > 1) {
            pageInput.value --;
        }
    });
    nextPageButton.addEventListener("click", () => {
        console.log(tableBody.children.length)
        if (tableBody.children.length !== 0) {
            pageInput.value ++;
        }
    });
});