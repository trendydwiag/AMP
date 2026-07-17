/**
 * Kabulhaden CMS - SEO Preview Widget
 * Live preview of how content will appear in Google search results
 */
document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.querySelector('[name="seo_title"]') || document.querySelector('[name="title"]');
    const descInput = document.querySelector('[name="seo_description"]') || document.querySelector('[name="excerpt"]');
    const previewTitle = document.getElementById('seo-preview-title');
    const previewDesc = document.getElementById('seo-preview-description');
    const previewUrl = document.getElementById('seo-preview-url');

    if (!titleInput || !previewTitle) return;

    function updatePreview() {
        const title = titleInput.value || 'Judul Halaman';
        const desc = descInput ? descInput.value : '';
        const url = window.location.origin + '/berita/';

        previewTitle.textContent = title.substring(0, 60);
        if (previewDesc) {
            previewDesc.textContent = desc.substring(0, 160) || 'Deskripsi halaman akan muncul di sini...';
        }
        if (previewUrl) {
            previewUrl.textContent = url;
        }
    }

    titleInput.addEventListener('input', updatePreview);
    if (descInput) descInput.addEventListener('input', updatePreview);
    updatePreview();
});
