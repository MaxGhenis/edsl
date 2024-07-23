.. _remote_inference:

Remote Inference
=================

Remote inference allows you to run EDSL jobs on the Expected Parrot server instead of your local machine.


Requirements
------------

1. `Create a Coop account <https://www.expectedparrot.com/login>`_.

2. Store your **Expected Parrot API key** in a *.env* file. See :ref:`coop` for more detailed instructions.


Activating remote inference
---------------------------

1. `Log in <https://www.expectedparrot.com/login>`_ to Coop and navigate to the `Coop API <https://www.expectedparrot.com/home/api>`_ page:

.. image:: static/coop_api_main_page.png
  :alt: Coop API page link at the main page
  :align: center
  :width: 600px

.. raw:: html
  
    <br>

2. Locate **EDSL Settings** section of the page.

2. Toggle the slider for *Remote inference* to turn it on:

.. image:: static/remote_inference_toggle_coop_api_page.png
  :alt: Remote inference toggle on the Coop web app
  :align: center
  :width: 600px

.. raw:: html

    <br>

When remote inference is on, jobs will be run on the Expected Parrot server instead of your local machine.


Using remote inference
----------------------

We can use remote inference by passing a `remote_inference_description` string to the `run` method of a survey.


Example
^^^^^^^

The steps below show how remote inference works. 
We start by creating an example survey:

.. code-block:: python

  from edsl import Survey
  from edsl.questions import QuestionMultipleChoice

  q1 = QuestionMultipleChoice.example()

  survey = Survey(questions=[q1])


Cost
^^^^

Running jobs on the Expected Parrot server requires seed. 
The current exchange rate is 1 seed = $0.01 USD.

We can estimate the cost of running a survey by passing it in the `remote_inference_cost` method:

.. code-block:: python

  from edsl import Coop

  coop = Coop()

  coop.remote_inference_cost(survey)


Output:

.. code-block:: python

  2   # This job costs 2 seed


You can purchase more seed at the `Purchases page <https://www.expectedparrot.com/home/purchases>`_.


Running a job
^^^^^^^^^^^^^

Next we run the survey, passing a `remote_inference_description` string to the `run` method:

.. code-block:: python

  survey.run(remote_inference_description="Example survey", verbose=True)


Output (actual details will be unique to your job):

.. code-block:: python

  "Remote inference activated. Sending job to server..."
  "Job sent!"

  # Some details about the job
  {
      "uuid": "2dd892a5-dc3d-4f82-ba8c-9aa9ef6b5391",
      "description": "Example survey",
      "status": "queued",
      "visibility": "unlisted",
      "version": "0.1.29.dev4",
  }


The job will appear at your `Remote Inference page <https://www.expectedparrot.com/home/remote-inference>`_ with a status of "Queued":

.. image:: static/coop_remote_inference_jobs_queued.png
  :alt: Remote inference page on the Coop web app. There is one job shown, and it has a status of "Queued."
  :align: center
  :width: 650px

.. raw:: html

  <br>


There are 6 status indicators for a job:

#. **Queued**: Your job has been added to the queue. 
#. **Running**: Your job has started running.
#. **Completed**: Your job has finished running successfully. 
#. **Failed**: Your job threw an error.
#. **Cancelling**: You have sent a cancellation request by pressing the **Cancel** button.
#. **Cancelled**: Your cancellation request has been processed. Your job will no longer run. 


Viewing the results
^^^^^^^^^^^^^^^^^^^

Once your job has finished, it will appear at the `Remote Inference page <https://www.expectedparrot.com/home/remote-inference>`_ with a status of "Completed"

.. image:: static/coop_remote_inference_jobs_completed.png
  :alt: Remote inference page on the Coop web app. There is one job shown, and it has a status of "Completed."
  :align: center
  :width: 650px

.. raw:: html

  <br>


You can now click on the **View** link to access the results of your job.
Your results are provided as an EDSL object for you to view, pull, and share with others. 

You can also access the results URL from EDSL by calling `coop.remote_cache_get()` 
and passing the UUID assigned when the job was run:

.. code-block:: python

  from edsl import Coop

  coop = Coop()

  coop.remote_cache_get("2dd892a5-dc3d-4f82-ba8c-9aa9ef6b5391")


Output:

.. code-block:: python

  {
    "jobs_uuid": "2dd892a5-dc3d-4f82-ba8c-9aa9ef6b5391",
    "results_uuid": "4442372d-6bc7-4c88-a4b9-da0fbec1de14",
    "results_url": "https://www.expectedparrot.com/content/4442372d-6bc7-4c88-a4b9-da0fbec1de14",
    "status": "completed",
    "reason": None,
    "price": 2,
    "version": "0.1.29.dev4",
  }


Job history
-----------

You can click on any job to view its history. When a job fails, the job history logs
will describe the error that caused the failure:

.. image:: static/coop_remote_inference_history_failed.png
  :alt: A screenshot of job history logs on the Coop web app. The job has failed due to insufficient funds.
  :align: center
  :width: 350px

.. raw:: html

  <br>


Job history can also provide important information about cancellation. When you cancel a job, one of two things must be true:

1. **The job hasn't started running yet.** No seed will be deducted from your balance.
2. **The job has started running.** Seed will be deducted.

When a late cancellation has occurred, the seed deduction will be reflected in your job history.

.. image:: static/coop_remote_inference_history_cancelled.png
  :alt: A screenshot of job history logs on the Coop web app. The job has been cancelled late, and 2 seed have been deducted from the user's balance.
  :align: center
  :width: 300px

.. raw:: html

  <br>


Using remote inference with remote caching
------------------------------------------

When remote caching and remote inference are both turned on, your remote jobs will use your remote cache entries when applicable.

.. image:: static/coop_toggle_remote_cache_and_inference.png
  :alt: Remote cache and remote inference toggles on the Coop web app
  :align: center
  :width: 300px

.. raw:: html

  <br>


Let's rerun the survey from earlier:

.. code-block:: python

  survey.run(remote_inference_description="Example survey rerun", verbose=True)


After running this survey, you will have a new entry in the remote cache.
This is reflected in your remote cache logs:

.. image:: static/coop_remote_inference_cache_logs.png
  :alt: Remote cache logs on the Coop web app. There is one log that reads, "Add 1 new cache entry from remote inference job."
  :align: center
  :width: 650px

.. raw:: html

  <br>


If the remote cache has been used for a particular job, the details will also show up in job history:

.. image:: static/coop_remote_inference_history_cache.png
  :alt: An entry in the job history log on the Coop web app. It shows that 1 new entry was added to the remote cache during this job.
  :align: center
  :width: 300px

.. raw:: html

  <br>


Remote inference methods
------------------------

The following methods allow you to work with remote jobs manually:


Coop class
^^^^^^^^^^

.. autoclass:: edsl.coop.coop.Coop
  :members: remote_inference_create, remote_inference_get, remote_inference_cost
  :undoc-members:
  :show-inheritance:
  :special-members:
  :exclude-members: 
