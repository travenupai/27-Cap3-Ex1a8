from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class PoemCrew:
    """
    Classe para configurar a equipe (crew) responsável por gerar o poema.
    """

    # Caminhos para os arquivos de configuração dos agentes e tarefas
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def poem_writer(self) -> Agent:
        """
        Configura o agente responsável por escrever poemas,
        utilizando o arquivo de configuração.
        """
        return Agent(
            config=self.agents_config['poem_writer'],
        )

    @task
    def write_poem(self) -> Task:
        """
        Configura a tarefa de escrever poemas.
        Recebe como entrada o estado que inclui sentence_count e theme.
        """
        return Task(
            config=self.tasks_config['write_poem'],
        )

    @crew
    def crew(self) -> Crew:
        """
        Configura a equipe para executar as tarefas.
        """
        return Crew(
            agents=self.agents,  # Criado automaticamente pelo decorator @agent
            tasks=self.tasks,  # Criado automaticamente pelo decorator @task
            process=Process.sequential,  # Define o fluxo de execução como sequencial
            verbose=True,  # Ativa logs detalhados
        )
