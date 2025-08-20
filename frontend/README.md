# Ethio Startup Advisor - Next.js Frontend

This is the Next.js frontend for the Ethio Startup Advisor application. It provides a modern, responsive web interface for interacting with the AI-powered Ethiopian business law advisor.

## 🚀 Features

- **Modern UI**: Clean, professional interface built with Next.js and Tailwind CSS
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Status**: Shows system status and document processing state
- **Interactive Q&A**: Ask questions and get instant AI-powered answers
- **Document Management**: Process and reprocess legal documents
- **Same Functionality**: Replicates all features from the Streamlit version

## 🛠️ Setup

### Prerequisites
- Node.js 18+ installed
- FastAPI backend running (see backend README)
- Your Ethiopian legal documents in the `../data` folder

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### 3. Build for Production
```bash
npm run build
npm start
```

## 🔗 Backend Integration

This frontend is designed to work with the FastAPI backend. Make sure:

1. **Backend is running** on `http://localhost:8000`
2. **Documents are processed** in the backend
3. **API endpoints** are accessible

## 📱 UI Components

### Header
- App title and branding
- Professional appearance

### Sidebar
- System status display
- Document processing controls
- Legal sources information
- Reprocess functionality

### Main Content
- Question input interface
- Answer display
- Common questions examples
- Status messages

## 🎨 Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Color Scheme**: Matches your Streamlit app (blue theme)
- **Responsive**: Mobile-first design approach
- **Professional**: Clean, business-appropriate styling

## 📁 Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── layout.tsx      # Root layout
│       ├── page.tsx        # Main page component
│       └── globals.css     # Global styles
├── package.json            # Dependencies
├── next.config.js          # Next.js configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
└── README.md              # This file
```

## 🔧 Configuration

### Next.js Config
- API rewrites to backend
- Experimental app directory enabled

### Tailwind Config
- Custom color scheme matching your app
- Responsive breakpoints
- Component-focused styling

## 🚀 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Hot Reload
- Changes automatically refresh in browser
- Fast development iteration
- TypeScript support

## 🔮 Future Enhancements

- User authentication
- Chat history
- Document upload interface
- Advanced search features
- Multi-language support
- Dark mode toggle

## 🚨 Important Notes

- **Backend Required**: This frontend requires the FastAPI backend to function
- **Data Dependencies**: Needs legal documents in the data folder
- **API Communication**: All AI functionality comes from backend API calls
- **State Management**: Uses React hooks for local state

## 🆚 Comparison with Streamlit

| Feature | Streamlit | Next.js |
|---------|-----------|---------|
| UI Framework | Streamlit | React/Next.js |
| Styling | Streamlit components | Tailwind CSS |
| Performance | Good | Excellent |
| Customization | Limited | Unlimited |
| Mobile Experience | Basic | Responsive |
| Deployment | Streamlit Cloud | Vercel/Any hosting |
| Development Speed | Fast | Moderate |
| Scalability | Limited | High |

The Next.js version provides the same functionality with better performance, customization, and user experience.
