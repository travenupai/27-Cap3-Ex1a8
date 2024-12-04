from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class HaikuCrew:
    """
    Classe responsável por configurar a equipe que gera haikais.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def haiku_writer(self) -> Agent:
        """
        Configura o agente responsável por escrever haikais.
        """
        return Agent(
            config=self.agents_config['haiku_writer'],
        )

    @task
    def write_haiku(self) -> Task:
        """
        Configura a tarefa de gerar um haikai com a estrutura 5-7-5.
        """
        return Task(
            config=self.tasks_config['write_haiku'],
        )

    @crew
    def crew(self) -> Crew:
        """
        Configura a equipe de geração de haikais.
        """
        return Crew(
            agents=self.agents,  # Criado automaticamente pelo decorator @agent
            tasks=self.tasks,  # Criado automaticamente pelo decorator @task
            process=Process.sequential,  # Define o fluxo de execução como sequencial
            verbose=True,  # Ativa logs detalhados
        )
