document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    
    // Search functionality - now triggers page reload
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const searchTerm = this.value;
            updateUrlParameter('search', searchTerm);
        }, 300);
    });
    
    // Column visibility toggles (remains client-side)
    const columnToggles = document.querySelectorAll('.toggle-item input[type="checkbox"]');
    columnToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const column = this.dataset.column;
            toggleColumn(column, this.checked);
        });
    });
    
    // Helper function to update URL parameters
    function updateUrlParameter(key, value) {
        const url = new URL(window.location);
        if (value && value !== 'all') {
            url.searchParams.set(key, value);
        } else {
            url.searchParams.delete(key);
        }
        // Reset to page 1 when filters change
        url.searchParams.delete('page');
        window.location.href = url.toString();
    }
    
    // Column visibility function (remains the same)
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
});

function uncheckAll() {
    document.querySelectorAll('.toggle-item input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));
    });
}

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

function exportToPDF() {
    // Implement PDF export functionality if needed
    console.log("PDF export would be implemented here");
}