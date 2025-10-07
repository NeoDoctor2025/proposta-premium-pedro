# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web application presenting a premium methodology for plastic surgeons to launch digital products. The application showcases a 5-step methodology (Discovery, Strategy, Production, Launch, Scale) through a sophisticated, mobile-first interface designed for medical specialists.

## Architecture

### Application Structure

- **Flask Backend**: Main application in `app.py` with route handlers for all pages
- **Serverless Deployment**: Configured for Netlify Functions via `netlify/functions/app.py`
- **Template System**: Jinja2 templates in `templates/` directory with inheritance from `base.html`
- **Static Assets**: CSS, JavaScript, and images in `static/` directory

### Key Components

**Main Application (`app.py`)**:
- Route handlers for all pages: `/sobre`, `/cases`, `/metodologia`, `/servicos`, `/investimento`, `/faq`
- Contact form submission with email integration (via `/submit-contact`)
- Environment-based configuration for development vs production
- Email functionality configured via environment variables (SMTP credentials)

**Serverless Function (`netlify/functions/app.py`)**:
- WSGI adapter for Netlify Functions using `serverless-wsgi`
- Handles path resolution and imports from project root
- Comprehensive error handling with detailed JSON responses

**Template Architecture**:
- `base.html`: Base template with common layout and navigation
- Page-specific templates inherit from base and override content blocks
- All templates receive `current_year` and `active_page` context variables

## Development Commands

### Local Development

```bash
# Run Flask development server
python app.py
# Runs on http://0.0.0.0:5000 with debug mode enabled
```

### Testing

No automated tests are currently configured. Manual testing workflow:

1. Start local server: `python app.py`
2. Test all routes:
   - `/` (redirects to `/sobre`)
   - `/sobre`, `/cases`, `/metodologia`, `/servicos`, `/investimento`, `/faq`
3. Test contact form submission at `/submit-contact`

### Deployment

**Netlify (Primary)**:
- Deployment is fully automated via Git integration
- Build command: `npm run build` (defined in `package.json`)
- Functions directory: `netlify/functions`
- Python version: 3.9 (set in `netlify.toml`)
- All configuration in `netlify.toml`

**Environment Variables** (configure in Netlify dashboard):
- `SESSION_SECRET`: Flask session secret key
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`: Email configuration
- `SENDER_EMAIL`: Email sender address

## Dependencies

**Python** (defined in `requirements.txt` and `pyproject.toml`):
- Flask 3.0.3
- email-validator 2.1.1
- serverless-wsgi 3.0.3

**Node** (minimal, for build process):
- Node 18 (specified in `package.json` and `netlify.toml`)

## Important Technical Details

### Request Handling

- AJAX requests are detected via `X-Requested-With: XMLHttpRequest` header
- Contact form returns JSON for AJAX requests, redirects for traditional form submission
- Flash messages use Bootstrap alert classes: `success`, `danger`

### Path Resolution

The serverless function adds project root to Python path and changes working directory to ensure proper imports and template/static file resolution.

### Error Handling

- Development mode: Full debug output enabled via `app.run(debug=True)`
- Production mode: Debug disabled in `app.config['DEBUG'] = False`
- Comprehensive logging configured with `logging.basicConfig(level=logging.DEBUG)`

### Security Headers

Configured in `netlify.toml`:
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## File Organization

```
├── app.py                          # Main Flask application
├── netlify/
│   └── functions/
│       └── app.py                  # Serverless function wrapper
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── about.html                  # Landing/about page
│   ├── cases.html                  # Success cases showcase
│   ├── methodology.html            # 5-step methodology
│   ├── services.html               # Services description
│   ├── investment.html             # Pricing and investment
│   └── faq.html                    # Frequently asked questions
├── static/
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript files
│   └── assets/                     # Images and media
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata
├── netlify.toml                    # Netlify configuration
└── package.json                    # Node scripts and metadata
```

## Common Workflows

### Adding a New Page

1. Create route handler in `app.py`:
   ```python
   @app.route('/new-page')
   def new_page():
       current_year = datetime.now().year
       return render_template('new-page.html', current_year=current_year, active_page='new-page')
   ```

2. Create template in `templates/new-page.html` extending `base.html`

3. Update navigation in `base.html` if needed

### Modifying Email Configuration

Email functionality is configured but requires environment variables. Update SMTP settings in Netlify dashboard or locally via environment variables. The `send_email()` function in `app.py` handles email sending.

### Updating Dependencies

Update `requirements.txt` AND `pyproject.toml` to maintain consistency. Netlify uses `requirements.txt` for installation.
