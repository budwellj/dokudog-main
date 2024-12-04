document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('add-work-modal');
    const openButton = document.getElementById('open-modal-button');
    const closeButton = document.getElementById('close-modal-button');

    // Open modal
    if (openButton) {
        openButton.addEventListener('click', function () {
            modal.style.display = 'block';
        });
    }

    // Close modal
    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside of the modal content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
