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
                window.location.href = `{% url 'client_detail' 0 %}`.replace('0', clientId);
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

function copyText(element) {
    const textContent = element.querySelector('.field-content').textContent.trim();
    
    if (textContent && textContent !== 'Not provided') {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(textContent).then(() => {
                showCopyFeedback(element);
            }).catch(() => {
                fallbackCopyTextToClipboard(textContent, element);
            });
        } else {
            fallbackCopyTextToClipboard(textContent, element);
        }
    }
}

function showCopyFeedback(element) {
    element.classList.add('copied-feedback');
    const originalContent = element.innerHTML;
    
    element.innerHTML = '<span class="field-content">✓ Copied!</span><i class="bi bi-check2 copy-icon"></i>';
    
    setTimeout(() => {
        element.innerHTML = originalContent;
        element.classList.remove('copied-feedback');
    }, 1500);
}

function fallbackCopyTextToClipboard(text, element) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyFeedback(element);
    } catch (err) {
        console.error('Could not copy text: ', err);
    }
    
    document.body.removeChild(textArea);
}

document.addEventListener('DOMContentLoaded', function() {
    const areaCodeInput = document.getElementById('areaCode');
    const phoneNumberInput = document.getElementById('phoneNumber');
    const fullPhoneDisplay = document.getElementById('fullPhoneDisplay');

    // Format phone number with dashes (XXX-XXX-XXXX)
    function formatPhoneNumber(value) {
        // Remove all non-digits
        const numbers = value.replace(/\D/g, '');
        
        // Limit to 10 digits
        const limitedNumbers = numbers.slice(0, 10);
        
        // Format based on length
        if (limitedNumbers.length <= 3) {
            return limitedNumbers;
        } else if (limitedNumbers.length <= 6) {
            return limitedNumbers.slice(0, 3) + '-' + limitedNumbers.slice(3);
        } else {
            return limitedNumbers.slice(0, 3) + '-' + limitedNumbers.slice(3, 6) + '-' + limitedNumbers.slice(6);
        }
    }

    // Update the full phone display
    function updateFullPhone() {
        const areaCode = areaCodeInput.value || '+52';
        const phoneNumber = phoneNumberInput.value || '';
        const fullPhone = areaCode + (phoneNumber ? '-' + phoneNumber : '');
        fullPhoneDisplay.textContent = 'Complete: ' + fullPhone;
    }

    // Phone number input handling
    phoneNumberInput.addEventListener('input', function(e) {
        const formatted = formatPhoneNumber(e.target.value);
        e.target.value = formatted;
        updateFullPhone();
    });

    // Area code input handling
    areaCodeInput.addEventListener('input', function(e) {
        // Allow +, numbers, parentheses, spaces, and dashes
        e.target.value = e.target.value.replace(/[^+\d\-\(\)\s]/g, '');
        updateFullPhone();
    });

    // Prevent non-numeric input for phone number (allow only digits and dashes)
    phoneNumberInput.addEventListener('keypress', function(e) {
        const char = String.fromCharCode(e.which);
        if (!/[\d\-]/.test(char) && !e.ctrlKey && !e.metaKey && e.which !== 8) {
            e.preventDefault();
        }
    });

    // Copy full phone number on click
    fullPhoneDisplay.addEventListener('click', function() {
        const areaCode = areaCodeInput.value || '+52';
        const phoneNumber = phoneNumberInput.value || '';
        const fullPhone = areaCode + (phoneNumber ? '-' + phoneNumber : '');
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(fullPhone).then(() => {
                // Briefly show copied feedback
                const originalText = fullPhoneDisplay.textContent;
                fullPhoneDisplay.textContent = 'Copied!';
                fullPhoneDisplay.style.backgroundColor = '#d4edda';
                setTimeout(() => {
                    fullPhoneDisplay.textContent = originalText;
                    fullPhoneDisplay.style.backgroundColor = '#f8f9fa';
                }, 1000);
            });
        }
    });

    // Add cursor pointer to clickable display
    fullPhoneDisplay.style.cursor = 'pointer';
    fullPhoneDisplay.title = 'Click to copy full number';

    // Initialize display
    updateFullPhone();
});



