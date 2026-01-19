# French Civics Test Frontend

Modern React frontend application for practicing French civics test questions with adaptive learning.

## Features

- 🔐 **AWS Cognito Authentication** - Secure user authentication
- 🎯 **Adaptive Learning** - Questions adapt to your performance level
- 📊 **Real-time Statistics** - Track your progress across topics and categories
- 📚 **15 Topics** - Covering French history, politics, geography, and culture
- ✅ **Verified Questions** - All questions based on official Livret du citoyen

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API deployed and running (see backend/README.md)

### Installation

```bash
# Install dependencies
npm install
```

### Configuration

The `.env` file is already configured with your deployed backend:

```
VITE_API_GATEWAY_URL=https://5oz651rsei.execute-api.us-east-1.amazonaws.com/prod/
VITE_COGNITO_USER_POOL_ID=us-east-1_Z3JeL9l2Z
VITE_COGNITO_CLIENT_ID=1tmqcjtq1qb93keq0cuiuna12c
VITE_COGNITO_REGION=us-east-1
```

### Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Application Structure

```
src/
├── components/          # Reusable React components
│   └── Layout.tsx      # Main layout with navigation
├── config/             # Configuration files
│   └── amplify.ts      # AWS Amplify/Cognito configuration
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication state management
├── pages/              # Page components
│   ├── HomePage.tsx    # Landing page
│   ├── PracticePage.tsx # Practice mode with questions
│   ├── TopicsPage.tsx  # Browse all topics
│   └── DashboardPage.tsx # Statistics dashboard
├── services/           # API service layer
│   └── api.ts          # Backend API client
├── styles/             # CSS stylesheets
│   └── App.css         # Main application styles
├── types/              # TypeScript type definitions
│   └── index.ts        # Shared types
├── App.tsx             # Main app component with routing
└── main.tsx            # Application entry point
```

## Key Pages

### Home Page (`/`)
- Welcome screen with feature overview
- Call-to-action buttons to start practicing or explore topics
- Available to all users (authenticated or not)

### Practice Mode (`/practice`)
- **Protected route** - requires authentication
- Displays one question at a time
- Submit answer and get immediate feedback
- Shows explanation and source reference
- Adaptive algorithm selects next question based on performance

### Topics (`/topics`)
- Browse all 15 available topics
- Filter by category (History, Politics, Geography, Culture)
- View topic descriptions and source page references

### Dashboard (`/dashboard`)
- **Protected route** - requires authentication
- View overall statistics (questions answered, accuracy, streak)
- Category-level performance breakdown
- Topic-level performance with progress bars
- Visual charts and metrics

## Authentication Flow

1. User clicks "Commencer la pratique" or "Statistiques"
2. If not authenticated, shows Amplify Authenticator UI
3. User can sign up or sign in with email/password
4. After authentication, user is redirected to the requested page
5. User profile is automatically created in backend on first API call

## API Integration

The frontend communicates with the backend through the `apiService` class:

```typescript
// Get next question (adaptive algorithm)
const { question } = await apiService.getNextQuestion();

// Submit an answer
const result = await apiService.submitAnswer({
  question_id: '...',
  user_answer: 'a',
  response_time_ms: 5000
});

// Get user statistics
const { stats } = await apiService.getUserStats();
```

All API requests automatically include the JWT token from Cognito in the Authorization header.

## Adaptive Learning

The application uses an adaptive learning algorithm:

1. **Performance Tracking** - Records all user answers with timestamps
2. **Topic Classification** - Weak (<60%), Medium (60-80%), Strong (>80%)
3. **Weighted Selection** - 60% weak topics, 30% medium, 10% strong
4. **Recency Weighting** - Recent performance (last 7 days) weighted more heavily
5. **Question Variety** - Avoids recently answered questions

## Styling

The app uses custom CSS with:
- French national colors (blue, white, red)
- Responsive design (mobile-friendly)
- Accessible UI components
- Smooth animations and transitions

## Technologies Used

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **AWS Amplify** - Cognito authentication
- **Axios** - HTTP client for API requests

## Deployment

To deploy the frontend to production:

1. **Option A: AWS S3 + CloudFront**
   ```bash
   npm run build
   aws s3 sync dist/ s3://your-bucket-name
   ```

2. **Option B: Vercel**
   ```bash
   npm install -g vercel
   vercel
   ```

3. **Option C: Netlify**
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod
   ```

Remember to update CORS settings in your backend API Gateway if deploying to a domain other than localhost.

## Troubleshooting

### Authentication Issues
- Check that `VITE_COGNITO_USER_POOL_ID` and `VITE_COGNITO_CLIENT_ID` are correct
- Verify user exists in Cognito User Pool
- Check browser console for detailed error messages

### API Connection Issues
- Verify `VITE_API_GATEWAY_URL` is correct
- Check that backend is deployed and health endpoint returns 200
- Inspect network tab in browser dev tools for API errors

### Build Errors
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 16+)
- Try clearing Vite cache: `rm -rf node_modules/.vite`

## Next Steps

- Add more questions to the database
- Implement history page to review past answers
- Add category-specific practice mode
- Implement timed quiz mode
- Add social features (leaderboards, sharing progress)
- Integrate AI question generation with validation
