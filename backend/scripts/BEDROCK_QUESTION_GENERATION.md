# Question Generation from PDFs using AWS Bedrock

Generate practice questions from PDF resources using AWS Bedrock Claude (no API key needed!).

## Prerequisites

1. **AWS Credentials**: Your AWS credentials are already configured
2. **Bedrock Access**: Ensure Claude models are enabled in your AWS account
   ```bash
   # Check if you have access to Bedrock
   aws bedrock list-foundation-models --region us-east-1
   ```

3. **Python Dependencies**:
   ```bash
   cd backend
   source venv/bin/activate
   pip install PyPDF2 boto3
   ```

## Enable AWS Bedrock (One-time Setup)

1. Go to AWS Bedrock Console: https://console.aws.amazon.com/bedrock/
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable "Claude 3.5 Sonnet" (or other Claude models)
5. Click "Save changes"
6. Wait ~1-2 minutes for access to be granted

## Quick Start

### 1. Save your web page as PDF
Save the page to your Downloads or any folder

### 2. Generate questions (Preview Mode)
```bash
cd /Users/emilyjones/Development/french-civics-test-app/backend

python scripts/generate_questions_from_pdf_bedrock.py \
  ~/Downloads/your-document.pdf \
  --document-name "French Citizenship Application Guide" \
  --category "French Culture" \
  --topic-id "cult-005" \
  --max-chunks 2 \
  --preview-only
```

### 3. Review the preview
Check the generated questions. If they look good, proceed to save them.

### 4. Generate and save
```bash
python scripts/generate_questions_from_pdf_bedrock.py \
  ~/Downloads/your-document.pdf \
  --document-name "French Citizenship Application Guide" \
  --category "French Culture" \
  --topic-id "cult-005"
```

### 5. Validate questions
```bash
python scripts/validate_generated_questions.py
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `pdf_path` | Yes | Path to PDF file | `~/Downloads/doc.pdf` |
| `--document-name` | Yes | Human-readable document name | `"French Government Guide"` |
| `--category` | Yes | One of: French History, French Politics, French Geography, French Culture | `"French Politics"` |
| `--topic-id` | Yes | Unique topic ID | `"pol-005"` |
| `--max-chunks` | No | Limit chunks (for testing) | `2` |
| `--preview-only` | No | Preview without saving | flag |
| `--model-id` | No | Bedrock model ID | Default: Claude 3.5 Sonnet |

## Categories and Topic IDs

### Existing Categories
- `French History` (Histoire de France)
- `French Politics` (Politique française)
- `French Geography` (Géographie française)
- `French Culture` (Culture française)

### Topic ID Convention
- `hist-XXX` for history topics
- `pol-XXX` for politics topics
- `geo-XXX` for geography topics
- `cult-XXX` for culture topics

Use the next available number (e.g., if you have `cult-004`, use `cult-005` for your new topic).

## Example Workflow

```bash
# 1. Set up environment
cd /Users/emilyjones/Development/french-civics-test-app/backend
source venv/bin/activate

# 2. Test with one chunk first
python scripts/generate_questions_from_pdf_bedrock.py \
  ~/Downloads/french_eu_integration.pdf \
  --document-name "France and European Integration" \
  --category "French Geography" \
  --topic-id "geo-004" \
  --max-chunks 1 \
  --preview-only

# 3. If preview looks good, generate all
python scripts/generate_questions_from_pdf_bedrock.py \
  ~/Downloads/french_eu_integration.pdf \
  --document-name "France and European Integration" \
  --category "French Geography" \
  --topic-id "geo-004"

# 4. Review and validate
python scripts/validate_generated_questions.py
```

## Cost Estimates

AWS Bedrock pricing (us-east-1, Claude 3.5 Sonnet):
- Input: $0.003 per 1K tokens (~750 words)
- Output: $0.015 per 1K tokens

Typical costs:
- 1 chunk (~3000 chars): ~$0.02
- 5 chunks: ~$0.10
- 20 chunks (full document): ~$0.40

Much cheaper than using Anthropic API directly!

## Tips for Good Results

### 1. Use Official Sources
- Government websites (.gouv.fr)
- Official study guides
- Educational resources from trusted institutions

### 2. Clean PDFs Work Best
- Text-based PDFs (not scanned images)
- Well-formatted documents
- Clear section headers

### 3. Start Small
Always use `--max-chunks 1 --preview-only` first to test

### 4. Organize Your Resources
Keep track in `resource_catalog.json`:
```json
{
  "resource_id": "res-002",
  "document_name": "France and EU Guide",
  "category": "French Geography",
  "topics": ["geo-004"],
  "date_added": "2026-01-19",
  "questions_generated": 15
}
```

## Troubleshooting

### "AccessDeniedException" from Bedrock
**Solution**: Enable Claude model access in Bedrock console (see setup above)

### "PDF text extraction failed"
**Solution**: PDF might be image-based. Try:
1. Re-saving the PDF with text selection enabled
2. Using OCR tools to convert to searchable PDF

### "Poor quality questions"
**Solution**:
- Use more focused, topic-specific documents
- Adjust chunk size if needed
- Try different sections of the document
- Manually edit in DynamoDB after generation

### "No AWS credentials"
**Solution**:
```bash
aws configure
# Or check: aws sts get-caller-identity
```

## Next Steps

After generating questions:
1. ✅ Validate them using the validation script
2. ✅ Test them in your app
3. ✅ Update your resource catalog
4. ✅ Mark good questions as `validated=True`

## Comparison: Bedrock vs Direct API

| Feature | AWS Bedrock | Anthropic API |
|---------|-------------|---------------|
| Setup | Enable in console | Need API key |
| Authentication | AWS credentials | API key management |
| Cost | ~$0.40 per document | ~$0.50 per document |
| Integration | Native AWS | External service |
| Billing | AWS bill | Separate billing |
| **Recommended** | ✅ Yes | Only if Bedrock unavailable |

Use Bedrock since you're already on AWS!
