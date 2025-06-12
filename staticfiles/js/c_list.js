document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const filterToggle = document.getElementById('filterToggle');
    const filterPanel = document.getElementById('filterPanel');
    const columnToggles = document.querySelectorAll('[data-column]');
    const table = document.getElementById('clientTable');
    const tableBody = document.getElementById('tableBody');
    const clientCount = document.getElementById('clientCount');
    const emptyState = document.getElementById('emptyState');
    const quickFilters = document.querySelectorAll('.filter-chip');
    
    let originalRows = Array.from(tableBody.querySelectorAll('tr'));
    let filteredRows = [...originalRows];
    let sortDirection = {};

    // Toggle filter panel
    filterToggle.addEventListener('click', function() {
        filterPanel.classList.toggle('show');
        filterToggle.classList.toggle('active');
    });

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterRows(searchTerm);
    });

    // Column visibility toggles
    columnToggles.forEach(toggle => {
        if (toggle.type === 'checkbox') {
            toggle.addEventListener('change', function() {
                const column = this.dataset.column;
                toggleColumn(column, this.checked);
            });
        }
    });

    // Quick filters
    quickFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            quickFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            applyQuickFilter(this.dataset.filter);
        });
    });

    // Sortable columns
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.column;
            sortTable(column);
        });
    });

    // Clear filters
    document.getElementById('clearFilters').addEventListener('click', clearAllFilters);

    function filterRows(searchTerm) {
        filteredRows = originalRows.filter(row => {
            const text = row.textContent.toLowerCase();
            return text.includes(searchTerm);
        });
        updateTable();
    }

    function toggleColumn(column, show) {
        const headerCell = document.querySelector(`th[data-column="${column}"]`);
        const dataCells = document.querySelectorAll(`td[data-column="${column}"]`);
        
        if (show) {
            headerCell?.classList.remove('hidden-column');
            dataCells.forEach(cell => cell.classList.remove('hidden-column'));
        } else {
            headerCell?.classList.add('hidden-column');
            dataCells.forEach(cell => cell.classList.add('hidden-column'));
        }
    }

    function applyQuickFilter(filterType) {
        switch(filterType) {
            case 'all':
                filteredRows = [...originalRows];
                break;
            case 'recent':
                // Assuming recent means higher IDs (you can adjust this logic)
                filteredRows = originalRows.filter(row => {
                    const id = parseInt(row.querySelector('[data-column="id"]').textContent.trim());
                    return id > (Math.max(...originalRows.map(r => parseInt(r.querySelector('[data-column="id"]').textContent.trim()))) - 10);
                });
                break;
            case 'gmail':
                filteredRows = originalRows.filter(row => {
                    const email = row.querySelector('[data-column="email"]').textContent.toLowerCase();
                    return email.includes('gmail.com');
                });
                break;
        }
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
        currentIcon.className = `bi bi-chevron-${direction === 'asc' ? 'up' : 'down'} sort-icon active`;

        filteredRows.sort((a, b) => {
            let aVal = a.querySelector(`[data-column="${column}"]`).textContent.trim();
            let bVal = b.querySelector(`[data-column="${column}"]`).textContent.trim();

            // Handle numeric sorting for ID
            if (column === 'id') {
                aVal = parseInt(aVal);
                bVal = parseInt(bVal);
            }

            if (direction === 'asc') {
                return aVal > bVal ? 1 : -1;
            } else {
                return aVal < bVal ? 1 : -1;
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
            const clientId = row.dataset.clientId;
            row.addEventListener('click', function() {
                window.location.href = URL_BUILDER.clientDetail(clientId);
            });
                        
            // Stop propagation for action buttons and email links
            row.querySelectorAll('.action-btn, .email-link').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });

        // Update count
        clientCount.textContent = `${filteredRows.length} client${filteredRows.length !== 1 ? 's' : ''}`;

        // Show/hide empty state
        if (filteredRows.length === 0) {
            table.style.display = 'none';
            emptyState.style.display = 'flex';
        } else {
            table.style.display = 'table';
            emptyState.style.display = 'none';
        }
    }

    function clearAllFilters() {
        searchInput.value = '';
        filteredRows = [...originalRows];
        
        // Reset column toggles
        columnToggles.forEach(toggle => {
            if (toggle.type === 'checkbox') {
                toggle.checked = true;
                toggleColumn(toggle.dataset.column, true);
            }
        });

        // Reset quick filters
        quickFilters.forEach(f => f.classList.remove('active'));
        quickFilters[0].classList.add('active');

        // Reset sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.className = 'bi bi-chevron-expand sort-icon';
        });
        sortDirection = {};

        updateTable();
    }

    // Initialize click handlers for existing rows
    document.querySelectorAll('.table-row').forEach(row => {
        row.querySelectorAll('.action-btn, .email-link').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        });
    });
});

function uncheckAll() {
    document.querySelectorAll('.toggle-item input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.checked = false;
        // Trigger change event if you have listeners
        checkbox.dispatchEvent(new Event('change'));
    });
};



// print table functions
function printTable() {
    // Get only the currently displayed table data
    const tableContent = document.getElementById('clientTable').cloneNode(true);
    
    // Remove action column and buttons from the clone
    tableContent.querySelectorAll('.actions-column, .action-buttons').forEach(el => el.remove());
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Client List</title>
                <style>
                    table { 
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }
                    th, td { 
                        padding: 12px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }
                    th {
                        background-color: #f5f5f7;
                        font-weight: 600;
                    }
                    .hidden-column {
                        display: none;
                    }
                    .id-badge {
                        background: #f0f0f0;
                        padding: 4px 8px;
                        border-radius: 12px;
                        font-size: 13px;
                    }
                    @media print {
                        @page { size: landscape; }
                    }
                </style>
            </head>
            <body>
                ${tableContent.outerHTML}
            </body>
        </html>
    `);
    
    printWindow.document.close();
    setTimeout(() => {
        printWindow.print();
        printWindow.close();
    }, 250);
}

function exportToExcel() {
    // Using SheetJS library
    const table = document.getElementById('clientTable');
    const ws = XLSX.utils.table_to_sheet(table);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Clients");
    XLSX.writeFile(wb, 'clients-list.xlsx');
}
