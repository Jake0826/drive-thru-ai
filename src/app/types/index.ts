export interface AgentConfig {
  name: string;
  publicDescription: string;
  model?: string;
  instructions: string;
  tools: Array<{
    type: string;
    name: string;
    description: string;
    parameters: any;
  }>;
  toolLogic: {
    [key: string]: (args: any) => Promise<any>;
  };
} 