// ============================================
// BANKBASE - COMMON JAVASCRIPT
// ============================================

// Auto-close flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => {
        setTimeout(() => {
            flash.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// FORM VALIDATION
// ============================================

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const inputs = form.querySelectorAll('[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else {
            clearError(input);
        }
    });
    
    return isValid;
}

function showError(input, message) {
    clearError(input);
    input.style.borderColor = 'var(--danger)';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

function clearError(input) {
    input.style.borderColor = '';
    const existingError = input.parentNode.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
}

// ============================================
// MONEY FORMATTING
// ============================================

function formatMoney(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

// Apply money formatting to elements with class 'money'
document.addEventListener('DOMContentLoaded', function() {
    const moneyElements = document.querySelectorAll('.money');
    moneyElements.forEach(el => {
        const amount = parseFloat(el.textContent);
        if (!isNaN(amount)) {
            el.textContent = formatMoney(amount);
        }
    });
});

// ============================================
// DATE FORMATTING
// ============================================

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ============================================
// CONFIRMATION DIALOGS
// ============================================

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ============================================
// LOADING SPINNER
// ============================================

function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span>Loading...</span>';
    }
}

function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

// ============================================
// TABLE SEARCH/FILTER
// ============================================

function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        }
    });
}

// ============================================
// NUMBER INPUT VALIDATION
// ============================================

function validateNumberInput(input, min = 0, max = Infinity) {
    input.addEventListener('input', function() {
        let value = parseFloat(this.value);
        
        if (isNaN(value) || value < min) {
            this.value = min;
        } else if (value > max) {
            this.value = max;
        }
    });
}

// ============================================
// COPY TO CLIPBOARD
// ============================================

function copyToClipboard(text, buttonElement) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = buttonElement.textContent;
        buttonElement.textContent = 'Copied!';
        setTimeout(() => {
            buttonElement.textContent = originalText;
        }, 2000);
    });
}

// ============================================
// MODAL HANDLING
// ============================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
    }
}

// Close modal on outside click
window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.add('hidden');
        e.target.style.display = 'none';
    }
});

// ============================================
// FORM SUBMISSION WITH LOADING
// ============================================

function handleFormSubmit(formId, buttonId) {
    const form = document.getElementById(formId);
    const button = document.getElementById(buttonId);
    
    if (!form || !button) return;
    
    form.addEventListener('submit', function(e) {
        if (validateForm(formId)) {
            const originalText = button.innerHTML;
            showLoading(buttonId);
            
            // Form will submit naturally
            // Loading state will show until page reloads
        } else {
            e.preventDefault();
        }
    });
}

// ============================================
// ACCOUNT NUMBER FORMATTING
// ============================================

function formatAccountNumber(accountNumber) {
    // Format: XXXX-XXXX-XXXX
    return accountNumber.replace(/(.{4})/g, '$1-').slice(0, -1);
}

// ============================================
// TRANSACTION TYPE BADGE
// ============================================

function getTransactionBadge(txType) {
    const badges = {
        'DEPOSIT': 'badge-success',
        'CREDIT': 'badge-success',
        'WITHDRAWAL': 'badge-danger',
        'DEBIT': 'badge-danger',
        'TRANSFER': 'badge-info'
    };
    return badges[txType] || 'badge-info';
}

// ============================================
// STATUS BADGE
// ============================================

function getStatusBadge(status) {
    const badges = {
        'active': 'badge-success',
        'Active': 'badge-success',
        'ACTIVE': 'badge-success',
        'inactive': 'badge-danger',
        'Inactive': 'badge-danger',
        'INACTIVE': 'badge-danger',
        'pending': 'badge-warning',
        'Pending': 'badge-warning',
        'PENDING': 'badge-warning',
        'APPROVED': 'badge-success',
        'REJECTED': 'badge-danger',
        'CLOSED': 'badge-info',
        'DEFAULTED': 'badge-danger',
        'PAID': 'badge-success',
        'OVERDUE': 'badge-danger'
    };
    return badges[status] || 'badge-info';
}

// ============================================
// EXPORT UTILITIES
// ============================================

// Make functions available globally
window.bankbaseUtils = {
    validateForm,
    formatMoney,
    formatDate,
    confirmAction,
    showLoading,
    hideLoading,
    filterTable,
    validateNumberInput,
    copyToClipboard,
    openModal,
    closeModal,
    handleFormSubmit,
    formatAccountNumber,
    getTransactionBadge,
    getStatusBadge
};