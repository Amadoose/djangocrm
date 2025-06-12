document.addEventListener('DOMContentLoaded', function() {
    const areaCodeInput = document.getElementById('areaCode');
    const phoneNumberInput = document.getElementById('phoneNumber');
    const fullPhoneDisplay = document.getElementById('fullPhoneDisplay');

    // Format phone number with dashes (XXX-XXX-XXXX)
    function formatPhoneNumber(value) {
        if (!value) return '';
        // Remove all non-digits
        const numbers = value.replace(/\D/g, '');
        // Limit to 10 digits
        const limitedNumbers = numbers.slice(0, 10);
        // Format based on length
        if (limitedNumbers.length <= 3) return limitedNumbers;
        if (limitedNumbers.length <= 6) return limitedNumbers.slice(0, 3) + '-' + limitedNumbers.slice(3);
        return limitedNumbers.slice(0, 3) + '-' + limitedNumbers.slice(3, 6) + '-' + limitedNumbers.slice(6);
    }

    // Update the full phone display
    function updateFullPhone() {
        const areaCode = areaCodeInput.value || '+52';
        const phoneNumber = phoneNumberInput.value || '';
        fullPhoneDisplay.textContent = 'Complete: +' + areaCode + (phoneNumber ? '' + phoneNumber : '');
    }

    // Initialize phone inputs
    function initPhoneFields() {
        // Check if we have a value from Django (for edit mode)
        if (phoneNumberInput.dataset.initialValue) {
            const fullNumber = phoneNumberInput.dataset.initialValue;
            if (fullNumber.includes('-')) {
                const [areaCode, number] = fullNumber.split('-');
                areaCodeInput.value = areaCode;
                phoneNumberInput.value = formatPhoneNumber(number);
            } else {
                phoneNumberInput.value = formatPhoneNumber(fullNumber);
            }
        }
        updateFullPhone();
    }

    // Event listeners
    phoneNumberInput.addEventListener('input', function(e) {
        e.target.value = formatPhoneNumber(e.target.value);
        updateFullPhone();
    });

    areaCodeInput.addEventListener('input', updateFullPhone);

    phoneNumberInput.addEventListener('keypress', function(e) {
        const char = String.fromCharCode(e.which);
        if (!/[\d\-]/.test(char) && !e.ctrlKey && !e.metaKey && e.which !== 8) {
            e.preventDefault();
        }
    });

    // Initialize
    initPhoneFields();
    fullPhoneDisplay.style.cursor = 'pointer';
    fullPhoneDisplay.title = 'Click to copy full number';
});