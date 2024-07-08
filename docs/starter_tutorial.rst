.. _starter_tutorial:

Starter Tutorial
================
This tutorial demonstrates basic steps for conducting an AI-powered survey using EDSL. 


Prerequisites
-------------
Before running the code below, ensure that you have already completed the :ref:`installation` steps and stored :ref:`api_keys` for the language models that you plan to use.

If you encounter any issues or have questions, please email us at info@expectedparrot.com or post a question at our `Discord channel <https://discord.com/invite/mxAYkjfy9m>`_.
You can also view the contents of this tutorial in an `interactive notebook <https://deepnote.com/workspace/expected-parrot-c2fa2435-01e3-451d-ba12-9c36b3b87ad9/project/Expected-Parrot-examples-b457490b-fc5d-45e1-82a5-a66e1738a4b9/notebook/Tutorial%20-%20Starter%20Tutorial-e080f5883d764931960d3920782baf34>`_.


Conducting an AI-powered survey
-------------------------------
In the steps below we show how to create and run a simple question in EDSL. 
Then we show how to design a more complex survey with AI agents and different language models.
The steps are as follows:

The following steps outline how to use EDSL to develop and execute surveys:

1. **Creating and running a basic question**
We show how to create and execute a question in EDSL:

    - Import a question type (multiple choice, free text, etc.).
    - Construct a question in the question type template.
    - Run the question (using the default language model).
    - Inspect the dataset of results.

2. **Designing a complex survey**
We show how to construct a more complex survey involving AI agents and different language models:

    - Import question types and other survey components.
    - Construct questions in the relevant templates.
    - Use parameters to create versions of the questions with different inputs.
    - Combine questions in a survey.
    - Create personas for AI agents that will answer the questions.
    - Select language models.
    - Run the survey with the agents and models.
    - Explore built-in methods for analyzing results.


A Basic Question
~~~~~~~~~~~~~~~~
Here we create a simple multiple choice question, administer it (to the default language model) and examine the response:

.. code-block:: python 

    # Import a question type
    from edsl.questions import QuestionMultipleChoice
    
    # Construct a question in the question type template
    q = QuestionMultipleChoice(
        question_name = "example_question",
        question_text = "How do you feel today?",
        question_options = ["Bad", "OK", "Good"]
    )
    
    # Run it with the default language model
    results = q.run()
    
    # Inspect the results
    results.select("example_question").print()


Output:

.. code-block:: text

    ┏━━━━━━━━━━━━━━━━━━━┓
    ┃ answer            ┃
    ┃ .example_question ┃
    ┡━━━━━━━━━━━━━━━━━━━┩
    │ Good              │
    └───────────────────┘


Note: The default language model is currently GPT 4; you will need an API key for OpenAI to use this model and run this example.
(See instructions on storing your :ref:`api_keys`.)

In the next example we show how to use different models to generate responses.


A Survey with Agents and Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In this next example we create a survey of multiple questions and personas for AI agents that we prompt language models to use in generating answers the questions.
We also show how to parameterize questions in order to create different versions of the questions that can be administered at once.
This is useful for comparing responses for different data, and conducting data labeling tasks.
We also compare results for different language models.

To see examples of all question types, run `Question.available()`.
To see all available models, run `Model.available()`.

.. code-block:: python

    # Import question types and survey components
    from edsl.questions import QuestionLinearScale, QuestionFreeText
    from edsl import Scenario, Survey, Agent, Model

    # Construct questions
    q1 = QuestionLinearScale(
        question_name = "enjoy",
        question_text = "On a scale from 1 to 5, how much do you enjoy {{ activity }}?",
        question_options = [1,2,3,4,5],
        option_labels = {1:"Not at all", 5:"Very much"}
    )

    q2 = QuestionFreeText(
        question_name = "recent",
        question_text = "Describe the most recent time you were {{ activity }}."
    )

    # Add data to questions using scenarios
    activities = ["exercising", "reading", "cooking"]
    scenarios = [Scenario({"activity": a}) for a in activities]

    # Combine questions in a survey
    survey = Survey(questions = [q1, q2])

    # Create personas for AI agents to use with the survey
    personas = ["athlete", "student", "chef"]
    agents = [Agent(traits = {"persona": p}) for p in personas]

    # Select language models
    models = [Model(m) for m in ["gpt-4o", "claude-3-5-sonnet-20240620"]]

    # Run the survey with the scenarios, agents and models
    results = survey.by(scenarios).by(agents).by(models).run()

    # Filter, sort, select and print components of the results to inspect
    (results
    .filter("activity == 'reading' and persona == 'chef'")
    .sort_by("model")
    .select("model", "activity", "persona", "answer.*")
    .print(format="rich",
            pretty_labels = ({"model.model":"Model",
                            "scenario.activity":"Activity",
                            "agent.persona":"Agent persona",
                            "answer.enjoy":"Enjoy",
                            "answer.recent":"Recent"})
        )
    )


Output:

.. code-block:: text

    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Model                      ┃ Activity ┃ Agent persona ┃ Enjoy ┃ Recent                                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ claude-3-5-sonnet-20240620 │ reading  │ chef          │ 4     │ As a chef, I recently found myself engrossed in │
    │                            │          │               │       │ a new cookbook featuring innovative             │
    │                            │          │               │       │ Mediterranean cuisine. I was curled up in my    │
    │                            │          │               │       │ favorite armchair, poring over vibrant photos   │
    │                            │          │               │       │ of colorful dishes and studying intricate       │
    │                            │          │               │       │ flavor combinations. The pages were filled with │
    │                            │          │               │       │ enticing recipes that sparked my culinary       │
    │                            │          │               │       │ imagination. I took notes on interesting        │
    │                            │          │               │       │ techniques and ingredient pairings, eager to    │
    │                            │          │               │       │ incorporate these fresh ideas into my own       │
    │                            │          │               │       │ cooking. Reading cookbooks is not just a        │
    │                            │          │               │       │ pastime for me; it's an essential part of my    │
    │                            │          │               │       │ professional development and a source of        │
    │                            │          │               │       │ endless inspiration in the kitchen.             │
    ├────────────────────────────┼──────────┼───────────────┼───────┼─────────────────────────────────────────────────┤
    │ gpt-4o                     │ reading  │ chef          │ 4     │ The most recent time I was reading, I was       │
    │                            │          │               │       │ flipping through a cookbook that focused on     │
    │                            │          │               │       │ Mediterranean cuisine. I was particularly       │
    │                            │          │               │       │ interested in a recipe for a traditional Greek  │
    │                            │          │               │       │ moussaka. The book had beautiful photographs    │
    │                            │          │               │       │ and detailed instructions, which really helped  │
    │                            │          │               │       │ me visualize the steps. I made some notes on    │
    │                            │          │               │       │ how I could add my own twist to the dish,       │
    │                            │          │               │       │ perhaps by incorporating some locally sourced   │
    │                            │          │               │       │ ingredients.                                    │
    └────────────────────────────┴──────────┴───────────────┴───────┴─────────────────────────────────────────────────┘

You can also view results in an `interactive notebook <https://deepnote.com/workspace/expected-parrot-c2fa2435-01e3-451d-ba12-9c36b3b87ad9/project/Expected-Parrot-examples-b457490b-fc5d-45e1-82a5-a66e1738a4b9/notebook/Tutorial%20-%20Starter%20Tutorial-e080f5883d764931960d3920782baf34>`_.


Exploring Your Results
~~~~~~~~~~~~~~~~~~~~~~
EDSL comes with built-in methods for analyzing and visualizing your results. 
For example, you can access results as a Pandas dataframe:

.. code-block:: python

    # Convert the Results object to a pandas dataframe
    results.to_pandas()


The `columns` method will display a list of all the components of your results, which you can then `select` and `print` to show them:

.. code-block:: python

    results.columns


Output for the results generated above:

.. code-block:: python

    ['agent.agent_instruction',
    'agent.agent_name',
    'agent.persona',
    'answer.enjoy',
    'answer.recent',
    'comment.enjoy_comment',
    'iteration.iteration',
    'model.frequency_penalty',
    'model.logprobs',
    'model.max_tokens',
    'model.model',
    'model.presence_penalty',
    'model.temperature',
    'model.top_logprobs',
    'model.top_p',
    'prompt.enjoy_system_prompt',
    'prompt.enjoy_user_prompt',
    'prompt.recent_system_prompt',
    'prompt.recent_user_prompt',
    'question_options.enjoy_question_options',
    'question_options.recent_question_options',
    'question_text.enjoy_question_text',
    'question_text.recent_question_text',
    'question_type.enjoy_question_type',
    'question_type.recent_question_type',
    'raw_model_response.enjoy_raw_model_response',
    'raw_model_response.recent_raw_model_response',
    'scenario.activity']


The `Results` object also supports SQL-like queries:

.. code-block:: python

    # Execute an SQL-like query on the results
    results.sql("select * from self", shape="wide")

You can view the output and examples of other methods in `interactive notebooks <https://deepnote.com/workspace/expected-parrot-c2fa2435-01e3-451d-ba12-9c36b3b87ad9/project/Expected-Parrot-examples-b457490b-fc5d-45e1-82a5-a66e1738a4b9/notebook/Tutorial%20-%20Starter%20Tutorial-e080f5883d764931960d3920782baf34>`_.



