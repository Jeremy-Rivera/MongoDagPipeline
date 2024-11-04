# Building a Simple Python Data Pipeline with MongoDB and Dagster

## Try it Yourself

- **GitHub Repository**: [MongoDagPipeline](https://github.com/Jeremy-Rivera/MongoDagPipeline)
- **Video Tutorial**: [Watch Here](https://youtu.be/YeSOVcBVid8)  
  _(Note: The video has a previous working version based on older Dagster syntax, this repository has an updated version)_

## Overview

With the increasing importance of AI and data, creating scalable data pipelines and orchestrating data flows is essential. In this project, we use **MongoDB** as our database and **Dagster** as a data orchestration tool to build a simple, robust Python data pipeline.

## What is Dagster?

Dagster is an orchestrator for data pipelines, designed to simplify workflow management, monitoring, and handling of data assets like datasets, machine learning models, and more. By integrating Dagster with MongoDB, we can build an efficient and flexible data pipeline.

## Setting Up the Environment

### Step 1: Create Your Project Structure

Begin by creating a `persons.json` file that holds the data you want to import into MongoDB, and place it in your project directory (`MongoDBPipeline`).

### Step 2: Start MongoDB

Ensure MongoDB is running on your local machine. You can start it by running `mongod` in a terminal window.

### Step 3: Set Up Your Python Environment

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
3. **Install Required Packages**:
   ```bash
   pip install dagster pymongo pydantic pydantic-settings
   ```

These dependencies will set up Dagster, enable connection to MongoDB, and validate configurations using Pydantic.

## Writing the Code

The current repository has updated changes due to feedback received by the Developer Relations team @Dagster

### Key Changes from Previous Code

1. **Dagster `asset` and `Definitions` API**:

   - The `@op` decorator has been replaced with the `@asset` decorator, which is recommended for data assets in Dagster.
   - Instead of using `@job`, we now use `Definitions` to define and bundle assets and resources, allowing a more modular setup.

2. **`__ASSET_JOB` Execution**:
   - Dagster auto-generates a job called `__ASSET_JOB` for all assets. We access it using `defs.get_job_def("__ASSET_JOB")` and then run it with `execute_in_process`.
   - This ensures all assets are executed within the specified context.

## Running the Application

To run the pipeline and insert data into MongoDB, use the following command:

```bash
python persons.py
```

Upon running the script, you should see logs confirming the data has been successfully inserted into MongoDB. To verify, open **MongoDB Compass** and check that the `persons` collection has been populated with the data from `persons.json`.
