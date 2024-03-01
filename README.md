# Excelus_agents

This repository is designed to contain the production Micro-service  AI Agents for ExcelusAI team (now made opensource).

Current Implementation architecture involves a REST-API service in **Fast-API**, **langchain** based agent using **gpt-4** open-ai model, **redis** cache database for Agents memory, **text embedding tool** and a **custom tool** implementation using OpenAi functions.

The `medical_reception agent` is a demonstration intended to serve at a hospital/clinic desk, to respond to user enquiries on doctors and treatment packages avaailable at the facility and also make a booking appointment via the agent.

Feel free to add new agents to this repository.
NOTE - Each agent should be independent as a separate micro-service.
