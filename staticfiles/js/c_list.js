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
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');
    const paginationSummary = document.getElementById('paginationSummary');
    
    let originalRows = Array.from(tableBody.querySelectorAll('tr'));
    let filteredRows = [...originalRows];
    let sortDirection = {};
    let currentPage = 1;
    const itemsPerPage = 50;
    let totalPages = 1;

    // Initialize pagination on page load
    updateTable();

    prevBtn.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            updateTable();
        }
    });

    nextBtn.addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
            updateTable();
        }
    });

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
        currentPage = 1; // Reset to first page
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
                // Assuming recent means higher IDs
                filteredRows = originalRows.filter(row => {
                    const idCell = row.querySelector('[data-column="id"]');
                    if (!idCell) return false;
                    const id = parseInt(idCell.textContent.trim());
                    const maxId = Math.max(...originalRows.map(r => {
                        const cell = r.querySelector('[data-column="id"]');
                        return cell ? parseInt(cell.textContent.trim()) : 0;
                    }));
                    return id > (maxId - 10);
                });
                break;
            case 'gmail':
                filteredRows = originalRows.filter(row => {
                    const emailCell = row.querySelector('[data-column="email"]');
                    if (!emailCell) return false;
                    const email = emailCell.textContent.toLowerCase();
                    return email.includes('gmail.com');
                });
                break;
        }
        currentPage = 1; // Reset to first page
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
            
            let aVal = aCell ? aCell.textContent.trim() : '';
            let bVal = bCell ? bCell.textContent.trim() : '';

            // Handle numeric sorting for ID
            if (column === 'id') {
                aVal = parseInt(aVal) || 0;
                bVal = parseInt(bVal) || 0;
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
        // Calculate pagination
        totalPages = Math.ceil(filteredRows.length / itemsPerPage);
        if (totalPages === 0) totalPages = 1;
        currentPage = Math.min(currentPage, Math.max(1, totalPages));
        
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const pageRows = filteredRows.slice(startIndex, endIndex);
        
        // Hide all original rows first
        originalRows.forEach(row => {
            if (row.parentNode) {
                row.style.display = 'none';
            }
        });
        
        // Clear table body
        tableBody.innerHTML = '';
        
        // Show only the rows for current page
        pageRows.forEach(row => {
            // Create a clean clone of the row
            const clonedRow = row.cloneNode(true);
            clonedRow.style.display = ''; // Make sure it's visible
            tableBody.appendChild(clonedRow);
        });

        // Re-add click handlers to cloned rows
        addRowEventListeners();

        // Update pagination controls
        updatePaginationControls();

        // Show/hide empty state
        if (filteredRows.length === 0) {
            table.style.display = 'none';
            emptyState.style.display = 'flex';
            const paginationContainer = document.querySelector('.pagination-container');
            if (paginationContainer) {
                paginationContainer.style.display = 'none';
            }
        } else {
            table.style.display = 'table';
            emptyState.style.display = 'none';
            const paginationContainer = document.querySelector('.pagination-container');
            if (paginationContainer) {
                paginationContainer.style.display = 'flex';
            }
        }
    }

    function addRowEventListeners() {
        tableBody.querySelectorAll('.table-row').forEach(row => {
            const clientId = row.dataset.clientId;
            if (clientId && typeof URL_BUILDER !== 'undefined') {
                row.addEventListener('click', function() {
                    window.location.href = URL_BUILDER.clientDetail(clientId);
                });
            }
                        
            // Stop propagation for action buttons and email links
            row.querySelectorAll('.action-btn, .email-link').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });
    }

    function updatePaginationControls() {
        // Update buttons
        prevBtn.disabled = currentPage <= 1;
        nextBtn.disabled = currentPage >= totalPages;
        
        // Update page info
        pageInfo.textContent = totalPages > 0 ? `${currentPage} of ${totalPages}` : '0 of 0';
        
        // Update client count and summary
        const startItem = filteredRows.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0;
        const endItem = Math.min(currentPage * itemsPerPage, filteredRows.length);
        
        clientCount.textContent = `${filteredRows.length} client${filteredRows.length !== 1 ? 's' : ''}`;
        paginationSummary.textContent = `Showing ${startItem}-${endItem} of ${filteredRows.length} clients`;
    }

    function clearAllFilters() {
        searchInput.value = '';
        filteredRows = [...originalRows];
        currentPage = 1;
        
        // Reset column toggles
        columnToggles.forEach(toggle => {
            if (toggle.type === 'checkbox') {
                toggle.checked = true;
                toggleColumn(toggle.dataset.column, true);
            }
        });

        // Reset quick filters
        quickFilters.forEach(f => f.classList.remove('active'));
        if (quickFilters.length > 0) {
            quickFilters[0].classList.add('active');
        }

        // Reset sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.className = 'bi bi-chevron-expand sort-icon';
        });
        sortDirection = {};

        updateTable();
    }

    // Initialize click handlers for existing rows
    addRowEventListeners();
});

function uncheckAll() {
    document.querySelectorAll('.toggle-item input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));
    });
}

// Print table functions
function printTable() {
    const tableContent = document.getElementById('clientTable').cloneNode(true);
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
    const table = document.getElementById('clientTable');
    const ws = XLSX.utils.table_to_sheet(table);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Clients");
    XLSX.writeFile(wb, 'clients-list.xlsx');
}