import pytest
from edsl.agents import Agent
from edsl.exceptions import AgentCombinationError, JobsRunError
from edsl.jobs import Jobs
from edsl.jobs.Interview import Interview
from edsl.questions import QuestionMultipleChoice
from edsl.scenarios import Scenario
from edsl.surveys import Survey
from edsl.language_models import (
    LanguageModelOpenAIThreeFiveTurbo,
    LanguageModelOpenAIFour,
)


@pytest.fixture(scope="function")
def valid_job():
    q = QuestionMultipleChoice(
        question_text="How are you?",
        question_options=["Good", "Great", "OK", "Bad"],
        question_name="how_feeling",
    )
    survey = Survey(name="Test Survey", questions=[q])
    agent = Agent(traits={"trait1": "value1"})
    model = LanguageModelOpenAIThreeFiveTurbo(use_cache=True)
    scenario = Scenario({"price": 100, "quantity": 2})
    valid_job = Jobs(
        survey=survey,
        agents=[agent],
        models=[model],
        scenarios=[scenario],
    )
    yield valid_job


def test_jobs_simple_stuf(valid_job):
    # simple stuff
    assert valid_job.survey.name == "Test Survey"
    assert valid_job.agents[0].traits == {"trait1": "value1"}
    assert valid_job.models[0].model == "gpt-3.5-turbo"
    assert valid_job.scenarios[0].get("price") == 100
    # eval works and returns eval-able string
    assert "Jobs(survey=Survey(" in repr(valid_job)
    assert isinstance(eval(repr(valid_job)), Jobs)
    # serialization
    assert isinstance(valid_job.to_dict(), dict)
    assert isinstance(Jobs.from_dict(valid_job.to_dict()), Jobs)
    assert Jobs.from_dict(valid_job.to_dict()).to_dict() == valid_job.to_dict()
    # serialize and de-serialize an empty job
    empty_job = Jobs(survey=Survey(questions=[valid_job.survey._questions[0]]))
    assert Jobs.from_dict(empty_job.to_dict()).to_dict() == empty_job.to_dict()


def test_jobs_by_agents():
    q = QuestionMultipleChoice(
        question_text="How are you?",
        question_options=["Good", "Great", "OK", "Bad"],
        question_name="how_feeling",
    )
    survey = Survey(name="Test Survey", questions=[q])
    agent1 = Agent(traits={"trait1": "value1"})
    agent2 = Agent(traits={"trait2": "value2"})
    # by without existing agents
    job = survey.by(agent1)
    assert job.agents == [agent1]
    job = survey.by(agent1, agent2)
    assert job.agents == [agent1, agent2]
    assert len(job) == 2
    job = survey.by([agent1, agent2])
    assert job.agents == [agent1, agent2]
    assert len(job) == 2
    job = survey.by((agent1, agent2))
    assert job.agents == [agent1, agent2]
    assert len(job) == 2
    # by with existing agents
    job = survey.by(agent1).by(agent2)
    assert job.agents == [agent1 + agent2]
    assert len(job) == 1
    with pytest.raises(AgentCombinationError):
        job = survey.by(agent1).by(agent1)


def test_jobs_by_scenarios():
    q = QuestionMultipleChoice(
        question_text="How are you?",
        question_options=["Good", "Great", "OK", "Bad"],
        question_name="how_feeling",
    )
    survey = Survey(name="Test Survey", questions=[q])
    scenario1 = Scenario({"price": "100"})
    scenario2 = Scenario({"value": "200"})
    scenario3 = Scenario({"price": "200"})
    # by without existing scenarios
    job = survey.by(scenario1)
    assert job.scenarios == [scenario1]
    job = survey.by(scenario1, scenario2)
    assert job.scenarios == [scenario1, scenario2]
    assert len(job) == 2
    job = survey.by([scenario1, scenario2])
    assert job.scenarios == [scenario1, scenario2]
    assert len(job) == 2
    job = survey.by((scenario1, scenario2))
    assert job.scenarios == [scenario1, scenario2]
    assert len(job) == 2
    # by with existing scenarios
    job = survey.by(scenario1).by(scenario2)
    assert job.scenarios == [scenario1 + scenario2]
    assert len(job) == 1
    # if the scenarios have the same keys, new scenarios take precedence
    job = survey.by(scenario1).by(scenario3)
    assert job.scenarios == [scenario3]
    assert len(job) == 1


def test_jobs_by_models():
    q = QuestionMultipleChoice(
        question_text="How are you?",
        question_options=["Good", "Great", "OK", "Bad"],
        question_name="how_feeling",
    )
    survey = Survey(name="Test Survey", questions=[q])
    model1 = LanguageModelOpenAIThreeFiveTurbo(use_cache=True)
    model2 = LanguageModelOpenAIFour(use_cache=False)
    # by without existing models
    job = survey.by(model1)
    assert job.models == [model1]
    job = survey.by(model1, model2)
    assert job.models == [model1, model2]
    assert len(job) == 2
    job = survey.by([model1, model2])
    assert job.models == [model1, model2]
    assert len(job) == 2
    job = survey.by((model1, model2))
    assert job.models == [model1, model2]
    assert len(job) == 2
    # by with existing models
    job = survey.by(model1).by(model2)
    assert job.models == [model2]
    assert len(job) == 1


def test_jobs_interviews(valid_job):
    # on a job with existing agents, scenarios, and models
    interviews = valid_job.interviews()
    assert isinstance(interviews[0], Interview)
    assert len(interviews) == 1
    # on a job with no agents, scenarios, or models
    q = QuestionMultipleChoice(
        question_text="How are you?",
        question_options=["Good", "Great", "OK", "Bad"],
        question_name="how_feeling",
    )
    survey = Survey(questions=[q])
    job = Jobs(survey=survey)
    interviews = job.interviews()
    assert interviews[0].survey == survey
    assert interviews[0].scenario == Scenario()
    assert interviews[0].agent == Agent()
    assert interviews[0].model.model == "gpt-3.5-turbo"
    assert interviews[0].model.use_cache == True


def test_jobs_run(valid_job):
    results = valid_job.run(debug=True)
    assert len(results) == 1
    with pytest.raises(JobsRunError):
        valid_job.run(method="invalid_method")
    # with pytest.raises(JobsRunError):
    #     valid_job.run(n="x")