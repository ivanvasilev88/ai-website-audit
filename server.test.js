const request = require('supertest');
const axios = require('axios');

// Mock axios before requiring server
jest.mock('axios');

// Import server after mocking axios
const app = require('./server');

describe('API Endpoints', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('POST /api/scan', () => {
        it('should return 400 if URL is missing', async () => {
            const response = await request(app)
                .post('/api/scan')
                .send({});

            expect(response.status).toBe(400);
            expect(response.body.error).toBe('URL is required');
        });

        it('should return 400 if URL is invalid format', async () => {
            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'not-a-url' });

            expect(response.status).toBe(400);
            expect(response.body.error).toBe('Invalid URL format');
        });

        it('should return 400 if URL protocol is not http/https', async () => {
            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'ftp://example.com' });

            expect(response.status).toBe(400);
            expect(response.body.error).toBe('URL must use http or https protocol');
        });

        it('should successfully audit a website with all features', async () => {
            const mockHtml = `
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Test Website</title>
                    <meta name="description" content="This is a test description that is longer than 50 characters to pass the test">
                    <meta property="og:title" content="Test">
                    <meta property="og:description" content="Test Description">
                    <meta property="og:image" content="test.jpg">
                    <meta name="robots" content="index, follow">
                    <script type="application/ld+json">{"@context":"https://schema.org"}</script>
                </head>
                <body>
                    <header>Header</header>
                    <nav>Nav</nav>
                    <main>
                        <article>
                            <h1>Main Heading</h1>
                            <h2>Subheading</h2>
                            <img src="test.jpg" alt="Test image">
                        </article>
                    </main>
                    <footer>Footer</footer>
                </body>
                </html>
            `;

            axios.get.mockResolvedValue({ data: mockHtml });

            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'https://example.com' });

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('score');
            expect(response.body).toHaveProperty('details');
            expect(response.body.score).toBeGreaterThanOrEqual(0);
            expect(response.body.score).toBeLessThanOrEqual(100);
            expect(response.body.details).toHaveLength(8);
        });

        it('should handle websites with missing features', async () => {
            const mockHtml = `
                <!DOCTYPE html>
                <html>
                <head></head>
                <body>
                    <div>No semantic elements</div>
                </body>
                </html>
            `;

            axios.get.mockResolvedValue({ data: mockHtml });

            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'https://example.com' });

            expect(response.status).toBe(200);
            expect(response.body.score).toBeLessThan(50); // Should have low score
            expect(response.body.details).toHaveLength(8);
            
            // Check that title tag is missing
            const titleCheck = response.body.details.find(d => d.name === 'Has Title Tag');
            expect(titleCheck.points).toBe(0);
        });

        it('should handle axios errors gracefully', async () => {
            axios.get.mockRejectedValue(new Error('Network error'));

            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'https://example.com' });

            expect(response.status).toBe(500);
            expect(response.body.error).toContain('Failed to fetch or analyze website');
        });

        it('should handle timeout errors', async () => {
            axios.get.mockRejectedValue(new Error('timeout of 10000ms exceeded'));

            const response = await request(app)
                .post('/api/scan')
                .send({ url: 'https://example.com' });

            expect(response.status).toBe(500);
            expect(response.body.error).toContain('Failed to fetch or analyze website');
        });
    });
});

describe('Audit Function Logic', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('should calculate correct score for perfect website', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Perfect Website</title>
                <meta name="description" content="This is a perfect meta description that is definitely longer than 50 characters and provides great information">
                <meta property="og:title" content="Perfect Site">
                <meta property="og:description" content="Perfect Description">
                <meta property="og:image" content="perfect.jpg">
                <meta name="robots" content="index, follow">
                <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite"}</script>
            </head>
            <body>
                <header>Header</header>
                <nav>Navigation</nav>
                <main>
                    <article>
                        <h1>Main Title</h1>
                        <h2>Subtitle</h2>
                        <img src="img1.jpg" alt="Image 1">
                        <img src="img2.jpg" alt="Image 2">
                    </article>
                </main>
                <footer>Footer</footer>
            </body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://perfect.com' });

        expect(response.status).toBe(200);
        expect(response.body.score).toBeGreaterThanOrEqual(80);
        
        // All checks should pass
        response.body.details.forEach(detail => {
            expect(detail.points).toBeGreaterThan(0);
        });
    });

    it('should handle partial meta description correctly', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test</title>
                <meta name="description" content="Short">
            </head>
            <body></body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://example.com' });

        const metaDescCheck = response.body.details.find(d => d.name === 'Has Meta Description');
        expect(metaDescCheck.points).toBe(5); // Partial points for short description
    });

    it('should handle images without alt text', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head><title>Test</title></head>
            <body>
                <img src="img1.jpg">
                <img src="img2.jpg" alt="Has alt">
                <img src="img3.jpg">
            </body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://example.com' });

        const altTextCheck = response.body.details.find(d => d.name === 'Image Alt Text');
        // 1 out of 3 images have alt text = 33% = ~3 points
        expect(altTextCheck.points).toBeLessThan(5);
    });

    it('should handle multiple h1 tags correctly', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head><title>Test</title></head>
            <body>
                <h1>First H1</h1>
                <h1>Second H1</h1>
            </body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://example.com' });

        const headingCheck = response.body.details.find(d => d.name === 'Proper Heading Hierarchy');
        expect(headingCheck.points).toBe(5); // Partial points for multiple h1
    });

    it('should detect noindex robots tag', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test</title>
                <meta name="robots" content="noindex, nofollow">
            </head>
            <body></body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://example.com' });

        const robotsCheck = response.body.details.find(d => d.name === 'Crawlable by AI (Robots)');
        expect(robotsCheck.points).toBe(0);
        expect(robotsCheck.status).toBe('fail');
    });

    it('should detect microdata as structured data', async () => {
        const mockHtml = `
            <!DOCTYPE html>
            <html>
            <head><title>Test</title></head>
            <body>
                <div itemscope itemtype="https://schema.org/Person">
                    <span itemprop="name">John Doe</span>
                </div>
            </body>
            </html>
        `;

        axios.get.mockResolvedValue({ data: mockHtml });

        const response = await request(app)
            .post('/api/scan')
            .send({ url: 'https://example.com' });

        const structuredDataCheck = response.body.details.find(d => d.name === 'Structured Data (Schema.org)');
        expect(structuredDataCheck.points).toBe(10); // Microdata gets 10 points
    });
});

