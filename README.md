
# Automation Testing Using AI in Large-Scale Projects

The **Python and Selenium Auditing Framework (PSAF)** is a web auditing project designed to evaluate websites across three core quality areas: Technical Health, SEO Best Practices, and Accessibility.

The framework uses Python, Flask, and Selenium WebDriver with headless Chrome to inspect web pages and generate structured audit results.

## Project Overview

Modern large-scale applications make it challenging to maintain consistent website quality. PSAF provides an automated approach to identifying website issues and helping development teams improve quality, accessibility, and search engine optimization.

## Key Features

- Automated website auditing through a URL-based interface.
- Technical Health assessment.
- SEO Best Practices validation.
- Accessibility testing.
- Automated browser testing using Selenium WebDriver.
- Headless Chrome execution.
- Structured pass/fail audit results.
- PDF audit report generation.

## System Architecture

PSAF consists of three main layers:

1. **Presentation Layer – Flask:** Accepts the target website URL and displays audit results.
2. **Business Logic Layer – Python:** Coordinates the automated test cases and processes results.
3. **Execution Layer – Selenium WebDriver:** Uses headless Chrome to load websites and inspect their elements.

## Technology Stack

- Python
- Flask
- Selenium WebDriver
- Google Chrome
- ChromeDriver
- HTML, CSS (for the web interface)

## Testing Categories

The framework includes 15 automated test cases grouped into three categories.

| Category | Description |
|---|---|
| Technical Health | Checks website connectivity, HTTPS, broken links, and page loading. |
| SEO Best Practices | Validates metadata, heading structure, and search engine optimization elements. |
| Accessibility | Checks image alternative text and other foundational accessibility requirements. |

## Research Findings

The framework was evaluated through a pilot study involving 20 live websites.

### Reported Results

| Testing Category | Compliance |
|---|---:|
| Technical Health | 45% |
| SEO Best Practices | 30% |
| Accessibility | 25% |

### Commonly Identified Issues

- Multiple H1 headings: 12 out of 20 websites.
- Missing image ALT attributes: 10 out of 20 websites.
- Missing meta descriptions: 9 out of 20 websites.

These findings demonstrate the importance of automated website auditing for maintaining website quality.

## Future Enhancements

- Integration with Google Lighthouse and Core Web Vitals.
- Extended WCAG 2.1 and 2.2 accessibility testing.
- Secure authentication support for protected websites.
- Docker-based deployment.
- Selenium Grid and Kubernetes integration.
- AI-assisted self-healing test automation.
- Predictive and risk-based test prioritization.

**Note:** AI-assisted self-healing, predictive analytics, and large-scale deployment are proposed future enhancements, not claims about the currently implemented prototype.

## Research Paper

The complete research paper associated with this project is available in the repository.

**Paper Title:** Automation Testing Using AI in Large-Scale Projects

**Authors:**
- Nali Bhuvanesh Pranay
- Avula Sai Chaitanya
- Boina Gayatri
- Gannu Vinay Kranth

**Faculty Guide:** Mrs. Tirumalasetty Sai Lakshmi

**Institution:** Koneru Lakshmaiah Education Foundation, Andhra Pradesh, India.

### Research Paper PDF

[Read the Complete Research Paper](research/Capstone_project_final.pdf)

## Repository Structure

```text
AUTOMATION-TESTING-USING-AI-IN-LARGE-SCALE-PROJECTS/
│
├── README.md
│
├── research/
│   └── Capstone_project_final.pdf
│
└── Application Source Code/
```

## Getting Started

### Prerequisites

- Python
- Google Chrome
- Selenium WebDriver
- Flask

Install the required dependencies using the project's dependency configuration.

```bash
pip install flask selenium
```

Run the Flask application using the appropriate Python entry-point file in the project.

## Contributors

- Nali Bhuvanesh Pranay
- Avula Sai Chaitanya
- Boina Gayatri
- Gannu Vinay Kranth

---

**Project:** Automation Testing Using AI in Large-Scale Projects

**Framework:** Python and Selenium Auditing Framework (PSAF)
