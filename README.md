# 🛒 E-Commerce QA Lifecycle — Selenium · Postman · GitHub · CI/CD

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions)](.github/workflows/ci.yml)
[![Selenium](https://img.shields.io/badge/UI%20Automation-Selenium%20%2B%20Pytest-43B02A?logo=selenium)](selenium_tests)
[![Postman](https://img.shields.io/badge/API%20Testing-Postman-FF6C37?logo=postman)](postman)
[![Allure](https://img.shields.io/badge/Reporting-Allure-orange)](#-reporting)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](#license)

A complete, end-to-end QA project that takes a single e-commerce
flow (Login → Product Browsing → Cart → Checkout) through the full testing
lifecycle: manual test design, UI automation, API testing, version control,
and a CI/CD pipeline with automated reporting.

**Application Under Test:** [automationexercise.com](https://automationexercise.com) —
a free, public demo e-commerce site (UI + REST API) purpose-built for QA practice.

---

## 📌 Project Highlights

- Designed a **35-case manual test suite** covering login, product browsing,
  cart, and checkout flows using **Equivalence Partitioning** and **Boundary
  Value Analysis**.
- Automated **20 regression test cases** with **Selenium WebDriver (Python)**
  using the **Page Object Model**, runnable across **Chrome, Firefox, and Edge**.
- Built a **Postman API collection with 15 requests** covering authentication,
  product listing, and order/account endpoints, including **schema validation**
  and **negative tests**.
- Configured a **GitHub Actions CI pipeline** that triggers on every push and
  publishes **Allure HTML reports** as pipeline artifacts.

---

## 🗂️ Project Structure

```
ecommerce-qa-lifecycle/
├── docs/                                # Phase 2 — Manual Testing
│   ├── 01_Test_Plan.md
│   ├── 02_Test_Scenarios.xlsx
│   ├── 03_Test_Cases.xlsx               # 35 cases (EP & BVA techniques)
│   ├── 04_Bug_Reports.xlsx              # 5 sample defect reports
│   └── 05_RTM.xlsx                      # Requirement Traceability Matrix
│
├── selenium_tests/                      # Phase 3 — Selenium Automation
│   ├── pages/                           # Page Object Model
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   ├── products_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/                           # 20 automated regression tests
│   │   ├── test_login.py                # 5 tests
│   │   ├── test_product_browsing.py     # 5 tests
│   │   ├── test_cart.py                 # 5 tests
│   │   └── test_checkout.py             # 5 tests
│   ├── utils/data_generator.py          # Unique test-data helpers
│   ├── conftest.py                      # Fixtures, multi-browser, screenshots
│   ├── pytest.ini
│   └── requirements.txt
│
├── postman/                             # Phase 4 — API Testing
│   ├── Ecommerce_API_Collection.postman_collection.json   # 15 requests
│   └── Ecommerce_API_Environment.postman_environment.json
│
├── .github/workflows/ci.yml             # Phase 6 — CI/CD (GitHub Actions + Allure)
├── .gitignore
└── README.md                            # You are here
```

---

## 🧪 Phase 2 — Manual Testing

| Deliverable | File | Description |
|---|---|---|
| Test Plan | `docs/01_Test_Plan.md` | Scope, approach, environment, schedule, risks |
| Test Scenarios | `docs/02_Test_Scenarios.xlsx` | 17 high-level scenarios across 4 modules |
| Test Cases | `docs/03_Test_Cases.xlsx` | **35 detailed cases** with steps, data, expected results, priority, and technique (EP/BVA) |
| Bug Reports | `docs/04_Bug_Reports.xlsx` | 5 sample defect reports with severity/priority/status |
| RTM | `docs/05_RTM.xlsx` | Maps 10 requirements → scenarios → test cases → automated tests → bugs |

> 20 of the 35 test cases are flagged `Automated = Y` in the Test Cases sheet
> and traced to their Selenium test function in the **Automation Reference**
> column — giving a direct line from a manual case to its automated check.

---

## 🤖 Phase 3 — Selenium Automation

**Stack:** Python · Selenium WebDriver 4 · Pytest · Page Object Model · `webdriver-manager`

### Setup
```bash
cd selenium_tests
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure test credentials
The login/checkout tests need one real account on automationexercise.com.
Sign up once via the UI (or the Postman "Create Account" request), then set:
```bash
export AE_TEST_EMAIL="your.email@example.com"        # Windows: set AE_TEST_EMAIL=...
export AE_TEST_PASSWORD="YourPassword123"
```

### Run the suite
```bash
pytest                                   # Chrome, headed, default
pytest --browser=firefox                 # Firefox
pytest --browser=edge                    # Edge
pytest --browser=chrome --headless       # Headless (used in CI)
pytest -m login                          # Run only the @pytest.mark.login tests
pytest --alluredir=allure-results        # Generate raw results for Allure
```

### View the Allure report locally
```bash
allure serve allure-results
```

### Framework design notes
- **Page Object Model** — one class per page (`pages/`), zero locators inside
  test files.
- **Explicit waits only** — `BasePage` wraps `WebDriverWait` +
  `expected_conditions`; no brittle `time.sleep()` calls in test logic.
- **Screenshots on failure** — `conftest.py`'s `pytest_runtest_makereport`
  hook captures a screenshot and attaches it to the Allure report whenever a
  test fails.
- **Cross-browser** — pass `--browser=chrome|firefox|edge`; driver binaries
  are resolved automatically via `webdriver-manager`.

---

## 🌐 Phase 4 — API Testing (Postman)

Collection: `postman/Ecommerce_API_Collection.postman_collection.json`
Environment: `postman/Ecommerce_API_Environment.postman_environment.json`

| Folder | Requests | Covers |
|---|---|---|
| 1. Products | 2 | Get product catalog; negative method check |
| 2. Categories (Brands) | 2 | Get brand/category list; negative method check |
| 3. Search | 3 | Valid keyword, empty term (BVA), missing parameter (negative) |
| 4. Login | 5 | Valid login, invalid credentials, missing email, missing password, unsupported method |
| 5. Account Management | 3 | Create account (setup), get user by email, delete account (cleanup) |

Every request asserts **both** the HTTP status code and the JSON response
contract (`responseCode`, required keys, array shapes) — see the *Tests* tab
on each request. Run via the Postman UI ("Run collection") or headlessly:

```bash
npm install -g newman newman-reporter-htmlextra
newman run postman/Ecommerce_API_Collection.postman_collection.json \
  -e postman/Ecommerce_API_Environment.postman_environment.json \
  --reporters cli,htmlextra
```

> ℹ️ AutomationExercise's API always responds `HTTP 200`; success/failure is
> communicated through the `responseCode` field inside the JSON body
> (200/201 success, 400 bad request, 404 not found, 405 method not allowed).
> Every test script accounts for this.

---

## 🔧 Phase 5 — GitHub

Recommended branching model for this project:

```
main          → always green, deployable / "portfolio-ready" state
 └─ develop    → integration branch
     ├─ feature/selenium-cart-tests
     ├─ feature/postman-login-suite
     └─ bugfix/checkout-empty-cart
```

```bash
# First-time push
git init
git add .
git commit -m "chore: initial commit — e-commerce QA lifecycle project"
git branch -M main
git remote add origin https://github.com/<your-username>/ecommerce-qa-lifecycle.git
git push -u origin main

# Working on a feature
git checkout -b feature/selenium-cart-tests
git add .
git commit -m "test: add cart regression tests with POM"
git push -u origin feature/selenium-cart-tests
# Open a Pull Request into develop/main on GitHub
```

---

## ⚙️ Phase 6 — CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`/`develop` and on
manual dispatch. It has three jobs:

1. **`ui-tests`** — installs Chrome, runs the full Selenium/Pytest suite
   headless, generates an **Allure** report, and uploads it (plus the Pytest
   HTML report and any failure screenshots) as build artifacts.
2. **`api-tests`** — runs the Postman collection via **Newman** and uploads
   an HTML report artifact.
3. **`publish-report`** — (on `main` only) publishes the Allure report to the
   `gh-pages` branch via GitHub Pages, so the latest report is viewable at
   `https://<your-username>.github.io/<repo-name>/`.

### Repository secrets required
| Secret | Purpose |
|---|---|
| `AE_TEST_EMAIL` | Email of a real registered account on automationexercise.com |
| `AE_TEST_PASSWORD` | Password for that account |

Set these under **Settings → Secrets and variables → Actions**.

### Reporting
- **Allure** — rich, interactive HTML report with step-by-step breakdowns,
  history trends, and attached failure screenshots.
- **Newman HTML Extra** — readable API test report with per-request
  pass/fail and response details.
- Both are published as downloadable **Actions artifacts** on every run, and
  the Allure report is additionally published to GitHub Pages from `main`.

---

## 🧰 Tech Stack Summary

| Layer | Tools |
|---|---|
| Manual QA | Excel (Test Plan/Scenarios/Cases/Bugs/RTM), EP & BVA techniques |
| UI Automation | Python, Selenium WebDriver, Pytest, Page Object Model |
| API Testing | Postman, Newman |
| Version Control | Git, GitHub (feature-branch workflow) |
| CI/CD | GitHub Actions |
| Reporting | Allure Framework, Pytest-HTML, Newman HTML Extra |

---

## ⚠️ Notes & Assumptions

- This project targets the **public, shared** demo site
  automationexercise.com. Locators and API contracts are based on its
  documented, long-stable structure — re-verify selectors if the site's
  markup changes, and avoid running destructive tests (e.g., account
  deletion) against an account you need to keep.
- Bug reports in `04_Bug_Reports.xlsx` are **illustrative artifacts** created
  to demonstrate professional defect-reporting practice; re-verify against
  the live site before treating them as currently-open defects.
- Checkout/payment tests use dummy card data only — the site does not
  process real payments.

---

## License

This project is provided for educational/portfolio purposes under the MIT
License.
