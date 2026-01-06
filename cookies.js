// GDPR Cookie Consent Management

(function() {
    'use strict';

    // Cookie utility functions
    const CookieManager = {
        // Set a cookie
        set: function(name, value, days = 365) {
            const expires = new Date();
            expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
            document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
        },

        // Get a cookie
        get: function(name) {
            const nameEQ = name + "=";
            const ca = document.cookie.split(';');
            for (let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        },

        // Delete a cookie
        delete: function(name) {
            document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
        },

        // Check if consent has been given
        hasConsent: function() {
            return this.get('cookie_consent') !== null;
        },

        // Get consent preferences
        getPreferences: function() {
            const consent = this.get('cookie_consent');
            if (!consent) return null;
            
            try {
                return JSON.parse(consent);
            } catch (e) {
                return { essential: true, analytics: false };
            }
        },

        // Save preferences
        savePreferences: function(preferences) {
            this.set('cookie_consent', JSON.stringify(preferences), 365);
            this.set('cookie_consent_date', new Date().toISOString(), 365);
        }
    };

    // Initialize cookie consent
    function initCookieConsent() {
        const consentBanner = document.getElementById('cookieConsent');
        const cookieSettings = document.getElementById('cookieSettings');
        
        // Check if user has already given consent
        if (!CookieManager.hasConsent()) {
            // Show banner after a short delay
            setTimeout(() => {
                consentBanner.classList.remove('hidden');
                consentBanner.style.display = 'flex';
            }, 1000);
        }

        // Accept All Cookies
        const acceptAllBtn = document.getElementById('acceptAllCookies');
        if (acceptAllBtn) {
            acceptAllBtn.addEventListener('click', function() {
                CookieManager.savePreferences({
                    essential: true,
                    analytics: true,
                    timestamp: new Date().toISOString()
                });
                hideConsentBanner();
                showConsentMessage('All cookies accepted. Thank you!');
            });
        }

        // Reject Non-Essential Cookies
        const rejectBtn = document.getElementById('rejectCookies');
        if (rejectBtn) {
            rejectBtn.addEventListener('click', function() {
                CookieManager.savePreferences({
                    essential: true,
                    analytics: false,
                    timestamp: new Date().toISOString()
                });
                hideConsentBanner();
                showConsentMessage('Only essential cookies enabled.');
            });
        }

        // Customize Cookies
        const customizeBtn = document.getElementById('customizeCookies');
        if (customizeBtn) {
            customizeBtn.addEventListener('click', function() {
                showCookieSettings();
            });
        }

        // Cookie Settings Modal
        const savePreferencesBtn = document.getElementById('saveCookiePreferences');
        const cancelSettingsBtn = document.getElementById('cancelCookieSettings');
        const analyticsCheckbox = document.getElementById('analyticsCookies');

        // Load current preferences into settings modal
        if (analyticsCheckbox) {
            const prefs = CookieManager.getPreferences();
            if (prefs) {
                analyticsCheckbox.checked = prefs.analytics || false;
            }
        }

        if (savePreferencesBtn) {
            savePreferencesBtn.addEventListener('click', function() {
                const preferences = {
                    essential: true, // Always true
                    analytics: analyticsCheckbox ? analyticsCheckbox.checked : false,
                    timestamp: new Date().toISOString()
                };
                CookieManager.savePreferences(preferences);
                hideCookieSettings();
                hideConsentBanner();
                showConsentMessage('Cookie preferences saved.');
            });
        }

        if (cancelSettingsBtn) {
            cancelSettingsBtn.addEventListener('click', function() {
                hideCookieSettings();
            });
        }

        // Close settings modal when clicking outside
        if (cookieSettings) {
            cookieSettings.addEventListener('click', function(e) {
                if (e.target === cookieSettings) {
                    hideCookieSettings();
                }
            });
        }
    }

    function hideConsentBanner() {
        const consentBanner = document.getElementById('cookieConsent');
        if (consentBanner) {
            consentBanner.classList.add('hidden');
            consentBanner.style.display = 'none';
        }
    }

    function showCookieSettings() {
        const cookieSettings = document.getElementById('cookieSettings');
        if (cookieSettings) {
            cookieSettings.classList.remove('hidden');
            cookieSettings.style.display = 'flex';
        }
    }

    function hideCookieSettings() {
        const cookieSettings = document.getElementById('cookieSettings');
        if (cookieSettings) {
            cookieSettings.classList.add('hidden');
            cookieSettings.style.display = 'none';
        }
    }

    function showConsentMessage(message) {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.className = 'cookie-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            font-weight: 500;
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCookieConsent);
    } else {
        initCookieConsent();
    }

    // Export CookieManager for use in other scripts
    window.CookieManager = CookieManager;
})();

