const express = require('express');
const cors = require('cors');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// AI Audit function
async function performAIAudit(url) {
    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout: 10000,
            maxRedirects: 5
        });

        const html = response.data;
        const $ = cheerio.load(html);
        
        const auditResults = [];
        let totalScore = 0;
        let maxScore = 0;

        // 1. Check for title tag
        const title = $('title').text().trim();
        const titleScore = title ? 10 : 0;
        auditResults.push({
            name: 'Has Title Tag',
            points: titleScore,
            maxPoints: 10,
            status: titleScore === 10 ? 'pass' : 'fail'
        });
        totalScore += titleScore;
        maxScore += 10;

        // 2. Check for meta description
        const metaDescription = $('meta[name="description"]').attr('content');
        const metaDescScore = metaDescription && metaDescription.length > 50 ? 10 : (metaDescription ? 5 : 0);
        auditResults.push({
            name: 'Has Meta Description',
            points: metaDescScore,
            maxPoints: 10,
            status: metaDescScore === 10 ? 'pass' : (metaDescScore === 5 ? 'warning' : 'fail')
        });
        totalScore += metaDescScore;
        maxScore += 10;

        // 3. Check for structured data (JSON-LD, microdata, etc.)
        const jsonLd = $('script[type="application/ld+json"]').length;
        const microdata = $('[itemscope]').length;
        const structuredDataScore = jsonLd > 0 ? 15 : (microdata > 0 ? 10 : 0);
        auditResults.push({
            name: 'Structured Data (Schema.org)',
            points: structuredDataScore,
            maxPoints: 15,
            status: structuredDataScore >= 10 ? 'pass' : 'fail'
        });
        totalScore += structuredDataScore;
        maxScore += 15;

        // 4. Check for semantic HTML (header, nav, main, article, etc.)
        const semanticElements = $('header, nav, main, article, section, aside, footer').length;
        const semanticScore = semanticElements >= 3 ? 15 : (semanticElements > 0 ? 8 : 0);
        auditResults.push({
            name: 'Semantic HTML Elements',
            points: semanticScore,
            maxPoints: 15,
            status: semanticScore >= 10 ? 'pass' : (semanticScore > 0 ? 'warning' : 'fail')
        });
        totalScore += semanticScore;
        maxScore += 15;

        // 5. Check for alt text on images
        const images = $('img').length;
        const imagesWithAlt = $('img[alt]').length;
        const altTextScore = images === 0 ? 10 : Math.round((imagesWithAlt / images) * 10);
        auditResults.push({
            name: 'Image Alt Text',
            points: altTextScore,
            maxPoints: 10,
            status: altTextScore >= 8 ? 'pass' : (altTextScore >= 5 ? 'warning' : 'fail')
        });
        totalScore += altTextScore;
        maxScore += 10;

        // 6. Check for heading hierarchy (h1, h2, etc.)
        const h1Count = $('h1').length;
        const h2Count = $('h2').length;
        const headingScore = h1Count === 1 && h2Count > 0 ? 10 : (h1Count === 1 ? 7 : (h1Count > 0 ? 5 : 0));
        auditResults.push({
            name: 'Proper Heading Hierarchy',
            points: headingScore,
            maxPoints: 10,
            status: headingScore >= 7 ? 'pass' : (headingScore > 0 ? 'warning' : 'fail')
        });
        totalScore += headingScore;
        maxScore += 10;

        // 7. Check for Open Graph tags (social media)
        const ogTags = $('meta[property^="og:"]').length;
        const ogScore = ogTags >= 3 ? 10 : (ogTags > 0 ? 5 : 0);
        auditResults.push({
            name: 'Open Graph Tags',
            points: ogScore,
            maxPoints: 10,
            status: ogScore >= 7 ? 'pass' : (ogScore > 0 ? 'warning' : 'fail')
        });
        totalScore += ogScore;
        maxScore += 10;

        // 8. Check for robots meta tag
        const robotsMeta = $('meta[name="robots"]').attr('content');
        const robotsScore = !robotsMeta || !robotsMeta.includes('noindex') ? 10 : 0;
        auditResults.push({
            name: 'Crawlable by AI (Robots)',
            points: robotsScore,
            maxPoints: 10,
            status: robotsScore === 10 ? 'pass' : 'fail'
        });
        totalScore += robotsScore;
        maxScore += 10;

        // Calculate final score
        const finalScore = Math.round((totalScore / maxScore) * 100);

        return {
            score: finalScore,
            details: auditResults
        };
    } catch (error) {
        throw new Error(`Failed to fetch or analyze website: ${error.message}`);
    }
}

// API endpoint
app.post('/api/scan', async (req, res) => {
    try {
        const { url } = req.body;

        if (!url) {
            return res.status(400).json({ error: 'URL is required' });
        }

        // Validate URL format
        let validUrl;
        try {
            validUrl = new URL(url);
        } catch (e) {
            return res.status(400).json({ error: 'Invalid URL format' });
        }

        // Ensure URL has protocol
        if (!validUrl.protocol || (!validUrl.protocol.startsWith('http'))) {
            return res.status(400).json({ error: 'URL must use http or https protocol' });
        }

        const auditResult = await performAIAudit(url);
        res.json(auditResult);
    } catch (error) {
        console.error('Error scanning website:', error);
        res.status(500).json({ 
            error: error.message || 'An error occurred while scanning the website' 
        });
    }
});

// Only start server if this file is run directly (not when imported for testing)
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on http://localhost:${PORT}`);
    });
}

module.exports = app;

