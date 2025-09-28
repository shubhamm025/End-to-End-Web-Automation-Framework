# 🧪 Custom Python Test Automation Framework

A robust, extensible **Python test automation framework** combining **Pytest**, **Page Object Model (POM)**, and an optional **Keyword-Driven Layer** to deliver scalable and maintainable UI automation.  

Built by [Shubham Motwani](https://github.com/shubhamm025) to **showcase best practices** in modern QA automation and provide a template for real-world projects.


---

## 📄 Project Overview

This framework solves the common problem of brittle, unorganized UI automation by combining:
- **Pytest** for lightweight test execution and fixture management.
- **Page Object Model (POM)** for clean separation of UI logic.
- **Optional Keyword-Driven Layer** for reusable, high-level business flows.
- **Allure reporting** for rich, interactive test reports.
- **Cross-browser support** to ensure reliability across environments.

It’s designed to be:
- **Extensible** – easy to add new pages, keywords, or test suites.
- **Readable** – test cases remain concise and business-focused.
- **Maintainable** – clear separation of responsibilities.

---

## ✨ Features

- ✅ **Pytest + POM + Keywords** architecture.
- ✅ Centralized **PageManager** for quick access to all Pages & Keywords.
- ✅ **Reusable high-level keywords** for common flows like login/logout.
- ✅ **Allure reporting** for visual insights.
- ✅ **Cross-browser support** (Chrome, Firefox, Edge, headless).
- ✅ **Fixtures** for suite-level and test-level setup/teardown.
- ✅ **Easy scalability** for adding new test cases.

---

**Folder/Files Explained:**
- **pages/**: Each file defines a Page Object with locators & actions.
- **keywords/**: High-level, reusable workflows (optional).
- **tests/**: Pytest test files calling POM methods or keywords.
- **conftest.py**: Defines suite-level & test-level fixtures.
- **pagemanager.py**: Single place to register and access page objects & keywords.
- **variables.py**: Centralized test data/config variables.
- **reports/**: Allure report outputs after test runs.

  <img width="1727" height="789" alt="Screenshot 2025-09-28 at 11 23 53 AM" src="https://github.com/user-attachments/assets/09b2d965-6eda-414c-bf06-8e6b54ad47d5" />

### Installation
```bash
git clone https://github.com/shubhamm025/End-to-End-Web-Automation-Framework.git
cd End-to-End-Web-Automation-Framework
pip install -r requirements.txt



