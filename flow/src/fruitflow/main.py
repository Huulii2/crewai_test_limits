#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, and_, or_
from crewai.flow.persistence import persist, SQLiteFlowPersistence

from fruitflow.crews.poem_crew.poem_crew import PoemCrew

class PoemState(BaseModel):
    sentence_count: int = 1
    poem1: str = ""
    poem1_length: str = ""
    poem2: str = ""
    
class Asd(BaseModel):
    id: str = ""

class PoemFlow(Flow[PoemState]):
    def __init__(self):
        super().__init__()
        self.poem_crew = PoemCrew().crew()
        
    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem1(self):
        print("Generating poem\n")
        result = (
            self.poem_crew
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated\n", result.raw)
        self.state.poem1 = result.raw
    
    @listen(generate_sentence_count)
    def generate_poem2(self):
        print("Generating poem\n")
        result = (
            self.poem_crew
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated\n", result.raw)
        self.state.poem2 = result.raw

    @router(generate_poem1)
    def poem1_length_decider(self):
        print("Deciding length\n")
        if (len(self.state.poem1) < 150):
            print("Poem1 is short")
            return "short1"
        else:
            print("Poem1 is long")
            return "long1"
        
    @listen("short1")
    def poem1_length_short(self):
        self.state.poem1_length = "short"
        
    @listen("long1")
    def poem1_length_long(self):
        self.state.poem1_length = "long"
        


    @listen(or_(poem1_length_short, poem1_length_long))
    @persist(SQLiteFlowPersistence())
    def save_poem(self):
        print("Saving poem\n")
        # print(self.state)
        with open("poem.txt", "w") as f:
            f.writelines(
                "Poem1 length: " + self.state.poem1_length +
                "\n" +
                self.state.poem1 + 
                "\n\n" + 
                self.state.poem2)



def kickoff():
    poem_flow = PoemFlow()
    PoemFlow().kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
