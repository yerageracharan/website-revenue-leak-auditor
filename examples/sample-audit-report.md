# Illustrative audit finding (not a live website result)

This example demonstrates the report format. It is synthetic and must not be presented as an actual audit of a business.

### [Medium impact] Viewport configuration is missing

- **Category:** Mobile usability
- **Page:** `https://example.test/`
- **Confidence:** High
- **Evidence:** No `meta name="viewport"` tag was found in the inspected HTML.
- **Why it may matter:** The mobile layout may render at an unexpected scale for phone visitors.
- **Recommended action:** Add a responsive viewport declaration and test the page at common mobile widths.
- **How to verify:** Inspect the page at 375 px and 390 px viewport widths and confirm content remains readable without unintended horizontal scrolling.
