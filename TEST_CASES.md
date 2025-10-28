# Feedback Management Application - Test Cases

## Test Environment
- **URL**: Your Replit application URL
- **Admin Account**: admin@example.com / admin123
- **Test User Account**: Create during testing

---

## 1. User Authentication Tests

### TC-001: User Registration - Valid Data
**Steps:**
1. Navigate to the application homepage
2. Click "Register" in the navigation
3. Enter valid details:
   - Name: "John Doe"
   - Email: "john.doe@test.com"
   - Password: "Test123!"
4. Click "Register" button

**Expected Result:**
- Success message displayed
- Redirected to login page
- User account created in database

**Priority:** High

---

### TC-002: User Registration - Duplicate Email
**Steps:**
1. Navigate to registration page
2. Enter email that already exists (e.g., "admin@example.com")
3. Fill other fields with valid data
4. Click "Register"

**Expected Result:**
- Error message: "Email already exists"
- User remains on registration page
- No new account created

**Priority:** High

---

### TC-003: User Login - Valid Credentials
**Steps:**
1. Navigate to login page
2. Enter email: "john.doe@test.com"
3. Enter correct password
4. Click "Login"

**Expected Result:**
- Successfully logged in
- Redirected to user dashboard
- User name displayed in navigation

**Priority:** High

---

### TC-004: User Login - Invalid Credentials
**Steps:**
1. Navigate to login page
2. Enter email: "john.doe@test.com"
3. Enter wrong password
4. Click "Login"

**Expected Result:**
- Error message: "Invalid email or password"
- User remains on login page
- Not logged in

**Priority:** High

---

### TC-005: Admin Login
**Steps:**
1. Navigate to login page
2. Enter email: "admin@example.com"
3. Enter password: "admin123"
4. Click "Login"

**Expected Result:**
- Successfully logged in
- Redirected to admin dashboard
- Admin navigation options visible

**Priority:** High

---

### TC-006: User Logout
**Steps:**
1. Login as any user
2. Click "Logout" in navigation

**Expected Result:**
- User logged out
- Redirected to homepage
- Authentication required for protected pages

**Priority:** Medium

---

## 2. Feedback Submission Tests (Regular Users)

### TC-007: Submit Feedback - All Fields
**Steps:**
1. Login as regular user (not admin)
2. Navigate to homepage
3. Fill form:
   - Name: "John Doe" (pre-filled)
   - Type: "Praise"
   - Feedback: "Great service!"
   - Rating: 5 stars
   - Image: Upload valid image (PNG/JPG)
4. Click "Submit Feedback"

**Expected Result:**
- Success message displayed
- Sentiment analysis result shown (should be "Positive")
- Form cleared
- Feedback saved in database

**Priority:** High

---

### TC-008: Submit Feedback - Required Fields Only
**Steps:**
1. Login as regular user
2. Fill only required fields:
   - Type: "Bug Report"
   - Feedback: "App crashes on startup"
3. Click "Submit"

**Expected Result:**
- Feedback submitted successfully
- Sentiment analysis shows "Negative"
- Name defaults to user's name
- No rating or image

**Priority:** High

---

### TC-009: Submit Feedback - Anonymous (Not Logged In)
**Steps:**
1. Logout if logged in
2. Navigate to homepage
3. Fill feedback form:
   - Name: Leave empty
   - Type: "General Feedback"
   - Feedback: "Nice interface"
4. Submit

**Expected Result:**
- Feedback submitted successfully
- Name shows as "Anonymous"
- Sentiment analyzed correctly

**Priority:** Medium

---

### TC-010: Submit Feedback - Image Upload (Valid)
**Steps:**
1. Login as regular user
2. Fill feedback form
3. Upload image (PNG, JPG, JPEG, or GIF under 5MB)
4. Verify preview appears
5. Submit

**Expected Result:**
- Image preview displayed before submission
- Success message shown
- Image saved in uploads folder
- Image linked to feedback record

**Priority:** High

---

### TC-011: Submit Feedback - Image Upload (Invalid Size)
**Steps:**
1. Fill feedback form
2. Upload image larger than 5MB
3. Try to submit

**Expected Result:**
- Error alert: "File size must be less than 5MB"
- Image input cleared
- Form not submitted

**Priority:** Medium

---

### TC-012: Submit Feedback - Image Upload (Invalid Format)
**Steps:**
1. Fill feedback form
2. Upload non-image file (.pdf, .txt, etc.)
3. Try to submit

**Expected Result:**
- Error alert showing allowed formats
- Image input cleared
- Form not submitted

**Priority:** Medium

---

### TC-013: Sentiment Analysis - Positive Text
**Steps:**
1. Submit feedback with text: "Excellent product! Love it!"
2. Check sentiment result

**Expected Result:**
- Sentiment detected as "Positive"
- Sentiment score displayed (compound > 0.05)

**Priority:** High

---

### TC-014: Sentiment Analysis - Negative Text
**Steps:**
1. Submit feedback with text: "Terrible experience, worst app ever!"
2. Check sentiment result

**Expected Result:**
- Sentiment detected as "Negative"
- Sentiment score displayed (compound < -0.05)

**Priority:** High

---

### TC-015: Sentiment Analysis - Neutral Text
**Steps:**
1. Submit feedback with text: "The app works fine."
2. Check sentiment result

**Expected Result:**
- Sentiment detected as "Neutral"
- Sentiment score between -0.05 and 0.05

**Priority:** Medium

---

## 3. Admin Feedback Restriction Tests (NEW FEATURE)

### TC-016: Admin Cannot See Feedback Form
**Steps:**
1. Login as admin (admin@example.com / admin123)
2. Navigate to homepage (/)

**Expected Result:**
- Feedback form is NOT displayed
- Admin notice with purple gradient background shown
- Notice states: "As an administrator, you cannot submit feedback"
- Button "Go to Admin Dashboard" is visible

**Priority:** HIGH

---

### TC-017: Admin Notice Navigation
**Steps:**
1. Login as admin
2. Navigate to homepage
3. Click "Go to Admin Dashboard" button

**Expected Result:**
- Redirected to admin dashboard (/admin)
- Dashboard loads with all analytics

**Priority:** Medium

---

### TC-018: Admin API Restriction - Direct POST
**Steps:**
1. Login as admin
2. Use browser developer tools or API client
3. Attempt to POST to /api/feedback with valid data

**Expected Result:**
- Response status: 403 Forbidden
- Response message: "Administrators cannot submit feedback"
- No feedback record created

**Priority:** HIGH

---

### TC-019: Regular User Can Still Submit
**Steps:**
1. Login as regular user
2. Navigate to homepage
3. Verify feedback form is visible and functional
4. Submit feedback

**Expected Result:**
- Form displays normally
- Feedback submits successfully
- No admin restriction applied

**Priority:** HIGH

---

## 4. User Dashboard Tests

### TC-020: View User's Own Feedback
**Steps:**
1. Login as user who has submitted feedback
2. Click "My Feedback" in navigation

**Expected Result:**
- Dashboard displays only user's feedback
- Feedback shown in reverse chronological order
- All feedback details visible (type, text, rating, sentiment, image)

**Priority:** High

---

### TC-021: Filter by Sentiment
**Steps:**
1. Navigate to user dashboard
2. Select "Positive" from sentiment filter

**Expected Result:**
- Only positive feedback displayed
- Other sentiments hidden
- Filter updates in real-time

**Priority:** Medium

---

### TC-022: Filter by Type
**Steps:**
1. Navigate to user dashboard
2. Select specific type (e.g., "Praise") from type filter

**Expected Result:**
- Only selected type displayed
- Other types hidden

**Priority:** Medium

---

### TC-023: Delete Own Feedback
**Steps:**
1. Navigate to user dashboard
2. Click delete button on a feedback item
3. Confirm deletion

**Expected Result:**
- Feedback removed from view
- Success confirmation
- Database record deleted

**Priority:** Medium

---

### TC-024: View Feedback Image
**Steps:**
1. Navigate to dashboard
2. Click on feedback image thumbnail

**Expected Result:**
- Modal opens with full-size image
- Click outside or close button to dismiss

**Priority:** Low

---

## 5. Admin Dashboard Tests

### TC-025: Access Admin Dashboard - Admin User
**Steps:**
1. Login as admin
2. Click "Admin" in navigation

**Expected Result:**
- Admin dashboard loads
- Statistics cards displayed
- Charts rendered
- Feedback table populated

**Priority:** High

---

### TC-026: Access Admin Dashboard - Regular User
**Steps:**
1. Login as regular user (not admin)
2. Try to access /admin directly

**Expected Result:**
- Access denied message
- Redirected to homepage
- Admin dashboard not accessible

**Priority:** High

---

### TC-027: View Summary Statistics
**Steps:**
1. Login as admin
2. Navigate to admin dashboard
3. Check statistics cards

**Expected Result:**
- Total Feedback count displayed
- Average Rating shown (X/5 or N/A)
- Positive, Negative, Neutral counts accurate
- Numbers match actual database records

**Priority:** High

---

### TC-028: Sentiment Pie Chart
**Steps:**
1. View admin dashboard
2. Check sentiment distribution pie chart

**Expected Result:**
- Chart shows Positive (green), Negative (red), Neutral (gray)
- Percentages add up to 100%
- Chart is interactive (hover shows details)

**Priority:** Medium

---

### TC-029: Feedback Type Bar Chart
**Steps:**
1. View admin dashboard
2. Check feedback type bar chart

**Expected Result:**
- All feedback types shown
- Counts accurate for each type
- Bars properly scaled

**Priority:** Medium

---

### TC-030: Category vs Sentiment Donut Chart (NEW FEATURE)
**Steps:**
1. View admin dashboard
2. Locate "Category vs Sentiment Distribution" donut chart
3. Hover over segments

**Expected Result:**
- Donut chart displays category-sentiment combinations
- Labels like "Praise-Positive", "Complaint-Negative", etc.
- Hover shows count and percentage
- Colors differentiate categories
- Chart updates with time filter

**Priority:** HIGH

---

### TC-031: Time Filter - Past 10 Days (NEW FEATURE)
**Steps:**
1. Navigate to admin dashboard
2. Select "Past 10 days" from time filter dropdown
3. Wait for data to load

**Expected Result:**
- All statistics update to show only last 10 days
- All charts refresh with filtered data
- Feedback table shows only recent feedback
- Counts match filtered period

**Priority:** HIGH

---

### TC-032: Time Filter - Past 1 Month (NEW FEATURE)
**Steps:**
1. Navigate to admin dashboard
2. Select "Past 1 month" from filter
3. Observe changes

**Expected Result:**
- Data filtered to last 30 days
- Statistics, charts, and table update
- More data than "10 days" filter

**Priority:** HIGH

---

### TC-033: Time Filter - All Time (NEW FEATURE)
**Steps:**
1. Navigate to admin dashboard
2. Select "All time" from filter

**Expected Result:**
- All feedback displayed
- Statistics show complete dataset
- Default state of dashboard

**Priority:** Medium

---

### TC-034: Filter Feedback Table - Sentiment
**Steps:**
1. Navigate to admin dashboard
2. Select "Positive" from sentiment filter

**Expected Result:**
- Table shows only positive feedback
- Other rows hidden
- Filter works independently of time filter

**Priority:** Medium

---

### TC-035: Filter Feedback Table - Type
**Steps:**
1. Navigate to admin dashboard
2. Select "Complaint" from type filter

**Expected Result:**
- Table shows only complaints
- Works with sentiment filter (AND logic)

**Priority:** Medium

---

### TC-036: Delete Feedback - Admin (NEW FEATURE)
**Steps:**
1. Login as admin
2. Navigate to admin dashboard
3. Click "Delete" button on any feedback row
4. Confirm deletion in popup

**Expected Result:**
- Confirmation dialog appears
- After confirming: feedback deleted
- Success message shown
- Dashboard automatically refreshes
- Feedback removed from database
- Associated image deleted from server

**Priority:** HIGH

---

### TC-037: Delete Feedback - Cancel (NEW FEATURE)
**Steps:**
1. Login as admin
2. Click delete button
3. Click "Cancel" on confirmation dialog

**Expected Result:**
- Deletion cancelled
- Feedback remains in table
- No changes to database

**Priority:** Medium

---

### TC-038: View Feedback Images in Admin Table
**Steps:**
1. Navigate to admin dashboard
2. View feedback with images
3. Click on image thumbnail

**Expected Result:**
- Modal opens with full image
- Image displays correctly
- Modal closes on click outside

**Priority:** Low

---

## 6. Security & Access Control Tests

### TC-039: Unauthorized Access - Admin Routes
**Steps:**
1. Logout completely
2. Try to access /admin directly

**Expected Result:**
- Redirected to login page
- Cannot access admin features

**Priority:** High

---

### TC-040: Unauthorized Access - User Dashboard
**Steps:**
1. Logout completely
2. Try to access /dashboard

**Expected Result:**
- Redirected to login page
- Cannot view dashboard

**Priority:** High

---

### TC-041: SQL Injection Prevention
**Steps:**
1. Try submitting feedback with SQL code: `'; DROP TABLE feedback; --`
2. Submit

**Expected Result:**
- Text saved as literal string
- No SQL injection executed
- Database intact

**Priority:** High

---

### TC-042: XSS Prevention
**Steps:**
1. Submit feedback with script tag: `<script>alert('XSS')</script>`
2. View in dashboard

**Expected Result:**
- Script not executed
- Text displayed as plain text
- No alert popup

**Priority:** High

---

## 7. UI/UX Tests

### TC-043: Responsive Design - Mobile
**Steps:**
1. Open app on mobile device or resize browser
2. Navigate through all pages

**Expected Result:**
- All elements resize appropriately
- Charts remain readable
- Navigation works on mobile
- Forms are usable

**Priority:** Medium

---

### TC-044: Form Validation - Empty Required Fields
**Steps:**
1. Try to submit feedback without filling type or text
2. Click submit

**Expected Result:**
- Browser validation prevents submission
- Error indicators on required fields
- Helpful validation messages

**Priority:** Medium

---

### TC-045: Star Rating - Interactive
**Steps:**
1. Hover over star rating
2. Click on 3rd star
3. Submit feedback

**Expected Result:**
- Stars highlight on hover
- Selected rating (3) submitted correctly
- Visual feedback clear

**Priority:** Low

---

### TC-046: Image Preview
**Steps:**
1. Upload image to feedback form
2. Observe preview

**Expected Result:**
- Preview appears immediately
- Confirmation message shown
- Image displays correctly scaled

**Priority:** Low

---

## 8. Edge Cases & Error Handling

### TC-047: Empty Database State
**Steps:**
1. Fresh database with no feedback
2. Login as admin
3. View dashboard

**Expected Result:**
- Charts display empty state gracefully
- No errors shown
- Statistics show 0

**Priority:** Medium

---

### TC-048: Network Error Handling
**Steps:**
1. Submit feedback while offline
2. Observe error handling

**Expected Result:**
- Error message displayed
- User informed to try again
- Form data preserved

**Priority:** Low

---

### TC-049: Large Text Input
**Steps:**
1. Submit feedback with very long text (1000+ characters)
2. Submit

**Expected Result:**
- Text saved completely
- Displays properly in table
- No truncation errors

**Priority:** Low

---

### TC-050: Special Characters in Input
**Steps:**
1. Submit feedback with special characters: `!@#$%^&*()_+-=[]{}|;':",./<>?`
2. Submit and view

**Expected Result:**
- All characters saved correctly
- Displayed without encoding issues
- No errors

**Priority:** Medium

---

## Test Summary Template

| Test ID | Test Case | Status | Notes |
|---------|-----------|--------|-------|
| TC-001 | User Registration - Valid | ☐ Pass ☐ Fail | |
| TC-002 | User Registration - Duplicate | ☐ Pass ☐ Fail | |
| ... | ... | ... | ... |

---

## Priority Definitions
- **High**: Core functionality, must work
- **Medium**: Important features, should work
- **Low**: Nice to have, can have minor issues

## Bug Report Template
```
Bug ID: BUG-XXX
Test Case: TC-XXX
Severity: Critical/High/Medium/Low
Description: [What went wrong]
Steps to Reproduce: [Detailed steps]
Expected: [What should happen]
Actual: [What actually happened]
Environment: [Browser, OS]
Screenshots: [If applicable]
```
