# OpenAI Realtime Agents

A Next.js application that demonstrates real-time agent interactions using OpenAI's API. This is a fork of the original [Realtime API Agents Demo](https://github.com/openai/swarm) that maintains all original functionality while adding a new fast food ordering system.

## Features

- All original features from the base project:
  - Sequential agent handoffs according to a defined agent graph
  - Background escalation to more intelligent models
  - State machine-based prompting for accurate data collection
  - Voice activity detection and PTT modes
  - Comprehensive event logging
- New Fast Food Ordering System:
  - Fast Food Order Agent: Helps customers order from a menu with items like French Fries, Chicken Nuggets, and Drinks
  - Interactive menu display with categories and items
  - Real-time order tracking and total calculation
  - Responsive UI with collapsible sidebar

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

## Fast Food Menu

The application includes a fast food menu with the following items:

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
- Multiple agent scenarios (front desk authentication, customer service retail)
- Voice interaction capabilities
- Real-time event logging
- Agent transfer capabilities
- Background model escalation
- State machine-based prompting

For more details about the original project's features and configuration, please refer to the [original repository](https://github.com/openai/swarm).

## Technologies Used

- Next.js
- React
- TypeScript
- OpenAI API
- Tailwind CSS

## License

MIT
