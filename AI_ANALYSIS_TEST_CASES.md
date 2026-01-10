# AI Complaint Analysis - Test Cases

## How to Test

1. **Start Backend**: `cd backend && python manage.py runserver`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Login** as a student
4. **Go to** "Create Complaint" page
5. **Type** in the description field
6. **Wait 1 second** - AI Assistant will appear on the right

---

## Test Cases

### ✅ TEST 1: Vague Complaint (Should Score LOW)

**Type this:**
```
The library is bad
```

**Expected Results:**
- Completeness: ~20-30%
- Clarity: ~30-40%
- Tone: Frustrated/Neutral
- Urgency: Low
- Missing: location, date, details, evidence
- Suggestions: "Be more specific", "Add location", "Include date"

**Pass Criteria:** Scores below 50%, multiple missing items

---

### ✅ TEST 2: Better Complaint (Should Score MEDIUM)

**Type this:**
```
The main library is too noisy during exam week
```

**Expected Results:**
- Completeness: ~40-50%
- Clarity: ~60-80%
- Tone: Frustrated
- Urgency: Medium
- Missing: specific date, evidence
- Suggestions: "Add specific dates", "Provide evidence"

**Pass Criteria:** Scores 40-70%, fewer missing items

---

### ✅ TEST 3: Complete Complaint (Should Score HIGH)

**Type this:**
```
The main library building 3, room 205 has been extremely noisy during the past week (Dec 1-6). Students are talking loudly and there are no quiet study zones. This is affecting my ability to prepare for final exams. I have photos of the crowded areas.
```

**Expected Results:**
- Completeness: ~80-90%
- Clarity: ~85-95%
- Tone: Professional/Frustrated
- Urgency: Medium
- Missing: Maybe just minor details
- Suggestions: Minimal or none

**Pass Criteria:** Scores above 80%, very few missing items

---

### ✅ TEST 4: Urgent/Critical Complaint

**Type this:**
```
URGENT: There is no water in dormitory building 5 since this morning. This is an emergency affecting 200 students.
```

**Expected Results:**
- Completeness: ~60-70%
- Clarity: ~70-80%
- Tone: Frustrated/Professional
- **Urgency: CRITICAL** ⚠️
- Missing: specific time, evidence
- Suggestions: "Add specific time", "Provide photos"

**Pass Criteria:** Urgency detected as "critical" or "high"

---

### ✅ TEST 5: Angry/Unprofessional Tone

**Type this:**
```
The stupid cafeteria staff are rude and the food is disgusting! This is unacceptable!
```

**Expected Results:**
- Completeness: ~20-30%
- Clarity: ~30-40%
- **Tone: ANGRY** 😠
- Urgency: Medium
- Missing: location, date, evidence, specifics
- Suggestions: "Be more professional", "Add specific details", "Provide evidence"

**Pass Criteria:** Tone detected as "angry", suggestions to be professional

---

### ✅ TEST 6: Academic Complaint

**Type this:**
```
My professor has not uploaded grades for the midterm exam that we took 3 weeks ago. This is affecting my ability to know where I stand in the course.
```

**Expected Results:**
- Completeness: ~50-60%
- Clarity: ~70-80%
- Tone: Professional
- Urgency: Medium
- Category: Academic
- Missing: professor name, course code, evidence
- Suggestions: "Add professor name", "Include course details"

**Pass Criteria:** Category detected as "Academic"

---

### ✅ TEST 7: Harassment Complaint (Should be HIGH URGENCY)

**Type this:**
```
A staff member in the registrar office made inappropriate comments to me yesterday. I felt uncomfortable and unsafe.
```

**Expected Results:**
- Completeness: ~40-50%
- Clarity: ~60-70%
- Tone: Professional/Concerned
- **Urgency: HIGH or CRITICAL**
- Category: Harassment
- Missing: specific details, witness, evidence
- Suggestions: "Provide specific details", "Include witness information"

**Pass Criteria:** High urgency, harassment category detected

---

### ✅ TEST 8: IT/Technical Issue

**Type this:**
```
The WiFi in the computer lab has been down for 2 days. Students cannot access online resources for assignments.
```

**Expected Results:**
- Completeness: ~50-60%
- Clarity: ~70-80%
- Tone: Professional
- Urgency: Medium/High
- Category: IT
- Missing: specific lab location, evidence
- Suggestions: "Add lab number", "Specify which building"

**Pass Criteria:** IT category detected

---

### ✅ TEST 9: Short Text (Should Show Hint)

**Type this:**
```
Bad food
```

**Expected Results:**
- Should show: "Start typing your complaint to get AI-powered suggestions..."
- No analysis (text too short)

**Pass Criteria:** No analysis shown, only hint message

---

### ✅ TEST 10: Real-time Updates

**Type this slowly, word by word:**
```
The → library → is → too → noisy → during → exam → week → in → building → 3
```

**Expected Results:**
- AI Assistant should update after each pause
- Scores should improve as more details are added
- Missing items should decrease
- Suggestions should become more specific

**Pass Criteria:** Real-time updates visible, scores improve progressively

---

## Visual Checks

### ✅ Completeness Bar
- Should be GREEN
- Should fill from 0% to score%
- Should animate smoothly

### ✅ Clarity Bar  
- Should be BLUE
- Should fill from 0% to score%
- Should animate smoothly

### ✅ Urgency Badge
- 🚨 Critical = RED
- ⚠️ High = ORANGE
- 📌 Medium = BLUE
- ℹ️ Low = GREEN

### ✅ Tone Badge
- ✅ Professional = GREEN
- 😠 Angry = RED
- 😤 Frustrated = ORANGE
- 😐 Neutral = GRAY

### ✅ Missing Information
- Should show as yellow/orange list items
- Should decrease as complaint improves

### ✅ Suggestions
- Should show as green list items
- Should be actionable and specific
- Should update based on content

---

## Performance Tests

### ✅ Response Time
- Analysis should complete within 2-5 seconds
- Loading indicator should show during analysis
- No UI freezing

### ✅ Debouncing
- Should wait 1 second after typing stops
- Should not spam API with every keystroke
- Should cancel previous requests if typing resumes

---

## Error Handling Tests

### ✅ Network Error
1. Disconnect internet
2. Type complaint
3. Should show error in console
4. Should not crash

### ✅ API Error
1. Stop backend server
2. Type complaint
3. Should show error in console
4. Should not crash

### ✅ Invalid Response
- Should handle malformed JSON
- Should fall back to basic analysis

---

## Browser Console Checks

Look for these logs:
- `⏱️ Debounce complete, starting analysis...`
- `🔍 Analyzing text: ...`
- `✅ Analysis received: {...}`

If you see errors:
- `❌ Analysis error: ...` - Check backend is running
- `Error response: ...` - Check API endpoint

---

## Success Criteria

✅ All 10 test cases pass
✅ Visual elements render correctly
✅ Real-time updates work smoothly
✅ Performance is acceptable (< 5s)
✅ Error handling works
✅ No console errors (except expected network errors)

---

## Quick Backend Test

Run this to test backend directly:
```bash
cd backend
python test_ai_analysis.py
```

Should show analysis for 5 test cases with scores and suggestions.
