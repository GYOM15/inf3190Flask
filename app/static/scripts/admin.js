document.addEventListener("DOMContentLoaded", () => {
    let selectedAnimalId = null;

    // Fonction pour afficher ou cacher le menu d'actions
    window.toggleActions = (buttonElement) => {
        const id = buttonElement.getAttribute("data-id");
        const menu = document.getElementById(`actions-${id}`);
        if (menu) {
            menu.classList.toggle("visible");
        }
    };

    // Fonction pour afficher le pop-up de confirmation de suppression
    window.confirmDeletion = (buttonElement) => {
        selectedAnimalId = buttonElement.getAttribute("data-id");
        const popup = document.getElementById("confirmation-popup");
        popup.style.display = "block";
    };

    // Fonction pour fermer le pop-up sans supprimer
    document.getElementById("cancel-delete").addEventListener("click", () => {
        const popup = document.getElementById("confirmation-popup");
        popup.style.display = "none";
        selectedAnimalId = null;
    });

    // Fonction pour confirmer la suppression
    document.getElementById("confirm-delete").addEventListener("click", () => {
        if (selectedAnimalId) {
            fetch(`/animals/delete/${selectedAnimalId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "success") {
                        const row = document.querySelector(`button[data-id="${selectedAnimalId}"]`).closest("tr");
                        if (row) row.remove();
                        document.getElementById("confirmation-popup").style.display = "none";
                        selectedAnimalId = null;
                    } else {
                        alert("Erreur : " + data.message);
                    }
                })
                .catch((error) => {
                    alert("Erreur réseau : impossible de supprimer l'animal.");
                    console.error("Erreur :", error);
                });
        }
    });
});