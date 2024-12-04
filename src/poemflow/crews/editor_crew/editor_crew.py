from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EditorCrew:
    """
    Classe responsável por configurar a equipe que revisa o poema.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def poem_editor(self) -> Agent:
        """
        Configura o agente responsável por revisar o poema.
        """
        return Agent(
            config=self.agents_config['poem_editor'],
        )

    @task
    def review_poem(self) -> Task:
        """
        Configura a tarefa de revisar o poema e sugerir melhorias.
        """
        return Task(
            config=self.tasks_config['review_poem'],
        )

    @crew
    def crew(self) -> Crew:
        """
        Configura a equipe de edição para executar a revisão.
        """
        return Crew(
            agents=self.agents,  # Criado automaticamente pelo decorator @agent
            tasks=self.tasks,  # Criado automaticamente pelo decorator @task
            process=Process.sequential,  # Define o fluxo de execução como sequencial
            verbose=True,  # Ativa logs detalhados
        )
