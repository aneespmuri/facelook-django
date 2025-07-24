document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.filter-wrapper') || document.querySelector('#changelist-filter');

    if (sidebar) {
        const existing = new URLSearchParams(window.location.search).get('specific_date') || '';
        const html = `
            <div class="form-row">
                <label for="specific_date_input"><strong>Specific Date</strong></label>
                <input type="date" id="specific_date_input" name="specific_date"
                       value="${existing}" style="width: 100%; padding: 4px; margin-top: 4px;">
            </div>
        `;
        sidebar.insertAdjacentHTML('beforeend', html);

        const input = document.getElementById('specific_date_input');
        input.addEventListener('change', function () {
            const url = new URL(window.location);
            url.searchParams.set('specific_date', input.value);
            window.location.href = url.toString();
        });
    }
});
