# McDonald's Drive-Thru AI Ordering System

A Next.js application that demonstrates an AI-powered McDonald's drive-thru ordering system. This project is a fork of the original [Realtime API Agents Demo](https://github.com/openai/swarm) that maintains all original functionality while adding a new fast food ordering system. 100% of the code I wrote was written by AI.

## Demo

https://raw.githubusercontent.com/Jake0826/drive-thru-ai/openai-realtime-agents/demo.mp4

## Features

- **AI-Powered Drive-Thru Ordering**: Experience a realistic McDonald's drive-thru ordering system with natural conversation
- **Interactive Menu Display**: Browse the menu with categories and items in a responsive sidebar
- **Real-time Order Tracking**: See your order update in real-time as you speak with the AI
- **Voice Interaction**: Talk naturally with the AI using voice or text input
- **Push-to-Talk Mode**: Optional push-to-talk functionality for clearer communication
- **Order Management**: Add, remove, or modify items in your order with ease
- **Total Calculation**: Automatic calculation of order totals as you build your meal

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Menu Items

The application includes a McDonald's-style menu with the following items:

### Food
- French Fries
  - Small ($2.99)
  - Medium ($3.99)
  - Large ($4.99)
- Chicken Nuggets
  - 6 pieces ($3.99)
  - 10 pieces ($5.99)
  - 20 pieces ($7.99)

### Drinks
- Milkshakes (Chocolate, Vanilla, Strawberry)
  - Small ($4.99)
  - Medium ($5.99)
  - Large ($6.99)
- Sodas (Coke, Diet Coke)
  - Small ($1.99)
  - Medium ($2.99)
  - Large ($3.99)

## Original Project Features

This fork maintains all the original functionality from the base project, including:
- Sequential agent handoffs according to a defined agent graph
- Background escalation to more intelligent models
- State machine-based prompting for accurate data collection
- Voice activity detection and PTT modes
- Comprehensive event logging
- Multiple agent scenarios (front desk authentication, customer service retail)
- Agent transfer capabilities
- Background model escalation

For more details about the original project's features and configuration, please refer to the [original repository](https://github.com/openai/swarm).

## Technologies Used

- Next.js
- React
- TypeScript
- OpenAI API
- Tailwind CSS

## License

MIT
