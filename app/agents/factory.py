from agno.agent import Agent


class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, **kwargs) -> Agent:
        if agent_type == "basic":
            return Agent(**kwargs)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
