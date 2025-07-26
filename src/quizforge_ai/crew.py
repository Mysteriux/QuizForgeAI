from crewai import Crew
from dotenv import load_dotenv
from crewai import Agent, LLM, Crew, Task, Process
from crewai.project import agent, task, CrewBase
from tools.extract_pdf_content_tool import ExtractPDFContentTool
from models.quiz import QuizOutput

load_dotenv()


@CrewBase
class QuizForgeAICrew:
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
    )
    agents_config = 'config/agent.yaml'
    tasks_config = 'config/task.yaml'

    @agent
    def pdf_analyzer(self) -> Agent:
      return Agent(
          config=self.agents_config['pdf_analyzer'],
          verbose=True,
          allow_delegation=False,
          llm=self.llm,
          tools=[ExtractPDFContentTool()]
      )

    @agent
    def quiz_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['quiz_generator'],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    
    @task
    def pdf_analyzer_task(self) -> Task:
      print(f'creating analyze task')
      return Task(
          config=self.tasks_config['pdf_analyzer_task'],
      )

    @task
    def quiz_generator_task(self) -> Task:
      return Task(
        config=self.tasks_config['quiz_generator_task'],
        output_pydantic=QuizOutput
    )
    
    
    def crew(self) -> Crew:
        return Crew(
            agents=[self.pdf_analyzer(), self.quiz_generator()],
            tasks=[self.pdf_analyzer_task(), self.quiz_generator_task()],
            verbose=True,
            process=Process.sequential,
        )