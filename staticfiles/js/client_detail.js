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
    const fullPhoneDisplay = document.getElementById('fullPhoneDisplay');
    const areaCodeInput = document.getElementById('areaCode');
    const phoneNumberInput = document.getElementById('phoneNumber');

    // Only proceed if the elements exist
    if (fullPhoneDisplay && areaCodeInput && phoneNumberInput) {
        fullPhoneDisplay.addEventListener('click', function() {
            const areaCode = areaCodeInput.value || '+52';
            const phoneNumber = phoneNumberInput.value || '';
            const fullPhone = '' + areaCode + (phoneNumber ? '' + phoneNumber : '');
            
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
    }
});