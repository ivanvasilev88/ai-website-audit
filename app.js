document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const scanButton = document.getElementById('scanButton');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    const scoreValue = document.getElementById('scoreValue');
    const interpretiveSummary = document.getElementById('interpretiveSummary');
    const freeInsights = document.getElementById('freeInsights');
    const uncertaintySection = document.getElementById('uncertaintySection');
    const lockedInsightsSection = document.getElementById('lockedInsightsSection');
    const lockedInsights = document.getElementById('lockedInsights');
    const unlockSection = document.getElementById('unlockSection');
    const unlockButton = document.getElementById('unlockButton');
    const unlockedState = document.getElementById('unlockedState');
    const allInsights = document.getElementById('allInsights');
    const paymentModal = document.getElementById('paymentModal');
    const paymentForm = document.getElementById('paymentForm');
    const cancelPayment = document.getElementById('cancelPayment');
    const closeModal = document.querySelector('.close-modal');
    const paymentStatus = document.getElementById('paymentStatus');
    const downloadPdfButton = document.getElementById('downloadPdfButton');
    
    let currentReportId = null;
    let isUnlocked = false;
    let currentReportData = null;

    scanButton.addEventListener('click', handleScan);
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleScan();
        }
    });
    
    unlockButton.addEventListener('click', () => {
        paymentModal.classList.remove('hidden');
        // Auto-scroll to modal and focus on email input
        setTimeout(() => {
            paymentModal.scrollIntoView({ behavior: 'smooth', block: 'center' });
            const emailInput = document.getElementById('emailInput');
            if (emailInput) {
                setTimeout(() => {
                    emailInput.focus();
                }, 300);
            }
        }, 100);
    });
    
    closeModal.addEventListener('click', () => {
        paymentModal.classList.add('hidden');
    });
    
    cancelPayment.addEventListener('click', () => {
        paymentModal.classList.add('hidden');
    });
    
    paymentForm.addEventListener('submit', handlePayment);
    downloadPdfButton.addEventListener('click', handlePdfDownload);

    async function handleScan() {
        let url = urlInput.value.trim();
        
        if (!url) {
            showError('Please enter a website URL');
            return;
        }

        // Auto-add https:// if no protocol specified
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }

        // Basic URL validation
        try {
            const urlObj = new URL(url);
            if (!urlObj.hostname || urlObj.hostname.length < 3) {
                throw new Error('Invalid hostname');
            }
            // Update input with formatted URL
            urlInput.value = url;
        } catch (e) {
            showError('Please enter a valid website (e.g., example.com or www.example.com)');
            return;
        }

        // Hide previous results and errors
        hideError();
        hideResults();
        showLoading('Connecting to website...');
        scanButton.disabled = true;
        isUnlocked = false;

        try {
            // Update loading message
            setTimeout(() => {
                if (loading && !loading.classList.contains('hidden')) {
                    updateLoadingMessage('Analyzing website structure...');
                }
            }, 2000);

            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to scan website');
            }

            currentReportId = data.reportId;
            currentReportData = data;
            displayResults(data);
        } catch (err) {
            const errorMsg = err.message || 'An error occurred while scanning your website';
            showError(errorMsg, true); // Show retry option
        } finally {
            hideLoading();
            scanButton.disabled = false;
        }
    }

    function displayResults(data) {
        // 1. AI Interpretability Score (large numeric, no animation > 500ms)
        scoreValue.textContent = data.score;
        scoreValue.style.color = getScoreColor(data.score);
        
        // 2. Short interpretive summary (1-2 sentences)
        interpretiveSummary.textContent = data.summary || generateSummaryFromScore(data.score);
        
        // 3. Free Insights (Exactly 4)
        freeInsights.innerHTML = '';
        if (data.freeInsights && data.freeInsights.length > 0) {
            data.freeInsights.forEach(insight => {
                const insightEl = createInsightElement(insight, false);
                freeInsights.appendChild(insightEl);
            });
        }

        // 4. "What AI Still Doesn't Understand" section
        if (data.locked && data.lockedInsights && data.lockedInsights.length > 0) {
            uncertaintySection.classList.remove('hidden');
            lockedInsightsSection.classList.remove('hidden');
            unlockSection.classList.remove('hidden');
            unlockedState.classList.add('hidden');
            
            // 5. Locked Insights Preview (titles visible, descriptions hidden)
            lockedInsights.innerHTML = '';
            data.lockedInsights.forEach(insight => {
                const lockedEl = createLockedInsightElement(insight);
                lockedInsights.appendChild(lockedEl);
            });
        } else {
            // Unlocked state - show all insights
            uncertaintySection.classList.add('hidden');
            lockedInsightsSection.classList.add('hidden');
            unlockSection.classList.add('hidden');
            unlockedState.classList.remove('hidden');
            
            // Show all insights in unlocked state
            allInsights.innerHTML = '';
            if (data.freeInsights) {
                data.freeInsights.forEach(insight => {
                    const insightEl = createInsightElement(insight, false);
                    allInsights.appendChild(insightEl);
                });
            }
            if (data.lockedInsights) {
                data.lockedInsights.forEach(insight => {
                    // Show full insight when unlocked (remove blur)
                    const fullInsight = {
                        title: insight.title,
                        explanation: insight.explanation || 'This insight is now available.',
                        status: insight.status || 'pass'
                    };
                    const insightEl = createInsightElement(fullInsight, false);
                    allInsights.appendChild(insightEl);
                });
            }
        }

        showResults();
    }

    function createInsightElement(insight, isLocked) {
        const div = document.createElement('div');
        div.className = `insight-item ${insight.status || ''}`;
        
        const title = document.createElement('h4');
        title.className = 'insight-title';
        title.textContent = insight.title;
        
        const explanation = document.createElement('p');
        explanation.className = 'insight-explanation';
        explanation.textContent = insight.explanation;
        
        div.appendChild(title);
        if (!isLocked) {
            div.appendChild(explanation);
        }
        
        return div;
    }

    function createLockedInsightElement(insight) {
        const div = document.createElement('div');
        div.className = 'locked-insight-item';
        
        const lockIcon = document.createElement('span');
        lockIcon.className = 'lock-icon-small';
        lockIcon.textContent = '🔒';
        
        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'locked-content-wrapper';
        
        const title = document.createElement('h4');
        title.className = 'locked-insight-title';
        title.textContent = insight.title;
        
        // Show blurred description if available
        if (insight.explanation) {
            const explanation = document.createElement('p');
            explanation.className = 'locked-insight-explanation blurred';
            explanation.textContent = insight.explanation;
            contentWrapper.appendChild(explanation);
        }
        
        contentWrapper.appendChild(title);
        
        div.appendChild(lockIcon);
        div.appendChild(contentWrapper);
        
        return div;
    }

    function generateSummaryFromScore(score) {
        if (score >= 80) {
            return "AI systems have a strong understanding of your website's purpose and content.";
        } else if (score >= 60) {
            return "AI partially understands your website, but several important signals remain unclear or misinterpreted.";
        } else if (score >= 40) {
            return "AI systems form an incomplete understanding of your website, with significant interpretation gaps.";
        } else {
            return "AI struggles to form a coherent understanding of your website, with many signals missing or unclear.";
        }
    }

    async function handlePayment(e) {
        e.preventDefault();
        
        const email = document.getElementById('emailInput').value.trim();
        const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
        
        if (!email || !email.includes('@')) {
            showPaymentStatus('Please enter a valid email address', 'error');
            return;
        }
        
        const payButton = paymentForm.querySelector('.pay-button');
        payButton.disabled = true;
        payButton.textContent = 'Processing...';
        paymentStatus.classList.remove('hidden');
        paymentStatus.textContent = 'Processing payment...';
        paymentStatus.className = 'payment-status';
        
        try {
            const response = await fetch('/api/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reportId: currentReportId,
                    email: email,
                    paymentMethod: paymentMethod
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Payment failed');
            }

            showPaymentStatus('Payment successful! Full report sent to your email.', 'success');
            
            // Unlock the report
            setTimeout(async () => {
                await unlockReport();
            }, 1500);
            
        } catch (err) {
            showPaymentStatus(err.message || 'Payment processing failed', 'error');
            payButton.disabled = false;
            payButton.textContent = 'Complete Payment';
        }
    }
    
    async function unlockReport() {
        try {
            const response = await fetch('/api/unlock', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reportId: currentReportId
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to unlock report');
            }

            isUnlocked = true;
            currentReportData = data;
            displayResults(data);
            paymentModal.classList.add('hidden');
            
        } catch (err) {
            showError(err.message || 'Failed to unlock report');
        }
    }

    async function handlePdfDownload() {
        if (!currentReportId) {
            showError('No report available to download');
            return;
        }

        downloadPdfButton.disabled = true;
        downloadPdfButton.textContent = 'Generating PDF...';

        try {
            const response = await fetch('/api/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ reportId: currentReportId }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to generate PDF');
            }

            // Get HTML content
            const htmlContent = await response.text();
            
            // Mobile-friendly PDF download
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                // For mobile: Create downloadable HTML file or use share API
                const blob = new Blob([htmlContent], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `ai-audit-report-${currentReportId}.html`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                // Also try to open for printing
                const printWindow = window.open('', '_blank');
                if (printWindow) {
                    printWindow.document.write(htmlContent);
                    printWindow.document.close();
                    // On mobile, show message to use browser's print/save
                    setTimeout(() => {
                        alert('Report opened. Use your browser\'s menu to save as PDF or print.');
                    }, 500);
                }
            } else {
                // Desktop: Open in new window for printing
                const printWindow = window.open('', '_blank');
                printWindow.document.write(htmlContent);
                printWindow.document.close();
                
                // Wait for content to load, then trigger print
                setTimeout(() => {
                    printWindow.print();
                }, 500);
            }

            downloadPdfButton.disabled = false;
            downloadPdfButton.textContent = '📥 Download PDF Report';

        } catch (err) {
            showError(err.message || 'Failed to download PDF');
            downloadPdfButton.disabled = false;
            downloadPdfButton.textContent = '📥 Download PDF Report';
        }
    }
    
    function showPaymentStatus(message, type) {
        paymentStatus.textContent = message;
        paymentStatus.className = `payment-status ${type}`;
        paymentStatus.classList.remove('hidden');
    }

    function getScoreColor(score) {
        if (score >= 80) return '#48bb78';
        if (score >= 60) return '#ed8936';
        return '#f56565';
    }

    function showLoading(message = 'Analyzing your website...') {
        loading.classList.remove('hidden');
        const loadingText = loading.querySelector('p');
        if (loadingText) {
            loadingText.textContent = message;
        }
    }

    function updateLoadingMessage(message) {
        const loadingText = loading.querySelector('p');
        if (loadingText && !loading.classList.contains('hidden')) {
            loadingText.textContent = message;
        }
    }

    function hideLoading() {
        loading.classList.add('hidden');
    }

    function showResults() {
        results.classList.remove('hidden');
    }

    function hideResults() {
        results.classList.add('hidden');
    }

    function showError(message, showRetry = false) {
        error.innerHTML = message;
        if (showRetry) {
            const retryButton = document.createElement('button');
            retryButton.textContent = 'Retry';
            retryButton.className = 'retry-button';
            retryButton.style.cssText = 'margin-left: 10px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer;';
            retryButton.onclick = () => {
                error.classList.add('hidden');
                handleScan();
            };
            error.appendChild(retryButton);
        }
        error.classList.remove('hidden');
    }

    function hideError() {
        error.classList.add('hidden');
    }
});
