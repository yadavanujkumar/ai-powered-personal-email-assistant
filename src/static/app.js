/**
 * AI Email Assistant - Frontend Application
 */

document.addEventListener('DOMContentLoaded', () => {
    const fetchEmailsButton = document.getElementById('fetch-emails');
    const emailList = document.getElementById('email-list');
    const loadingIndicator = document.getElementById('loading');
    const emailCount = document.getElementById('email-count');

    let currentEmails = [];

    /**
     * Show/hide loading indicator
     */
    function setLoading(isLoading) {
        loadingIndicator.classList.toggle('active', isLoading);
        fetchEmailsButton.disabled = isLoading;
    }

    /**
     * Display error message
     */
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        emailList.insertBefore(errorDiv, emailList.firstChild);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    /**
     * Create priority badge
     */
    function createPriorityBadge(priority) {
        const badge = document.createElement('span');
        badge.className = `badge priority-${priority}`;
        badge.textContent = priority;
        return badge;
    }

    /**
     * Create category badge
     */
    function createCategoryBadge(category) {
        const badge = document.createElement('span');
        badge.className = 'badge category';
        badge.textContent = category;
        return badge;
    }

    /**
     * Create sentiment badge
     */
    function createSentimentBadge(sentiment) {
        const badge = document.createElement('span');
        const sentimentClass = sentiment === 'POSITIVE' ? 'sentiment-positive' : 'sentiment-negative';
        badge.className = `badge ${sentimentClass}`;
        badge.textContent = sentiment;
        return badge;
    }

    /**
     * Analyze an email
     */
    async function analyzeEmail(emailId, content) {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error('Failed to analyze email');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error analyzing email:', error);
            throw error;
        }
    }

    /**
     * Summarize an email
     */
    async function summarizeEmail(content) {
        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error('Failed to summarize email');
            }

            const data = await response.json();
            return data.summary;
        } catch (error) {
            console.error('Error summarizing email:', error);
            throw error;
        }
    }

    /**
     * Generate reply for an email
     */
    async function generateReply(content) {
        try {
            const response = await fetch('/api/reply', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error('Failed to generate reply');
            }

            const data = await response.json();
            return data.reply;
        } catch (error) {
            console.error('Error generating reply:', error);
            throw error;
        }
    }

    /**
     * Display analysis results in email card
     */
    function displayAnalysisResult(card, analysis, type) {
        // Remove existing result if any
        const existing = card.querySelector('.analysis-result');
        if (existing) {
            existing.remove();
        }

        const resultDiv = document.createElement('div');
        resultDiv.className = 'analysis-result';

        const title = document.createElement('h4');
        const content = document.createElement('div');

        if (type === 'analyze') {
            title.textContent = '📊 Analysis Results';
            
            // Create structured content
            const priorityP = document.createElement('p');
            priorityP.innerHTML = '<strong>Priority:</strong> ';
            const priorityText = document.createTextNode(`${analysis.priority.priority.toUpperCase()} (Score: ${analysis.priority.score})`);
            priorityP.appendChild(priorityText);
            
            const categoryP = document.createElement('p');
            categoryP.innerHTML = '<strong>Category:</strong> ';
            const categoryText = document.createTextNode(analysis.category.category);
            categoryP.appendChild(categoryText);
            
            const sentimentP = document.createElement('p');
            sentimentP.innerHTML = '<strong>Sentiment:</strong> ';
            const sentimentText = document.createTextNode(`${analysis.sentiment.sentiment} (Confidence: ${analysis.sentiment.confidence})`);
            sentimentP.appendChild(sentimentText);
            
            content.appendChild(priorityP);
            content.appendChild(categoryP);
            content.appendChild(sentimentP);
            
            if (analysis.priority.keywords.length > 0) {
                const keywordsP = document.createElement('p');
                keywordsP.innerHTML = '<strong>Keywords:</strong> ';
                const keywordsText = document.createTextNode(analysis.priority.keywords.join(', '));
                keywordsP.appendChild(keywordsText);
                content.appendChild(keywordsP);
            }
        } else if (type === 'summarize') {
            title.textContent = '📝 Summary';
            const summaryP = document.createElement('p');
            summaryP.textContent = analysis;
            content.appendChild(summaryP);
        } else if (type === 'reply') {
            title.textContent = '💬 Suggested Reply';
            const replyP = document.createElement('p');
            replyP.textContent = analysis;
            content.appendChild(replyP);
        }

        resultDiv.appendChild(title);
        resultDiv.appendChild(content);
        card.appendChild(resultDiv);
    }

    /**
     * Create email card with enhanced features
     */
    function createEmailCard(email) {
        const li = document.createElement('li');
        li.className = 'email-card';

        // Email header with badges
        const header = document.createElement('div');
        header.className = 'email-header';

        const badges = document.createElement('div');
        badges.className = 'email-badges';
        
        // Will be populated after analysis
        header.appendChild(badges);

        // Email snippet
        const snippet = document.createElement('div');
        snippet.className = 'email-snippet';
        snippet.textContent = email.snippet || 'No preview available';

        // Actions
        const actions = document.createElement('div');
        actions.className = 'email-actions';

        const analyzeBtn = document.createElement('button');
        analyzeBtn.textContent = '🔍 Analyze';
        analyzeBtn.className = 'btn-small';
        analyzeBtn.onclick = async () => {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';
            try {
                const analysis = await analyzeEmail(email.id, email.snippet);
                
                // Update badges
                badges.innerHTML = '';
                badges.appendChild(createPriorityBadge(analysis.priority.priority));
                badges.appendChild(createCategoryBadge(analysis.category.category));
                if (analysis.sentiment.sentiment !== 'UNKNOWN') {
                    badges.appendChild(createSentimentBadge(analysis.sentiment.sentiment));
                }
                
                // Display results
                displayAnalysisResult(li, analysis, 'analyze');
            } catch (error) {
                showError('Failed to analyze email');
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🔍 Analyze';
            }
        };

        const summarizeBtn = document.createElement('button');
        summarizeBtn.textContent = '📝 Summarize';
        summarizeBtn.className = 'btn-small btn-info';
        summarizeBtn.onclick = async () => {
            summarizeBtn.disabled = true;
            summarizeBtn.textContent = 'Summarizing...';
            try {
                const summary = await summarizeEmail(email.snippet);
                displayAnalysisResult(li, summary, 'summarize');
            } catch (error) {
                showError('Failed to summarize email');
            } finally {
                summarizeBtn.disabled = false;
                summarizeBtn.textContent = '📝 Summarize';
            }
        };

        const replyBtn = document.createElement('button');
        replyBtn.textContent = '💬 Reply';
        replyBtn.className = 'btn-small btn-success';
        replyBtn.onclick = async () => {
            replyBtn.disabled = true;
            replyBtn.textContent = 'Generating...';
            try {
                const reply = await generateReply(email.snippet);
                displayAnalysisResult(li, reply, 'reply');
            } catch (error) {
                showError('Failed to generate reply');
            } finally {
                replyBtn.disabled = false;
                replyBtn.textContent = '💬 Reply';
            }
        };

        actions.appendChild(analyzeBtn);
        actions.appendChild(summarizeBtn);
        actions.appendChild(replyBtn);

        // Assemble card
        li.appendChild(header);
        li.appendChild(snippet);
        li.appendChild(actions);

        return li;
    }

    /**
     * Fetch and display emails
     */
    fetchEmailsButton.addEventListener('click', async () => {
        setLoading(true);
        emailList.innerHTML = '';

        try {
            const response = await fetch('/api/emails');
            if (!response.ok) {
                throw new Error('Failed to fetch emails');
            }

            const data = await response.json();
            const emails = data.emails || [];
            
            currentEmails = emails;
            emailCount.textContent = `${emails.length} email${emails.length !== 1 ? 's' : ''} loaded`;

            if (emails.length === 0) {
                emailList.innerHTML = '<li class="email-card">No emails found</li>';
                return;
            }

            emails.forEach(email => {
                const card = createEmailCard(email);
                emailList.appendChild(card);
            });
        } catch (error) {
            console.error('Error fetching emails:', error);
            showError('Failed to fetch emails. Please try again.');
        } finally {
            setLoading(false);
        }
    });
});