document.addEventListener('DOMContentLoaded', function() {
    // Search functionality with AJAX
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            // Debounce search to avoid too many requests
            searchTimeout = setTimeout(() => {
                performSearch();
            }, 300); // Wait 300ms after user stops typing
        });
    }
    
    function performSearch() {
        const searchTerm = searchInput.value;
        const currentUrl = new URL(window.location);
        
        // Update URL without page reload
        if (searchTerm) {
            currentUrl.searchParams.set('search', searchTerm);
        } else {
            currentUrl.searchParams.delete('search');
        }
        currentUrl.searchParams.delete('page'); // Reset to first page
        
        // Update browser history without reload
        window.history.pushState({}, '', currentUrl);
        
        // Perform AJAX request to get filtered results
        fetch(currentUrl.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.text())
        .then(html => {
            // Parse the response and update only the table content
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Update table body
            const newTableBody = doc.querySelector('#foliosTable tbody');
            const currentTableBody = document.querySelector('#foliosTable tbody');
            if (newTableBody && currentTableBody) {
                currentTableBody.innerHTML = newTableBody.innerHTML;
                // Re-attach click events to new rows
                attachRowClickEvents();
            }
            
            // Update pagination
            const newPagination = doc.querySelectorAll('.pagination-container');
            const currentPagination = document.querySelectorAll('.pagination-container');
            if (newPagination.length > 0 && currentPagination.length > 0) {
                newPagination.forEach((newPag, index) => {
                    if (currentPagination[index]) {
                        currentPagination[index].innerHTML = newPag.innerHTML;
                    }
                });
            }
            
            // Update folio count
            const newFolioCount = doc.querySelector('.folio-count');
            const currentFolioCount = document.querySelector('.folio-count');
            if (newFolioCount && currentFolioCount) {
                currentFolioCount.textContent = newFolioCount.textContent;
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            // Fallback to page reload if AJAX fails
            window.location.href = currentUrl.toString();
        });
    }

    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.dataset.filter;
            const url = new URL(window.location);
            
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            if (filter === 'all') {
                url.searchParams.delete('status');
            } else {
                url.searchParams.set('status', filter);
            }
            url.searchParams.delete('page'); // Reset to first page
            window.location.href = url.toString();
        });
    });

    // Initial attachment of row click events
    attachRowClickEvents();
    
    function attachRowClickEvents() {
        const tableRows = document.querySelectorAll('.table-row');
        tableRows.forEach(row => {
            row.addEventListener('click', function(e) {
                // Don't navigate if clicking on action buttons
                if (e.target.closest('.action-buttons')) {
                    return;
                }
                
                const folioId = this.dataset.folioId;
                if (folioId) {
                    window.location.href = `/folio_detail/${folioId}/`;
                }
            });
        });
    }
});

function openNewFolioModal() {
    // Implement modal opening logic
    // For now, redirect to a create folio page or show modal
    alert('Abrir modal para crear nuevo folio');
}