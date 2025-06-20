document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('folioModal');
    const overlay = document.getElementById('folioModalOverlay');
    const closeBtn = document.getElementById('closeFolioModal');
    const cancelBtn = document.getElementById('cancelFolio');
    const timeDisplay = document.getElementById('createdAtDisplay'); // <-- Make sure this variable is here
    let clienteSelect, agenteSelect;

    if (!modal || !overlay) {
        console.warn('Modal elements not found');
        return;
    }

    // RE-ADD: The function to update the time display
    function updateTime() {
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        if (timeDisplay) {
            timeDisplay.textContent = now.toLocaleDateString('es-ES', options);
        }
    }

    function openModal() {
        document.body.classList.add('modal-open');
        overlay.classList.add('active');
        modal.classList.add('active');
        
        // RE-ADD: Start the clock when the modal opens
        updateTime();
        window.folioTimeInterval = setInterval(updateTime, 1000);

        window.dispatchEvent(new CustomEvent('folioModalOpened'));
    }

    function closeModal() {
        document.body.classList.remove('modal-open');
        overlay.classList.remove('active');
        modal.classList.remove('active');
        
        // RE-ADD: Stop the clock when the modal closes to save resources
        if (window.folioTimeInterval) {
            clearInterval(window.folioTimeInterval);
            window.folioTimeInterval = null;
        }

        if (clienteSelect && clienteSelect.destroy) clienteSelect.destroy();
        if (agenteSelect && agenteSelect.destroy) agenteSelect.destroy();
        
        const form = document.getElementById('folioForm');
        if (form) form.reset();
    }

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => e.stopPropagation());
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) closeModal();
    });

    window.addEventListener('folioModalOpened', function() {
        
        const fetchClients = fetch('/api/search_clients/?q=').then(res => res.json());
        const fetchAgents = fetch('/api/search_agents/?q=').then(res => res.json());

        Promise.all([fetchClients, fetchAgents])
            .then(([clientData, agentData]) => {
                
                // --- INITIALIZE TOM SELECT FOR CLIENTES ---
                clienteSelect = new TomSelect('#clienteSelect', {
                    maxOptions: null, // <-- ADD THIS LINE: Render all options and disable the performance limit.
                    maxItems: 1,
                    valueField: 'id',
                    labelField: 'text',
                    searchField: ['nombre', 'apellido_paterno', 'email', 'id'],
                    options: clientData.results,
                    create: false,
                    openOnFocus: true,
                    score: function(search) {
                        var score = this.getScoreFunction(search);
                        return function(item) {
                            if (item.id.toString() === search.query) return 2.0;
                            return score(item);
                        };
                    },
                    render: {
                        option: function(data, escape) {
                            return `<div class="d-flex align-items-center p-2">
                                        <div class="flex-grow-1">
                                            <div class="text-dark">${escape(data.nombre)} ${escape(data.apellido_paterno)}</div>
                                            <div class="text-muted small mt-1">ID: ${escape(data.id)} | ${escape(data.email)}</div>
                                        </div>
                                    </div>`;
                        },
                        item: function(data, escape) {
                            return `<div>${escape(data.id)} ${escape(data.nombre)} ${escape(data.apellido_paterno)} ${escape(data.email)}</div>`;
                        }
                    }
                });

                // --- INITIALIZE TOM SELECT FOR AGENTES ---
                agenteSelect = new TomSelect('#agenteSelect', {
                    maxOptions: null, // <-- ADD THIS LINE: Render all options and disable the performance limit.
                    maxItems: 1,
                    valueField: 'id',
                    labelField: 'text',
                    searchField: ['first_name', 'last_name', 'username', 'id'],
                    options: agentData.results,
                    create: false,
                    openOnFocus: true,
                    score: function(search) {
                        var score = this.getScoreFunction(search);
                        return function(item) {
                            if (item.id.toString() === search.query) return 2.0;
                            return score(item);
                        };
                    },
                    render: {
                        option: function(data, escape) {
                            return `<div class="d-flex align-items-center p-2">
                                        <div class="flex-grow-1">
                                            <div class="text-dark">${escape(data.first_name)} ${escape(data.last_name)}</div>
                                            <div class="text-muted small mt-1">ID: ${escape(data.id)} | Username: ${escape(data.username)}</div>
                                        </div>
                                    </div>`;
                        },
                        item: function(data, escape) {
                            return `<div>${escape(data.id)} ${escape(data.username)} ${escape(data.first_name)}</div>`;
                        }
                    }
                });

            }).catch(error => {
                console.error("Failed to fetch data for select inputs:", error);
                alert("Error: No se pudieron cargar los datos de clientes o agentes.");
            });
    });
    
    // Global FolioModal object
    window.FolioModal = { open: openModal, close: closeModal };
    
    // --- FORM SUBMISSION LOGIC ---
    // This is the code that makes the "Crear Folio" button work.
    const form = document.getElementById('folioForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); 
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnHTML = submitBtn.innerHTML;
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Creando...';
                submitBtn.disabled = true;
            }
            const formData = new FormData(form);
            const actionURL = form.getAttribute('action');
            fetch(actionURL, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    alert('Error: ' + (data.error || 'Ocurrió un error al crear el folio.'));
                    if(submitBtn) {
                        submitBtn.innerHTML = originalBtnHTML;
                        submitBtn.disabled = false;
                    }
                }
            })
            .catch(error => {
                console.error('Submission Error:', error);
                alert('An unexpected error occurred. Please try again.');
                if(submitBtn) {
                    submitBtn.innerHTML = originalBtnHTML;
                    submitBtn.disabled = false;
                }
            });
        });
    }
});