# 🤖 AI-Powered Complaint Validation System

## Overview

The system now includes AI-powered validation to automatically detect and filter:
- ✅ Valid complaints
- ❌ Spam/fake complaints
- 🔄 Duplicate complaints
- ⚠️ Inappropriate content
- 📊 Urgency levels

---

## Features

### 1. Automatic Validation on Submission

When a student submits a complaint, the AI automatically:
- Checks if the complaint is valid
- Detects spam or advertising
- Identifies inappropriate language
- Checks for gibberish text
- Validates complaint clarity
- Detects duplicates

### 2. Spam Detection

Detects:
- Advertising keywords (viagra, casino, lottery, etc.)
- Excessive links/URLs
- Phone numbers and contact info spam
- "Get rich quick" schemes

### 3. Duplicate Detection

- Compares with recent complaints (last 30 days)
- Uses similarity matching (80%+ = duplicate)
- Shows similar complaints to user
- Prevents duplicate submissions

### 4. Content Validation

Checks for:
- Minimum length (10 characters)
- Maximum length (5000 characters)
- Valid complaint keywords
- Specific details (room numbers, locations)
- Appropriate language

### 5. Quality Indicators

Looks for:
- Problem description keywords
- Location details
- Specific issues
- Question marks (asking for help)
- Numbers and specifics

---

## How It Works

### For Students

**When submitting a complaint:**

1. **Valid Complaint** ✅
   ```
   Title: "Broken projector in Room 301"
   Description: "The projector in lecture hall 301 is not working. 
   It won't turn on and we can't attend our class properly."
   
   Result: ✅ Accepted
   Confidence: 95%
   ```

2. **Spam Detected** ❌
   ```
   Title: "Win free money now!"
   Description: "Click here to get rich quick! Buy now! Limited offer!"
   
   Result: ❌ Rejected
   Reason: "Appears to be spam or advertising"
   ```

3. **Too Short** ⚠️
   ```
   Title: "Problem"
   Description: "Bad"
   
   Result: ❌ Rejected
   Reason: "Complaint is too short"
   Suggestion: "Please provide more details"
   ```

4. **Duplicate Detected** 🔄
   ```
   Title: "Broken projector in Room 301"
   Description: "The projector doesn't work..."
   
   Result: ❌ Rejected
   Reason: "Possible duplicate complaint detected"
   Similar: CMP-ABC123 (85% match)
   ```

5. **Gibberish** ❌
   ```
   Title: "asdfghjkl"
   Description: "qwertyuiop zxcvbnm"
   
   Result: ❌ Rejected
   Reason: "Text appears to be gibberish"
   ```

---

## API Endpoints

### 1. Validate Complaint (Before Submission)

**Endpoint:** `POST /api/complaints/validate/`

**Request:**
```json
{
  "title": "Broken projector",
  "description": "The projector in room 301 is not working"
}
```

**Response:**
```json
{
  "validation": {
    "is_valid": true,
    "confidence": 0.85,
    "reason": "Complaint appears valid",
    "flags": [],
    "suggestions": [],
    "spam_score": 0.0,
    "validity_score": 0.8
  },
  "duplicate_check": {
    "is_duplicate": false,
    "confidence": 0.0,
    "similar_complaints": []
  }
}
```

### 2. Get AI Statistics (Admin Only)

**Endpoint:** `GET /api/complaints/ai-stats/`

**Response:**
```json
{
  "total_complaints": 150,
  "analyzed": 100,
  "valid_percentage": 92.5,
  "spam_detected": 5,
  "unclear_complaints": 8,
  "period": "30 days"
}
```

---

## Testing the AI Validation

### Test Case 1: Valid Complaint ✅

```bash
curl -X POST http://127.0.0.1:8000/api/complaints/validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Broken AC in Dormitory",
    "description": "The air conditioning in Block A, Room 205 has been broken for 3 days. It is very hot and uncomfortable."
  }'
```

**Expected:** `is_valid: true`, high confidence

### Test Case 2: Spam ❌

```bash
curl -X POST http://127.0.0.1:8000/api/complaints/validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Win free money!",
    "description": "Click here now! Buy viagra! Casino lottery winner! Get rich quick!"
  }'
```

**Expected:** `is_valid: false`, spam detected

### Test Case 3: Too Short ❌

```bash
curl -X POST http://127.0.0.1:8000/api/complaints/validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bad",
    "description": "Problem"
  }'
```

**Expected:** `is_valid: false`, too short

### Test Case 4: Gibberish ❌

```bash
curl -X POST http://127.0.0.1:8000/api/complaints/validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "asdfghjkl",
    "description": "qwertyuiop zxcvbnm lkjhgfdsa"
  }'
```

**Expected:** `is_valid: false`, gibberish detected

---

## Validation Rules

### Spam Keywords
- viagra, casino, lottery, prize, winner
- click here, buy now, limited offer
- free money, get rich, work from home

### Valid Complaint Keywords
- broken, not working, damaged, issue, problem
- leaking, dirty, unsafe, missing, stolen
- harassment, discrimination, unfair, delay
- noise, smell, cold, hot, water, electricity
- library, dormitory, cafeteria, classroom

### Scoring System

**Confidence Score (0-1):**
- 1.0 = Perfect complaint
- 0.8-1.0 = Very good
- 0.5-0.8 = Acceptable
- 0.0-0.5 = Rejected

**Deductions:**
- Too short: -0.3
- Too long: -0.2
- Spam detected: -0.5
- Inappropriate: -0.4
- Gibberish: -0.6
- Unclear: -0.3

---

## Frontend Integration

### Example: Validate Before Submit

```javascript
// In CreateComplaint.jsx
const validateBeforeSubmit = async () => {
  try {
    const response = await api.post('complaints/validate/', {
      title: formData.title,
      description: formData.description
    });
    
    const { validation, duplicate_check } = response.data;
    
    if (!validation.is_valid) {
      alert(`Validation failed: ${validation.reason}\n\nSuggestions:\n${validation.suggestions.join('\n')}`);
      return false;
    }
    
    if (duplicate_check.is_duplicate) {
      const similar = duplicate_check.similar_complaints[0];
      const confirm = window.confirm(
        `Similar complaint found: ${similar.tracking_id}\n` +
        `Similarity: ${(similar.similarity * 100).toFixed(0)}%\n\n` +
        `Do you still want to submit?`
      );
      return confirm;
    }
    
    return true;
  } catch (error) {
    console.error('Validation error:', error);
    return true; // Allow submission if validation fails
  }
};

const handleSubmit = async (e) => {
  e.preventDefault();
  
  // Validate first
  const isValid = await validateBeforeSubmit();
  if (!isValid) return;
  
  // Submit complaint
  // ...
};
```

---

## Admin Dashboard

### View AI Statistics

Admins can view AI validation statistics:
- Total complaints analyzed
- Percentage of valid complaints
- Spam detected count
- Unclear complaints count

**Access:** Dashboard → AI Statistics

---

## Customization

### Add Custom Keywords

Edit `backend/complaints/ai_validator.py`:

```python
# Add spam keywords
SPAM_KEYWORDS = [
    'viagra', 'casino', 'lottery',
    'your-custom-spam-word'  # Add here
]

# Add valid complaint keywords
VALID_COMPLAINT_KEYWORDS = [
    'broken', 'not working',
    'your-custom-valid-word'  # Add here
]
```

### Adjust Thresholds

```python
# In ComplaintValidator class
self.min_length = 10  # Minimum complaint length
self.max_length = 5000  # Maximum complaint length

# In validate_complaint method
is_valid = confidence > 0.5  # Adjust threshold (0-1)
```

---

## Benefits

### For Students
- ✅ Immediate feedback on complaint quality
- ✅ Prevents accidental duplicates
- ✅ Guidance on writing better complaints
- ✅ Faster processing of valid complaints

### For Admins
- ✅ Automatic spam filtering
- ✅ Reduced workload
- ✅ Better complaint quality
- ✅ Statistics and insights
- ✅ Duplicate detection

### For the System
- ✅ Improved data quality
- ✅ Reduced noise
- ✅ Better analytics
- ✅ Automated moderation

---

## Troubleshooting

### False Positives

If valid complaints are being rejected:
1. Check the validation response for specific flags
2. Adjust thresholds in `ai_validator.py`
3. Add domain-specific keywords
4. Review spam keyword list

### False Negatives

If spam is getting through:
1. Add new spam keywords
2. Increase spam detection sensitivity
3. Review flagged complaints
4. Update validation rules

---

## Future Enhancements

Potential improvements:
- 🔮 Machine learning model training
- 🌐 Multi-language support
- 📊 Advanced analytics dashboard
- 🎯 Category auto-classification
- 🔗 Integration with external AI APIs
- 📈 Sentiment analysis
- 🎨 Image content validation

---

## Summary

The AI validation system provides:
1. **Automatic spam detection**
2. **Duplicate prevention**
3. **Quality assurance**
4. **Real-time feedback**
5. **Admin insights**

All complaints are now automatically validated before submission, ensuring high-quality data and reducing admin workload!
