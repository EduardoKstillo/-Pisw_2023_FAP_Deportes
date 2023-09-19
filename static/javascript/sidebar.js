$(document).ready(function() {
    // Mostrar u ocultar el sidebar al hacer clic en el botón
    $("#sidebarCollapse").on("click", function() {
        $("#sidebar").toggleClass("active");
    });
});