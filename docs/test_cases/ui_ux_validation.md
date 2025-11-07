# UX/UI Validation Test Cases

## Overview
Test cases focused on user error scenarios during medical chart upload, assessing interface responsiveness and error message clarity. These manual test cases validate the user experience when common errors occur.

---

## TC-UI-001: Medical Chart Upload - Invalid File Format
**Category**: Error Handling  
**Priority**: High | **Risk**: Medium | **Complexity**: Low

### Objective
Verify that the UI correctly handles medical chart uploads with invalid file formats and provides clear, actionable error messages.

### Prerequisites
- Application is accessible
- Test files in various formats available (JPG, DOCX, TXT)
- User is logged in with appropriate permissions

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" or "Choose File" button
3. Select a non-PDF file (e.g., `test_chart.jpg`)
4. Click "Upload" or "Submit"
5. Observe the system response
6. Verify error message content and clarity
7. Verify user can retry with correct format

### Expected Results
- File upload is rejected before or during validation
- Clear error message is displayed: 
  - **Message**: "Invalid file format. Please upload a PDF file."
  - **Location**: Near upload button with appropriate styling (red text/border)
- Error message specifies acceptable formats: "Accepted formats: PDF"
- User can immediately select a new file without page refresh
- Invalid file is not saved to system
- No partial data is stored or processed

### Pass/Fail Criteria
- **Pass**: Invalid format is rejected with clear, helpful error message; user can retry
- **Fail**: Invalid file is accepted, error message is unclear/missing, or file is saved

### Test Data
- Invalid files: `test_chart.jpg`, `test_chart.docx`, `test_chart.txt`
- Valid file for retry: `valid_chart.pdf`

---

## TC-UI-002: Medical Chart Upload - File Too Large
**Category**: Error Handling  
**Priority**: Medium | **Risk**: Low | **Complexity**: Low

### Objective
Verify that the system handles oversized file uploads gracefully with clear size limits and helpful error messages.

### Prerequisites
- Application has defined file size limit (e.g., 10MB)
- Test files of various sizes available
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Verify size limit is displayed (e.g., "Maximum file size: 10MB")
3. Select a PDF file exceeding size limit (e.g., 15MB PDF)
4. Click "Upload"
5. Observe system response
6. Verify error message clarity
7. Verify file size information is accessible

### Expected Results
- File size limit is clearly displayed before upload attempt
- Upload is rejected with clear error message:
  - **Message**: "File size exceeds maximum limit of 10MB. Current file size: 15MB."
  - **Action**: "Please compress or select a smaller file."
- Error includes both limit and actual file size
- Upload button remains functional for retry
- No partial upload or processing occurs
- System performance remains stable

### Pass/Fail Criteria
- **Pass**: Clear size limit displayed; oversized file rejected with helpful error message
- **Fail**: Size limit unclear, file accepted, or system hangs/crashes

### Test Data
- Large file: `large_chart_15mb.pdf` (15MB)
- Valid file: `normal_chart_5mb.pdf` (5MB)

---

## TC-UI-003: Medical Chart Upload - Excessive Page Count
**Category**: Error Handling  
**Priority**: Low | **Risk**: Low | **Complexity**: Medium

### Objective
Verify that the system handles medical charts with excessive page counts and provides clear guidance on limits.

### Prerequisites
- System has page count limit (e.g., 50 pages)
- Test PDFs with varying page counts available
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Check if page count limit is displayed
3. Upload a PDF with excessive pages (e.g., 75 pages)
4. Click "Upload"
5. Wait for validation/processing
6. Observe error handling
7. Verify error message provides actionable guidance

### Expected Results
- Page count limit is displayed: "Maximum pages: 50"
- File is rejected after processing/validation
- Clear error message:
  - **Message**: "Document exceeds maximum page limit. Found 75 pages, limit is 50 pages."
  - **Suggestion**: "Please split the document or remove unnecessary pages."
- Progress indicator shown during processing (if applicable)
- User can upload a different file
- System remains responsive

### Pass/Fail Criteria
- **Pass**: Page limit clear; excessive pages rejected with actionable error message
- **Fail**: Limit unclear, file accepted, or system becomes unresponsive

### Test Data
- Excessive: `medical_chart_75pages.pdf` (75 pages)
- Valid: `medical_chart_30pages.pdf` (30 pages)

---

## Suggested Additional Test Scenarios

### TC-UI-004: Medical Chart Upload - Corrupted File
Verify system handles corrupted PDF files gracefully without crashing. Test with a corrupted PDF that cannot be opened or processed. Expected: Clear error message like "File is corrupted or cannot be read. Please upload a valid PDF file." System remains stable and allows retry.

### TC-UI-005: Medical Chart Upload - Network Interruption During Upload
Test behavior when network connection is lost mid-upload. Verify upload stops appropriately, user receives clear error message, and can retry without data corruption. Expected: "Upload interrupted due to network error. Please check your connection and try again." with option to resume or restart upload.

---

## Test Environment Requirements
- **Browser**: Chrome (latest), Firefox (latest), Edge (latest)
- **Network**: Stable connection, ability to simulate interruptions
- **Test Data**: Various PDF files with different sizes, page counts, formats
- **Access**: Valid user credentials with upload permissions
