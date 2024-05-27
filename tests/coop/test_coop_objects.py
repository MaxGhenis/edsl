import pytest
from edsl import (
    Agent,
    Cache,
    Coop,
    Jobs,
    QuestionCheckBox,
    QuestionFreeText,
    QuestionMultipleChoice,
    Results,
    Survey,
)


def coop_object_api_workflows(object_type, object_examples):
    coop = Coop(api_key="b")

    # 1. Ensure we are starting with a clean state
    objects = coop.get_all(object_type)
    for object in objects:
        coop.delete(object_type, object.get("uuid"))
    objects = coop.get_all(object_type)
    assert objects == [], "Expected no objects in the database."

    # 2. Test object creation and retrieval
    responses = []
    for object, visibility in object_examples:
        response = coop.create(object, visibility=visibility)
        print(response)
        assert (
            coop.get(object_type=object_type, uuid=response.get("uuid")) == object
        ), f"Expected object to be the same as the one created. "
        # assert coop.get(url=response.get("url")) == object
        responses.append(response)

    # 3. Test visibility with different clients
    coop2 = Coop(api_key="a")
    for i, response in enumerate(responses):
        object, visibility = object_examples[i]
        if visibility != "private":
            assert (
                coop2.get(object_type=object_type, uuid=response.get("uuid")) == object
            )
        else:
            with pytest.raises(Exception):
                coop2.get(object_type=object_type, uuid=response.get("uuid"))

    # 4. Cleanup
    for object in coop.get_all(object_type):
        response = coop.delete(object_type, object.get("uuid"))
        assert response.get("status") == "success"


@pytest.mark.coop
def test_coop_client_agents():
    agent_examples = [
        (Agent.example(), "public"),
        (Agent.example(), "private"),
        (Agent.example(), "public"),
        (Agent.example(), "unlisted"),
    ]
    coop_object_api_workflows("agent", agent_examples)


@pytest.mark.coop
def test_coop_client_cache():
    cache_examples = [
        (Cache.example(), "public"),
        (Cache.example(), "private"),
        (Cache.example(), "public"),
        (Cache.example(), "unlisted"),
    ]
    coop_object_api_workflows("cache", cache_examples)


@pytest.mark.coop
def test_coop_client_jobs():
    job_examples = [
        (Jobs.example(), "public"),
        (Jobs.example(), "private"),
        (Jobs.example(), "public"),
        (Jobs.example(), "unlisted"),
    ]
    coop_object_api_workflows("job", job_examples)


@pytest.mark.coop
def test_coop_client_questions():
    question_examples = [
        (QuestionMultipleChoice.example(), "public"),
        (QuestionCheckBox.example(), "private"),
        (QuestionFreeText.example(), "public"),
        (QuestionFreeText.example(), "unlisted"),
    ]
    coop_object_api_workflows("question", question_examples)


@pytest.mark.coop
def test_coop_client_results():
    results_examples = [
        (Results.example(), "public"),
        (Results.example(), "private"),
        (Results.example(), "public"),
        (Results.example(), "unlisted"),
    ]
    coop_object_api_workflows("results", results_examples)


@pytest.mark.coop
def test_coop_client_surveys():
    survey_examples = [
        (Survey.example(), "public"),
        (Survey.example(), "private"),
        (Survey.example(), "public"),
        (Survey.example(), "unlisted"),
    ]
    coop_object_api_workflows("survey", survey_examples)