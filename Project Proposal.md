# Cover

| Created  →  Oct 19, 2025  | Last update  →  Date |
| ----- | :---: |
|  Travel Itinerary Generator   |  |
| **Course:** Natural Language Processing Amar Hajrovic |  |

# Problem Statement and motivation

#### Introduction

Planning a personalized trip is a complex task which in itself involves user preferences, gathering data, querying and aggregating data from multiple sources. With increased capability of NLP and AI agents entering mainstream usage,  automation of task to assist users in a dynamic and personalized way of planning a trip has become possible and promising. The goal of the project is to develop a Travel Itinerary Generator (TIG) which uses recent advancements in NLP and agentic workflows to provide assistance to users in planning customized trips. Motivation is to enhance  task of manual research and composing of itinerary to something more streamlined \-  consuming free form requirements and turning them into structured action plan.

The main techniques that will be applied are: 

* Natural Language Understanding \- process of making sense of unstructured user input. For example: “I am planning a 3 day trip to Italy, Rome. I am interested in sightseeing and culture” , at this point system needs to apply NLU and extract key entities like location, duration, main interests.  
* Agentic workflows  \-  system built around different kind of agents for purpose of performing specific tasks in sequence

#### Problem statement & motivation

Planning a trip is in itself exciting, but at the same time it can be rather daunting and a huge time sink.  When you figure when and where to go then there is more research about activities, POI’sand similar. All that information of interest is usually thrown around several places.  

Services like Booking or TripIt assist user by consolidating bookings and suggestions of main points of interest based on several distinct manual inputs.  At the same time they provide results in a generic way. Usually they do not handle dynamic input well and they cannot adapt to dynamic real time changes related to user intent. 

This project aims to develop a TIG using Natural Language Processing techniques and agentic workflows to generate dynamic and customized itineraries based on understanding of user preferences from natural language. The goal is to deliver an intelligent, interactive and helpfull system for trip planning. 

#### Research question(s)

Some of research questions that arise are: 

* How can NLP input be reliably parsed to extract relevant information from user 

  *Why it is important:*  users express travel preferences on different and non standard ways. And this issue is important to TIG application, because possibility to extract required information from spoken language which structure is organic and unique for each  person is primary. Without that possibility TIG  would not be able to operate and entire process would fail. 

  *Goal:* evaluate and improve on TIG’s usage of NLP techniques to accurately extract structured information from spoken language. 

* What kind of feedback can be easily captured from the user to refine existing itinerary and will it affect the flow of the process. Can it be incorporated without disrupting the process.

  *Why it is important:* Travel planning is interactive process which can become iterative (user after initial results sees a need to refine some part of his query for different hotel, change dates or interests for a trip).  Standard systems cannot accommodate the dynamic of human expression and usually require a new process of planning from the start.  Understanding how to process additional feedback while maintaining context and coherence  makes a difference between static system and truly personalized travel planning. 

  *Goal:* Implement interactive feedback mechanism which will allow users to change and refine initial queries

* What is effective way to evaluate if generated itinerary is valid and matches user intent

  *Why it is important:*   if we take into account process of understanding spoken or written language, extraction of information from that language proper evaluation metrics is important in establishing baseline  accuracy because it would be impossible to measure that performance or compare it to existing information.

  *Goal:* establish multilevel comparison against existing dataset, all for the purpose of reaching a level where we have comparable or better performance than standard approaches. 

#### Data set(s)

We plan to use [osunlp/TravelPlanner · Datasets at Hugging Face](https://huggingface.co/datasets/osunlp/TravelPlanner) as benchmark to compare output from my system to data provided by osunlp. All LLMs are trained with actual data to fixed point in time, they essentially operate in closed information space. To overcome this constraint at some point of TIG workflow there is possibility of including real world api’s for collecting additional information (flight data, local events,  restaurant ratings and similar)

