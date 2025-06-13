function toggleButton(btn) {
    // Remove active class from all other filter buttons
    document.querySelectorAll('.filter-btn.active').forEach(activeBtn => {
        if (activeBtn !== btn) {
            activeBtn.classList.remove('active');
        }
    });
   
    // Toggle the clicked button
    btn.classList.toggle('active');
}
// suppliers.js
let currentService = null;
let serviceData = {};
let changedRows = new Set();
let fieldChoices = {}; // Store choices for select fields
// Service field configurations - matching your Django models
const serviceFields = {
    hotels: [
        'id', 'name', 'location', 'contact_email', 'phone',
        'rating', 'amenities', 'website', 'price_per_night', 'is_active'
    ],
    airlines: [
        'id', 'name', 'code', 'country', 'phone', 'website', 'is_active'
    ],
    activities: [
        'id', 'name', 'type', 'location', 'duration', 'price',
        'capacity', 'supplier'
    ],
    operators: [
        'id', 'name', 'type', 'location', 'contact_email', 'phone',
        'website', 'specialization', 'is_active'
    ],
    transports: [
        'id', 'name', 'type', 'location', 'contact_email', 'phone',
        'website', 'capacity', 'price_per_unit', 'is_active'
    ]
};
// Field configurations for proper input types and validation
const fieldConfigs = {
    hotels: {
        rating: {
            type: 'select',
            choices: [
                ['', '-- Select Rating --'],
                [1, '★☆☆☆☆ (Poor)'],
                [2, '★★☆☆☆ (Fair)'],
                [3, '★★★☆☆ (Good)'],
                [4, '★★★★☆ (Very Good)'],
                [5, '★★★★★ (Excellent)']
            ]
        },
        is_active: { type: 'checkbox' },
        contact_email: { type: 'email' },
        website: { type: 'url' },
        price_per_night: { type: 'number', step: '0.01', min: '0' },
        phone: { type: 'tel' }
    },
    airlines: {
        is_active: { type: 'checkbox' },
        website: { type: 'url' },
        phone: { type: 'tel' },
        code: { type: 'text', pattern: '[A-Z]{2,3}', title: 'IATA code must be 2-3 uppercase letters' }
    },
    activities: {
        type: {
            type: 'select',
            choices: [
                ['', '-- Select Type --'],
                ['safari', 'Safari'],
                ['tour', 'Tour'],
                ['excursion', 'Excursiones'],
                ['cultural', 'Actividad Cultural'],
                ['deportiva', 'Deportiva'],
                ['aventura', 'Aventura']
            ]
        },
        price: { type: 'number', step: '0.01', min: '0' },
        capacity: { type: 'number', min: '1' },
        supplier: { type: 'textarea' }
    },
    operators: {
        type: {
            type: 'select',
            choices: [
                ['', '-- Select Type --'],
                ['aerolinea', 'Aerolinea'],
                ['hotel', 'Hotel'],
                ['actividades', 'Actividades'],
                ['terrestre', 'Transporte terrestre'],
                ['maritimo', 'Transporte Maritimo']
            ]
        },
        is_active: { type: 'checkbox' },
        contact_email: { type: 'email' },
        website: { type: 'url' },
        phone: { type: 'tel' }
    },
    transports: {
        type: {
            type: 'select',
            choices: [
                ['', '-- Select Type --'],
                ['bus', 'Bus'],
                ['taxi', 'Taxi'],
                ['rental_car', 'Rental Car'],
                ['train', 'Train'],
                ['shuttle', 'Shuttle'],
                ['boat', 'Boat']
            ]
        },
        is_active: { type: 'checkbox' },
        contact_email: { type: 'email' },
        website: { type: 'url' },
        phone: { type: 'tel' },
        capacity: { type: 'number', min: '1' },
        price_per_unit: { type: 'number', step: '0.01', min: '0' }
    }
};
function toggleServiceTable(button, serviceType) {
    // Remove active class from all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
   
    // Hide all service tables
    document.querySelectorAll('.service-table').forEach(table => {
        table.classList.remove('active');
    });
   
    // If clicking the same button, just close the table
    if (currentService === serviceType) {
        currentService = null;
        return;
    }
   
    // Activate the clicked button and show corresponding table
    button.classList.add('active');
    document.getElementById(serviceType + '-table').classList.add('active');
    currentService = serviceType;
   
    // Load data for this service type
    loadServiceData(serviceType);
}
async function loadServiceData(serviceType) {
    try {
        // Load field choices first if needed
        await loadFieldChoices(serviceType);
       
        const response = await fetch(`/suppliers/api/${serviceType}/data/`);
        const result = await response.json();
       
        if (response.ok) {
            serviceData[serviceType] = result.data;
            renderTable(serviceType, result.data);
        } else {
            console.error('Error loading data:', result.error);
            alert('Error loading data: ' + result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Network error occurred while loading data');
    }
}
async function loadFieldChoices(serviceType) {
    if (fieldChoices[serviceType]) return; // Already loaded
   
    try {
        const response = await fetch(`/suppliers/api/${serviceType}/choices/`);
        const result = await response.json();
       
        if (response.ok) {
            fieldChoices[serviceType] = result.choices;
        }
    } catch (error) {
        console.error('Error loading field choices:', error);
    }
}
function renderTable(serviceType, data) {
    const tbody = document.getElementById(serviceType + '-tbody');
    tbody.innerHTML = '';
   
    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.dataset.rowIndex = index;
        tr.dataset.recordId = row.id || '';
       
        serviceFields[serviceType].forEach(field => {
            const td = document.createElement('td');
           
            if (field === 'id') {
                td.textContent = row[field] || 'New';
                td.style.color = '#666';
                td.style.fontStyle = 'italic';
                td.classList.add('id-cell');
            } else {
                const element = createFieldElement(serviceType, field, row[field]);
                element.addEventListener('input', function() {
                    markRowAsChanged(tr);
                });
                element.addEventListener('change', function() {
                    markRowAsChanged(tr);
                });
                td.appendChild(element);
            }
           
            tr.appendChild(td);
        });
       
        tbody.appendChild(tr);
    });
}
function createFieldElement(serviceType, field, value) {
    const config = fieldConfigs[serviceType]?.[field] || {};
   
    if (config.type === 'select') {
        const select = document.createElement('select');
        select.className = 'editable-cell';
        select.dataset.field = field;
       
        // Use predefined choices or dynamic choices
        const choices = config.choices || (fieldChoices[serviceType]?.[field] || []);
       
        choices.forEach(([choiceValue, choiceLabel]) => {
            const option = document.createElement('option');
            option.value = choiceValue;
            option.textContent = choiceLabel;
            if (value == choiceValue) {
                option.selected = true;
            }
            select.appendChild(option);
        });
       
        return select;
    } else if (config.type === 'checkbox') {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'editable-cell';
        checkbox.dataset.field = field;
        checkbox.checked = value === true || value === 'true' || value === 1;
        return checkbox;
    } else if (config.type === 'textarea') {
        const textarea = document.createElement('textarea');
        textarea.className = 'editable-cell';
        textarea.dataset.field = field;
        textarea.value = value || '';
        textarea.rows = 2;
        return textarea;
    } else {
        const input = document.createElement('input');
        input.type = config.type || getDefaultInputType(field);
        input.className = 'editable-cell';
        input.dataset.field = field;
        input.value = value || '';
       
        // Add additional attributes
        if (config.step) input.step = config.step;
        if (config.min) input.min = config.min;
        if (config.pattern) input.pattern = config.pattern;
        if (config.title) input.title = config.title;
       
        return input;
    }
}
function getDefaultInputType(field) {
    if (field.includes('email')) return 'email';
    if (field.includes('phone')) return 'tel';
    if (field.includes('website')) return 'url';
    if (field.includes('price') || field.includes('rating') || field.includes('capacity')) return 'number';
    return 'text';
}
function markRowAsChanged(row) {
    row.style.backgroundColor = '#fff3cd';
    const rowKey = `${currentService}-${row.dataset.rowIndex}`;
    changedRows.add(rowKey);
}
function addNewRow(serviceType) {
    const tbody = document.getElementById(serviceType + '-tbody');
    const newIndex = tbody.children.length;
   
    // Create empty row data with default values
    const emptyRow = {};
    serviceFields[serviceType].forEach(field => {
        if (field === 'id') {
            emptyRow[field] = null;
        } else if (field === 'is_active') {
            emptyRow[field] = true; // Default to active
        } else {
            emptyRow[field] = '';
        }
    });
   
    // Add to service data
    if (!serviceData[serviceType]) {
        serviceData[serviceType] = [];
    }
    serviceData[serviceType].push(emptyRow);
   
    // Re-render the table
    renderTable(serviceType, serviceData[serviceType]);
   
    // Mark the new row as changed
    const newRow = tbody.children[newIndex];
    markRowAsChanged(newRow);
}
async function saveAllChanges(serviceType) {
    const tbody = document.getElementById(serviceType + '-tbody');
    const rows = tbody.querySelectorAll('tr');
    const savePromises = [];
   
    for (let row of rows) {
        const rowKey = `${serviceType}-${row.dataset.rowIndex}`;
       
        if (changedRows.has(rowKey) || !row.dataset.recordId) {
            const rowData = extractRowData(row, serviceType);
           
            // Validate required fields
            if (!validateRowData(serviceType, rowData)) {
                return; // Stop if validation fails
            }
           
            savePromises.push(saveRecord(serviceType, rowData));
        }
    }
   
    if (savePromises.length === 0) {
        alert('No hay cambios para guardar');
        return;
    }
   
    try {
        await Promise.all(savePromises);
        alert('Todos los cambios se guardaron exitosamente');
        changedRows.clear();
        loadServiceData(serviceType); // Reload to get updated IDs and data
    } catch (error) {
        alert('Error al guardar algunos cambios. Por favor, revisa la consola para más detalles.');
        console.error('Save error:', error);
    }
}
function validateRowData(serviceType, data) {
    // Basic validation for required fields
    const requiredFields = {
        hotels: ['name', 'location', 'contact_email', 'amenities', 'website'],
        airlines: ['name', 'code', 'country', 'phone', 'website'],
        activities: ['name', 'type', 'location'],
        operators: ['name', 'type', 'location', 'contact_email', 'phone', 'website'],
        transports: ['name', 'type', 'location', 'contact_email', 'phone', 'website']
    };
   
    const required = requiredFields[serviceType] || [];
   
    for (const field of required) {
        if (!data[field] || data[field].toString().trim() === '') {
            alert(`El campo "${field.replace('_', ' ')}" es requerido`);
            return false;
        }
    }
   
    // Validate email format
    const emailFields = ['contact_email'];
    for (const field of emailFields) {
        if (data[field] && !isValidEmail(data[field])) {
            alert(`El campo "${field.replace('_', ' ')}" debe ser un email válido`);
            return false;
        }
    }
   
    // Validate URL format
    const urlFields = ['website'];
    for (const field of urlFields) {
        if (data[field] && !isValidUrl(data[field])) {
            alert(`El campo "${field.replace('_', ' ')}" debe ser una URL válida`);
            return false;
        }
    }
   
    return true;
}
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
function isValidUrl(url) {
    try {
        new URL(url.startsWith('http') ? url : `http://${url}`);
        return true;
    } catch {
        return false;
    }
}
function extractRowData(row, serviceType) {
    const data = {};
    const elements = row.querySelectorAll('.editable-cell');
   
    // Add ID if it exists
    if (row.dataset.recordId && row.dataset.recordId !== '') {
        data.id = row.dataset.recordId;
    }
   
    elements.forEach(element => {
        const field = element.dataset.field;
        let value;
       
        if (element.type === 'checkbox') {
            value = element.checked;
        } else if (element.type === 'number') {
            const numValue = element.value.trim();
            value = numValue === '' ? null : parseFloat(numValue);
        } else {
            value = element.value.trim();
            value = value === '' ? null : value;
        }
       
        data[field] = value;
    });
   
    return data;
}
async function saveRecord(serviceType, data) {
    try {
        const response = await fetch(`/suppliers/api/${serviceType}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        });
       
        const result = await response.json();
       
        if (!response.ok) {
            throw new Error(result.error || 'Unknown error occurred');
        }
       
        return result;
    } catch (error) {
        console.error('Error saving record:', error);
        throw error;
    }
}
// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Export/Import functionality
function exportServiceData(serviceType) {
    if (!serviceData[serviceType] || serviceData[serviceType].length === 0) {
        alert('No hay datos para exportar');
        return;
    }
   
    const data = serviceData[serviceType];
    const csv = convertToCSV(data);
    downloadCSV(csv, `${serviceType}_export.csv`);
}
function convertToCSV(data) {
    if (data.length === 0) return '';
   
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row =>
            headers.map(header => {
                const value = row[header];
                if (value === null || value === undefined) return '';
                return `"${String(value).replace(/"/g, '""')}"`;
            }).join(',')
        )
    ].join('\n');
   
    return csvContent;
}
function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
   
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
// Legacy function for backward compatibility
function toggleButton(button) {
    console.log('Legacy toggleButton called, use toggleServiceTable instead');
}

