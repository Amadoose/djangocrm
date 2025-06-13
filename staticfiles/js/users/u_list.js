document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('clientTable');
    const tableBody = document.getElementById('tableBody');
    const clientCount = document.getElementById('clientCount');
    const emptyState = document.getElementById('emptyState');
    
    let originalRows = Array.from(tableBody.querySelectorAll('tr'));
    let filteredRows = [...originalRows];
    let sortDirection = {};

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterRows(searchTerm);
    });

    // Sortable columns
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.column;
            sortTable(column);
        });
    });

    function filterRows(searchTerm) {
        filteredRows = originalRows.filter(row => {
            const text = row.textContent.toLowerCase();
            return text.includes(searchTerm);
        });
        updateTable();
    }

    function sortTable(column) {
        const direction = sortDirection[column] === 'asc' ? 'desc' : 'asc';
        sortDirection[column] = direction;

        // Update sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.className = 'bi bi-chevron-expand sort-icon';
        });
        
        const currentIcon = document.querySelector(`th[data-column="${column}"] .sort-icon`);
        if (currentIcon) {
            currentIcon.className = `bi bi-chevron-${direction === 'asc' ? 'up' : 'down'} sort-icon active`;
        }

        filteredRows.sort((a, b) => {
            const aCell = a.querySelector(`[data-column="${column}"]`);
            const bCell = b.querySelector(`[data-column="${column}"]`);
            
            if (!aCell || !bCell) return 0;
            
            let aVal = aCell.textContent.trim();
            let bVal = bCell.textContent.trim();

            // Handle numeric sorting for username (if they're numeric IDs)
            if (column === 'username' && !isNaN(aVal) && !isNaN(bVal)) {
                aVal = parseInt(aVal);
                bVal = parseInt(bVal);
            }

            // Handle permission sorting (priority order)
            if (column === 'permission') {
                const permissionOrder = { 'Superuser': 3, 'Staff': 2, 'User': 1 };
                aVal = permissionOrder[aVal] || 0;
                bVal = permissionOrder[bVal] || 0;
            }

            if (direction === 'asc') {
                return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            } else {
                return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
            }
        });

        updateTable();
    }

    function updateTable() {
        // Clear current table body
        tableBody.innerHTML = '';
        
        // Add filtered rows
        filteredRows.forEach(row => {
            tableBody.appendChild(row.cloneNode(true));
        });

        // Re-add click handlers to cloned rows
        tableBody.querySelectorAll('.table-row').forEach(row => {
            // Stop propagation for action buttons and email links
            row.querySelectorAll('.action-btn, .email-link').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });

        // Update count
        clientCount.textContent = `${filteredRows.length} user${filteredRows.length !== 1 ? 's' : ''}`;

        // Show/hide empty state
        if (filteredRows.length === 0) {
            table.style.display = 'none';
            emptyState.style.display = 'flex';
        } else {
            table.style.display = 'table';
            emptyState.style.display = 'none';
        }
    }

    // Make clearAllFilters globally available for the HTML button
    window.clearAllFilters = function() {
        searchInput.value = '';
        filteredRows = [...originalRows];
        
        // Reset sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.className = 'bi bi-chevron-expand sort-icon';
        });
        sortDirection = {};

        updateTable();
    };

    // Initialize click handlers for existing rows
    document.querySelectorAll('.table-row').forEach(row => {
        row.querySelectorAll('.action-btn, .email-link').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        });
    });
});