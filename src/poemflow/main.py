#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.poem_crew.poem_crew import PoemCrew
from .crews.editor_crew.editor_crew import EditorCrew
import logging
import os


# Configuração do sistema de logs
logging.basicConfig(
    filename="flow_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class PoemState(BaseModel):
    themes: list[str] = []  # Lista de temas para os poemas
    current_theme: str = ""  # Tema atual sendo processado
    sentence_count: int = 1
    poem: str = ""
    review: str = ""
    analysis: str = ""


class ExtendedPoemState(PoemState):
    """Estado estendido para incluir detalhes adicionais"""
    pass


class PoemFlow(Flow[ExtendedPoemState]):
    @start()
    def set_themes(self):
        """Define uma lista de temas para o fluxo"""
        try:
            logging.info("Starting: Set Themes")
            themes_input = input("Enter themes separated by commas: ").strip()
            self.state.themes = [theme.strip() for theme in themes_input.split(",") if theme.strip()]
            logging.info(f"Themes Set: {self.state.themes}")
        except Exception as e:
            logging.error(f"Error in set_themes: {e}")
            raise

    @listen(set_themes)
    def process_theme(self):
        """Itera sobre os temas e processa um de cada vez"""
        try:
            logging.info("Starting: Process Theme")
            for theme in self.state.themes:
                logging.info(f"Processing Theme: {theme}")
                self.state.current_theme = theme
                self.generate_sentence_count()
                self.generate_poem()
                self.review_poem()
                self.save_poem()
        except Exception as e:
            logging.error(f"Error in process_theme: {e}")
            raise

    def generate_sentence_count(self):
        """Permite ao usuário definir o número de frases ou gerar automaticamente"""
        try:
            logging.info("Starting: Generate Sentence Count")
            user_input = input("Enter the number of sentences for the poem (or press Enter for automatic generation): ").strip()
        
            if user_input.isdigit():
                self.state.sentence_count = int(user_input)
                logging.info(f"User-defined Sentence Count: {self.state.sentence_count}")
            else:
                self.state.sentence_count = randint(1, 5)
                logging.info(f"Automatically Generated Sentence Count: {self.state.sentence_count}")
        
        except Exception as e:
            logging.error(f"Error in generate_sentence_count: {e}")
            raise


    def generate_poem(self):
        """Gera o poema utilizando o PoemCrew"""
        try:
            logging.info("Starting: Generate Poem")
            result = (
                PoemCrew()
                .crew()
                .kickoff(
                    inputs={
                        "sentence_count": self.state.sentence_count,
                        "theme": self.state.current_theme,
                    }
                )
            )
            self.state.poem = result.raw
            logging.info(f"Poem Generated for Theme '{self.state.current_theme}': {self.state.poem}")
        except Exception as e:
            logging.error(f"Error in generate_poem: {e}")
            raise

    def review_poem(self):
        """Revisa o poema utilizando o EditorCrew"""
        try:
            logging.info("Starting: Review Poem")
            result = (
                EditorCrew()
                .crew()
                .kickoff(inputs={"poem": self.state.poem})
            )
            self.state.review = result.raw
            logging.info(f"Poem Review Completed for Theme '{self.state.current_theme}': {self.state.review}")
        except Exception as e:
            logging.error(f"Error in review_poem: {e}")
            raise

    def save_poem(self):
        """Salva o poema e seus detalhes em arquivos"""
        try:
            logging.info("Starting: Save Poem")
            # Salvar o poema no arquivo com o nome do tema
            poem_filename = f"{self.state.current_theme.replace(' ', '_')}.txt"
            with open(poem_filename, "w") as poem_file:
                poem_file.write(self.state.poem)

            # Salvar os detalhes no arquivo de detalhes
            details_filename = f"{self.state.current_theme.replace(' ', '_')}_details.txt"
            with open(details_filename, "w") as details_file:
                details_file.write(f"Theme: {self.state.current_theme}\n")
                details_file.write(f"Sentence Count: {self.state.sentence_count}\n")
                details_file.write(f"Analysis: {self.state.analysis}\n")
                details_file.write(f"Review Suggestions: {self.state.review}\n")

            logging.info(f"Poem and Details Saved for Theme '{self.state.current_theme}'")
        except Exception as e:
            logging.error(f"Error in save_poem: {e}")
            raise


def kickoff():
    """Inicia o fluxo de geração do poema"""
    logging.info("Starting the Flow")
    try:
        poem_flow = PoemFlow()
        poem_flow.kickoff()
    except Exception as e:
        logging.error(f"Flow Execution Failed: {e}")
        raise


def plot():
    """Exibe o diagrama do fluxo"""
    try:
        logging.info("Generating Flow Diagram")
        poem_flow = PoemFlow()
        poem_flow.plot()
        logging.info("Flow Diagram Generated Successfully")
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

