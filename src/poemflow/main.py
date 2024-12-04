#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.poem_crew.poem_crew import PoemCrew


class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class ExtendedPoemState(PoemState):
    """Estado estendido para incluir detalhes do poema"""
    theme: str = "default"  # Tema do poema


class PoemFlow(Flow[ExtendedPoemState]):
    @start()
    def generate_sentence_count(self):
        """Gera uma contagem aleatória de frases para o poema"""
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def set_theme(self):
        """Define o tema do poema com entrada do usuário"""
        print("Setting poem theme")
        self.state.theme = input("Enter the theme of the poem: ") or "default"

    @listen(set_theme)
    def generate_poem(self):
        """Gera o poema utilizando o PoemCrew"""
        print("Generating poem")
        result = (
            PoemCrew()
            .crew()
            .kickoff(
                inputs={
                    "sentence_count": self.state.sentence_count,
                    "theme": self.state.theme,
                }
            )
        )
        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        """Salva o poema em poem.txt e os detalhes em poem_details.txt"""
        print("Saving poem")

        # Salvar o poema no arquivo poem.txt
        with open("poem.txt", "w") as poem_file:
            poem_file.write(self.state.poem)

        # Salvar os detalhes (número de frases e tema) no arquivo poem_details.txt
        with open("poem_details.txt", "w") as details_file:
            details_file.write(f"Sentence Count: {self.state.sentence_count}\n")
            details_file.write(f"Theme: {self.state.theme}\n")

def kickoff():
    """Inicia o fluxo de geração do poema"""
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    """Exibe o diagrama do fluxo (opcional, caso o CrewAI tenha suporte a isso)"""
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
