# sunshine
Get an AI-generated analysis of legislation

## Project Goals

1. Automatically pull up-to-date information about legislative activity.
1. Analyze the data gathered to create a concise, human-friendly summary of the main focus of the activity.
1. Analyze the data gathered to find ammendments, riders, "pork," and other inclusions added to the main bill. Present those as a list.
1. Analyze the data gathered to find who might benefit from the legislative activity. 
1. Analyze the data gathered to find who might be harmed by the legislative activity.

## Technical Goals

1. Create an extensible structure to hold and describe all this information. Maybe use JSON? Is there a better format?
1. We should probably build local storage for this so that we can have an extremely fast user interface. How do we approach this? Is this a database, RAG, something else?
1. Implement excellent (accurate; fast) search for the UI. 

## Roadmap

1. Build script to access the congress.gov API and test data pulls.
1. Test summarizing / enriching the data via LLM.
    1. Local LLM vs online
    1. Implement method of finding related data. Labels?
    1. Just give the whole chunk of data to the LLM, or is there cleaning that will help the analysis?
1. Review available data, consider DB storage options.
1. Create test web-based front-end to present data. This will probably benefit from really well-implemented search functionality.
1. Identify other APIs that could be useful in this endeavor.
    1. Opensecrets
    1. Propublica
