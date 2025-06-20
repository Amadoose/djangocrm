document.addEventListener('DOMContentLoaded', function() {
    // Auto-save comments functionality
    const commentsTextarea = document.getElementById('folioComments');
    const commentsSaveIndicator = document.getElementById('commentsSaveIndicator');
    let saveTimeout;

    if (commentsTextarea) {
        commentsTextarea.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            commentsSaveIndicator.style.display = 'none';
            
            saveTimeout = setTimeout(() => {
                saveComments();
            }, 1000); // Save after 1 second of inactivity
        });
    }

    function saveComments() {
        const folioId = commentsTextarea.dataset.folioId;
        const comments = commentsTextarea.value;
        
        // Show saving indicator
        commentsSaveIndicator.innerHTML = '<i class="bi bi-clock"></i> Guardando...';
        commentsSaveIndicator.style.display = 'block';
        
        // AJAX call to save comments
        fetch(`/folio_detail/${folioId}/update_comments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify({
                comments: comments
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                commentsSaveIndicator.innerHTML = '<i class="bi bi-check-circle"></i> Guardado automáticamente';
                commentsSaveIndicator.style.display = 'block';
                setTimeout(() => {
                    commentsSaveIndicator.style.display = 'none';
                }, 2000);
            } else {
                commentsSaveIndicator.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Error al guardar';
                commentsSaveIndicator.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            commentsSaveIndicator.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Error al guardar';
            commentsSaveIndicator.style.display = 'block';
        });
    }

    const budgetInput = document.getElementById('budgetInput');
    const saveBudgetBtn = document.getElementById('saveBudgetBtn');
    const changeIndicator = document.getElementById('changeIndicator');

    // Change const to let so we can reassign it later
    let originalBudgetValue = budgetInput ? budgetInput.value : '';

    if (budgetInput && saveBudgetBtn) {
        // Show save button when budget changes
        budgetInput.addEventListener('input', function() {
            if (this.value !== originalBudgetValue) {
                saveBudgetBtn.style.display = 'inline-block';
                changeIndicator.style.display = 'block';
            } else {
                saveBudgetBtn.style.display = 'none';
                changeIndicator.style.display = 'none';
            }
        });

        // Handle form submission via JavaScript for better UX
        const budgetForm = document.getElementById('budgetForm');
        if (budgetForm) {
            budgetForm.addEventListener('submit', function(e) {
                e.preventDefault(); // Prevent default form submission
                
                const amount = parseFloat(budgetInput.value) || 0;
                
                // Show loading state
                saveBudgetBtn.innerHTML = '<i class="bi bi-clock"></i> Guardando...';
                saveBudgetBtn.disabled = true;
                
                // Use the form's action URL
                fetch(budgetForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest', // Ensure AJAX detection
                    },
                    body: new URLSearchParams({
                        'budget': amount
                    })
                })
                .then(response => {
                    // Check if response is JSON
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        return response.json();
                    } else {
                        throw new Error('Server returned non-JSON response');
                    }
                })
                .then(data => {
                    if (data.success) {
                        // Success - hide the save button
                        saveBudgetBtn.style.display = 'none';
                        changeIndicator.style.display = 'none';
                        
                        // Update the original value (this was causing the error!)
                        originalBudgetValue = budgetInput.value;
                        
                        // Show success message
                        changeIndicator.innerHTML = '<i class="bi bi-check-circle"></i> ' + (data.message || 'Presupuesto actualizado correctamente');
                        changeIndicator.style.display = 'block';
                        changeIndicator.style.color = '#28a745';
                        
                        // Update summary card budget display
                        const summaryBudget = document.querySelector('.summary-item .summary-number');
                        if (summaryBudget && summaryBudget.textContent.includes('$')) {
                            summaryBudget.textContent = '$' + parseFloat(budgetInput.value).toLocaleString();
                        }
                        
                        setTimeout(() => {
                            changeIndicator.style.display = 'none';
                        }, 3000);
                    } else {
                        // Server returned success: false
                        changeIndicator.innerHTML = '<i class="bi bi-exclamation-triangle"></i> ' + (data.error || 'Error al guardar el presupuesto');
                        changeIndicator.style.display = 'block';
                        changeIndicator.style.color = '#dc3545';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    changeIndicator.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Error al guardar el presupuesto';
                    changeIndicator.style.display = 'block';
                    changeIndicator.style.color = '#dc3545';
                })
                .finally(() => {
                    // Reset button state
                    saveBudgetBtn.innerHTML = '<i class="bi bi-check"></i> Guardar';
                    saveBudgetBtn.disabled = false;
                });
            });
        }
    }
});
