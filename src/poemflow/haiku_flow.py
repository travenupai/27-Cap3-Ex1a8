#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.haiku_crew.haiku_crew import HaikuCrew
import logging


# Configuração do sistema de logs
logging.basicConfig(
    filename="haiku_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class HaikuState(BaseModel):
    theme: str = "nature"  # Tema do haikai
    haiku: str = ""  # Haikai gerado


class HaikuFlow(Flow[HaikuState]):
    @start()
    def set_theme(self):
        """Define o tema do haikai com entrada do usuário"""
        try:
            logging.info("Starting: Set Theme")
            self.state.theme = input("Enter the theme of the haiku: ") or "nature"
            logging.info(f"Theme Set: {self.state.theme}")
        except Exception as e:
            logging.error(f"Error in set_theme: {e}")
            raise

    @listen(set_theme)
    def generate_haiku(self):
        """Gera o haikai utilizando o HaikuCrew"""
        try:
            logging.info("Starting: Generate Haiku")
            result = (
                HaikuCrew()
                .crew()
                .kickoff(
                    inputs={"theme": self.state.theme}
                )
            )
            self.state.haiku = result.raw
            logging.info(f"Haiku Generated: {self.state.haiku}")
        except Exception as e:
            logging.error(f"Error in generate_haiku: {e}")
            raise

    @listen(generate_haiku)
    def save_haiku(self):
        """Salva o haikai gerado em um arquivo"""
        try:
            logging.info("Starting: Save Haiku")
            haiku_filename = f"haiku_{self.state.theme.replace(' ', '_')}.txt"
            with open(haiku_filename, "w") as haiku_file:
                haiku_file.write(self.state.haiku)
            logging.info(f"Haiku Saved: {haiku_filename}")
        except Exception as e:
            logging.error(f"Error in save_haiku: {e}")
            raise


def kickoff():
    """Inicia o fluxo de geração do haikai"""
    logging.info("Starting Haiku Flow")
    try:
        haiku_flow = HaikuFlow()
        haiku_flow.kickoff()
    except Exception as e:
        logging.error(f"Haiku Flow Execution Failed: {e}")
        raise


def plot():
    """Exibe o diagrama do fluxo"""
    try:
        logging.info("Generating Haiku Flow Diagram")
        haiku_flow = HaikuFlow()
        haiku_flow.plot()
        logging.info("Haiku Flow Diagram Generated Successfully")
    except Exception as e:
        logging.error(f"Error Generating Diagram: {e}")
        raise


if __name__ == "__main__":
    option = input("Type 'run' to kickoff or 'plot' to generate a flow diagram: ").strip().lower()
    if option == "run":
        kickoff()
    elif option == "plot":
        plot()
    else:
        logging.error("Invalid option selected")
        print("Invalid option. Please type 'run' or 'plot'.")
