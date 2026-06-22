function showToast(message, type = 'success',parent) {
    const container = parent.querySelector('.toast-container');

    // Create the HTML structure
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'primary' : 'danger'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="toast-header">
            <strong class="me-auto">Bootstrap</strong>
            <small class="text-body-secondary">just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>

            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>`;

    // Convert string to DOM element
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = toastHtml;
    const toastElement = tempDiv.firstElementChild;

    // Add to container
    container.prepend(toastElement);

    // Initialize and Show Bootstrap Toast
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Cleanup: Remove from DOM after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

export {
    showToast
}