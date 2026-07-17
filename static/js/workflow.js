/**
 * Kabulhaden CMS - Workflow Actions
 * Handles content workflow transitions via HTMX
 */
document.addEventListener('DOMContentLoaded', function() {
    // Workflow action buttons
    document.querySelectorAll('[data-workflow-action]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.workflowAction;
            const url = this.dataset.workflowUrl;
            const confirmMsg = this.dataset.confirm;

            if (confirmMsg && !confirm(confirmMsg)) return;

            const formData = new FormData();
            formData.append('action', action);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]')?.value || '');

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    // Update status badge
                    const badge = document.getElementById('status-badge');
                    if (badge && data.status_display) {
                        badge.textContent = data.status_display;
                        badge.className = getStatusBadgeClass(data.new_status);
                    }
                    // Show success message
                    showToast('Status berhasil diperbarui', 'success');
                    // Reload page after short delay
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showToast(data.error || 'Gagal memperbarui status', 'error');
                }
            })
            .catch(() => showToast('Terjadi kesalahan', 'error'));
        });
    });

    // Schedule publish form
    const scheduleForm = document.getElementById('schedule-form');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const url = this.action;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    showToast('Berhasil dijadwalkan', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showToast(data.error || 'Gagal menjadwalkan', 'error');
                }
            });
        });
    }
});

function getStatusBadgeClass(status) {
    const classes = {
        'DRAFT': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        'PENDING_REVIEW': 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
        'APPROVED': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
        'SCHEDULED': 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
        'PUBLISHED': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        'ARCHIVED': 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
        'REJECTED': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    };
    return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ' + (classes[status] || classes['DRAFT']);
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg text-white text-sm font-medium transition-all transform translate-y-0 opacity-100 ${
        type === 'success' ? 'bg-green-600' : 'bg-red-600'
    }`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
