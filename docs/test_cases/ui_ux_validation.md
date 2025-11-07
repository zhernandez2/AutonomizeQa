# UX/UI Validation Test Cases

## Overview
Test cases focused on user error scenarios, interface responsiveness, and error message clarity. Emphasis on medical chart upload scenarios with various error conditions.

## Test Case Priority
- **P0 (Critical)**: Error handling, data validation, user safety
- **P1 (High)**: User experience, error messages, accessibility
- **P2 (Medium)**: Visual design, performance, edge cases
- **P3 (Low)**: Nice-to-have features, minor improvements

---

## TC-UI-001: Medical Chart Upload - Invalid Format (Non-PDF)
**Priority**: P0  
**Category**: Error Handling

### Objective
Verify that the UI correctly handles medical chart uploads with invalid file formats and provides clear error messages.

### Prerequisites
- Application is accessible
- Test files in various formats available (JPG, DOCX, TXT)
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Select a non-PDF file (e.g., JPG image)
4. Click "Upload" or "Submit"
5. Verify file upload is rejected
6. Verify error message is displayed
7. Verify error message is clear and actionable
8. Verify error message specifies acceptable formats
9. Verify user can retry upload
10. Verify invalid file is not saved to system

### Expected Results
- File upload is rejected immediately or after validation
- Clear error message is displayed:
  - **Message**: "Invalid file format. Please upload a PDF file."
  - **Location**: Near upload button or file selection area
  - **Visibility**: Error message is visible and readable
- Error message specifies acceptable formats: "Accepted formats: PDF"
- User can select a new file and retry
- Invalid file is not uploaded or saved
- No partial data is stored

### Pass/Fail Criteria
- **Pass**: Invalid format rejected with clear error message
- **Fail**: Invalid file accepted, unclear error, or file saved

### Test Data
- Test files: `test_chart.jpg`, `test_chart.docx`, `test_chart.txt`

---

## TC-UI-002: Medical Chart Upload - File Too Large
**Priority**: P0  
**Category**: Error Handling

### Objective
Verify that the UI handles medical chart uploads exceeding size limits and provides appropriate feedback.

### Prerequisites
- Application is accessible
- Test PDF file exceeding size limit (e.g., 50MB when limit is 25MB)
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Select a PDF file exceeding size limit (e.g., 50MB)
4. Click "Upload" or "Submit"
5. Verify file upload is rejected (either before or during upload)
6. Verify error message is displayed
7. Verify error message specifies size limit
8. Verify upload progress indicator (if shown) stops
9. Verify user can select a smaller file
10. Verify large file is not saved to system

### Expected Results
- File upload is rejected (ideally before upload starts, or during upload)
- Clear error message is displayed:
  - **Message**: "File size exceeds maximum limit. Maximum file size: 25MB. Your file: 50MB."
  - **Location**: Near upload area
  - **Actionable**: Suggests compressing or splitting file
- Size limit is clearly specified
- Upload progress (if shown) stops and clears
- User can select a new file
- Large file is not uploaded or saved
- No partial data or corrupted files are stored

### Pass/Fail Criteria
- **Pass**: Large file rejected with clear size limit message
- **Fail**: Large file accepted, unclear error, or upload continues

### Test Data
- Test file: `large_chart_50mb.pdf` (50MB PDF)

---

## TC-UI-003: Medical Chart Upload - Too Many Pages
**Priority**: P0  
**Category**: Error Handling

### Objective
Verify that the UI handles medical charts with excessive page counts and provides appropriate feedback.

### Prerequisites
- Application is accessible
- Test PDF file with excessive pages (e.g., 100 pages when limit is 50)
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Select a PDF file with excessive pages (e.g., 100 pages)
4. Click "Upload" or "Submit"
5. Verify file is processed (page count checked)
6. Verify error message is displayed if page limit exceeded
7. Verify error message specifies page limit
8. Verify error message is displayed in reasonable time (< 30 seconds)
9. Verify user can select a different file
10. Verify excessive page file is not saved

### Expected Results
- Page count is validated (either during upload or after)
- If page limit exceeded, clear error message is displayed:
  - **Message**: "Medical chart exceeds maximum page limit. Maximum pages: 50. Your chart: 100 pages. Please split the document or contact support."
  - **Location**: Near upload area or in notification
  - **Actionable**: Provides guidance on next steps
- Page limit is clearly specified
- Validation completes within reasonable time (< 30 seconds for 100 pages)
- User can select a new file
- Excessive page file is not saved
- No partial processing or data corruption

### Pass/Fail Criteria
- **Pass**: Excessive pages detected with clear error message
- **Fail**: Excessive pages accepted, unclear error, or timeout

### Test Data
- Test file: `large_chart_100pages.pdf` (100-page PDF)

---

## TC-UI-004: Medical Chart Upload - Valid PDF Success
**Priority**: P1  
**Category**: Positive Path

### Objective
Verify that valid medical chart uploads work correctly and provide positive feedback.

### Prerequisites
- Application is accessible
- Valid PDF file (within size and page limits)
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Select a valid PDF file
4. Click "Upload" or "Submit"
5. Verify upload progress indicator is shown
6. Verify file uploads successfully
7. Verify success message is displayed
8. Verify uploaded file information is displayed
9. Verify user can proceed to next step or view uploaded chart

### Expected Results
- Upload progress indicator is visible and updates
- File uploads successfully
- Clear success message is displayed:
  - **Message**: "Medical chart uploaded successfully. File: chart.pdf (25 pages)"
  - **Location**: Notification or success banner
  - **Duration**: Message is visible for sufficient time (3-5 seconds)
- Uploaded file information is displayed (name, size, pages)
- User can proceed to next step (e.g., review, submit)
- File is saved and accessible

### Pass/Fail Criteria
- **Pass**: Valid upload succeeds with clear success feedback
- **Fail**: Upload fails, unclear feedback, or file not saved

### Test Data
- Test file: `valid_chart_10pages.pdf` (10-page PDF, 5MB)

---

## TC-UI-005: Medical Chart Upload - Corrupted PDF File
**Priority**: P1  
**Category**: Error Handling

### Objective
Verify that the UI handles corrupted PDF files gracefully.

### Prerequisites
- Application is accessible
- Corrupted PDF test file
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Select a corrupted PDF file
4. Click "Upload" or "Submit"
5. Verify file validation occurs
6. Verify error message is displayed
7. Verify error message indicates file corruption
8. Verify user can select a valid file

### Expected Results
- File validation detects corruption
- Clear error message is displayed:
  - **Message**: "The uploaded file appears to be corrupted or invalid. Please ensure the file is a valid PDF and try again."
  - **Location**: Near upload area
- Error message is helpful and actionable
- User can select a new file
- Corrupted file is not saved

### Pass/Fail Criteria
- **Pass**: Corrupted file detected with clear error
- **Fail**: Corrupted file accepted or unclear error

---

## TC-UI-006: Medical Chart Upload - Network Interruption
**Priority**: P1  
**Category**: Error Handling

### Objective
Verify that the UI handles network interruptions during upload gracefully.

### Prerequisites
- Application is accessible
- Ability to simulate network interruption
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Select a valid PDF file
3. Start file upload
4. Simulate network interruption during upload (e.g., disconnect network)
5. Verify upload progress stops
6. Verify error message is displayed
7. Verify retry option is provided
8. Restore network connection
9. Verify user can retry upload
10. Verify retry resumes or restarts upload appropriately

### Expected Results
- Network interruption is detected
- Upload progress stops
- Clear error message is displayed:
  - **Message**: "Upload failed due to network error. Please check your connection and try again."
  - **Location**: Notification or error banner
- Retry button or option is provided
- After network restore, retry works
- Retry either resumes from where it stopped or restarts cleanly
- No corrupted partial uploads are saved

### Pass/Fail Criteria
- **Pass**: Network interruption handled with retry option
- **Fail**: No error shown, no retry option, or corrupted uploads

---

## TC-UI-007: Medical Chart Upload - Multiple File Selection
**Priority**: P2  
**Category**: User Experience

### Objective
Verify that the UI handles multiple file selection appropriately (if supported, or prevents it if not).

### Prerequisites
- Application is accessible
- Multiple PDF files available
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Click "Upload Chart" button
3. Attempt to select multiple files
4. Verify behavior (either allows or prevents multiple selection)
5. If allowed, verify all files are handled correctly
6. If prevented, verify clear indication that only single file is allowed
7. Verify error messages for invalid combinations

### Expected Results
- If multiple selection is not supported:
  - File picker restricts to single file selection
  - Or clear message: "Please select one file at a time"
- If multiple selection is supported:
  - All selected files are shown
  - Each file is validated individually
  - Clear indication of which files are valid/invalid
  - User can remove individual files
- Behavior is consistent and predictable

### Pass/Fail Criteria
- **Pass**: Multiple file selection handled appropriately
- **Fail**: Unclear behavior or inconsistent handling

---

## TC-UI-008: Medical Chart Upload - Drag and Drop
**Priority**: P2  
**Category**: User Experience

### Objective
Verify that drag-and-drop functionality works correctly (if supported).

### Prerequisites
- Application is accessible
- Drag-and-drop is supported
- Test PDF files available
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Verify drag-and-drop area is visible
3. Drag a valid PDF file to drop zone
4. Verify visual feedback during drag (e.g., highlight)
5. Drop the file
6. Verify file is accepted
7. Verify upload starts automatically or user can confirm
8. Test with invalid file (non-PDF)
9. Verify invalid file is rejected with appropriate message

### Expected Results
- Drag-and-drop area is clearly visible
- Visual feedback during drag (highlight, border change)
- Valid PDF files are accepted
- Upload starts automatically or requires confirmation (consistent with click upload)
- Invalid files are rejected with same error messages as click upload
- User experience is consistent between drag-drop and click upload

### Pass/Fail Criteria
- **Pass**: Drag-and-drop works correctly and consistently
- **Fail**: Drag-drop doesn't work or inconsistent with click upload

---

## TC-UI-009: Error Message Accessibility
**Priority**: P1  
**Category**: Accessibility

### Objective
Verify that error messages are accessible to all users, including those using screen readers.

### Prerequisites
- Application is accessible
- Screen reader available (or testing tool)
- User is logged in

### Test Steps
1. Trigger an error scenario (e.g., invalid file format)
2. Verify error message is displayed
3. Test with screen reader
4. Verify error message is announced by screen reader
5. Verify error message has appropriate ARIA attributes
6. Verify error message is associated with form field (if applicable)
7. Verify error message has sufficient color contrast
8. Verify error message is visible without color (color-blind friendly)

### Expected Results
- Error message is announced by screen reader
- Error message has appropriate ARIA attributes (e.g., `aria-live`, `role="alert"`)
- Error message is associated with relevant form field (`aria-describedby`)
- Error message has sufficient color contrast (WCAG AA: 4.5:1)
- Error message is distinguishable without color (e.g., icon or text indicator)
- Error message is keyboard accessible

### Pass/Fail Criteria
- **Pass**: Error messages are accessible and screen reader friendly
- **Fail**: Error messages not announced or not accessible

---

## TC-UI-010: Form Validation - Required Fields
**Priority**: P0  
**Category**: Data Validation

### Objective
Verify that required fields in forms are validated and show clear error messages.

### Prerequisites
- Application is accessible
- Form with required fields (e.g., patient ID, chart type)
- User is logged in

### Test Steps
1. Navigate to medical chart upload page
2. Leave required fields empty
3. Attempt to submit form
4. Verify form validation prevents submission
5. Verify error messages are displayed for each required field
6. Verify error messages are clear and specific
7. Verify error messages are positioned near relevant fields
8. Fill in required fields
9. Verify error messages clear when fields are filled
10. Verify form can be submitted successfully

### Expected Results
- Form validation prevents submission with empty required fields
- Clear error messages for each required field:
  - **Message**: "Patient ID is required" (or similar)
  - **Location**: Near the field, or in a summary
- Error messages are specific to each field
- Error messages clear when fields are filled correctly
- Visual indicators (e.g., red border) highlight invalid fields
- Form submits successfully when all required fields are filled

### Pass/Fail Criteria
- **Pass**: Required field validation works with clear error messages
- **Fail**: Validation fails, unclear errors, or form submits with empty fields

---

## Suggested Modifications/New Test Cases

### TC-UI-011: Medical Chart Upload - Progress Indicator Accuracy
**Priority**: P2  
Verify that upload progress indicators accurately reflect upload status.

### TC-UI-012: Medical Chart Upload - Cancel Upload
**Priority**: P2  
Verify that users can cancel ongoing uploads and system handles cancellation correctly.

### TC-UI-013: Medical Chart Upload - File Preview
**Priority**: P3  
Verify that file preview (if available) works correctly and shows accurate information.

### TC-UI-014: Medical Chart Upload - Mobile Responsiveness
**Priority**: P1  
Verify that upload functionality works correctly on mobile devices.

### TC-UI-015: Medical Chart Upload - Browser Compatibility
**Priority**: P2  
Verify that upload functionality works across different browsers (Chrome, Firefox, Safari, Edge).

