📂 Project Structure

app/
│── main.py                     
│
├── engine/
│   ├── graph.py                
│   ├── models.py              
│   ├── registry.py            
│   └── store.py                
│
└── workflows/
    └── summarization.py

## git repo:- "https://github.com/Saketbishnu/EngineWorkflow.git" 

##graph/expample/summarization :-

## graph id : "graph_id": "68c3b6f9-2730-41a9-97a5-35a39a3fa82b"

## step 2 : POST /graph/run : - "run_id": "6a3b5cc8-0284-45dd-afaf-5bad70e27db4"

## step 3: GET /graph/state/{run_id} paste run id :- 6a3b5cc8-0284-45dd-afaf-5bad70e27db4

## output : response body : -
{
  "run_id": "6a3b5cc8-0284-45dd-afaf-5bad70e27db4",
  "final_state": {
    "additionalProp1": {},
    "chunks": [],
    "summaries": [],
    "merged_summary": "",
    "final_summary": "",
    "summary_length": 0,
    "keep_looping": "no"
  },
  "log": [
    {
      "node_id": "split",
      "state_before": {
        "additionalProp1": {}
      },
      "state_after": {
        "additionalProp1": {},
        "chunks": []
      },
      "status": "ok"
    },
    {
      "node_id": "summarize",
      "state_before": {
        "additionalProp1": {},
        "chunks": []
      },
      "state_after": {
        "additionalProp1": {},
        "chunks": [],
        "summaries": []
      },
      "status": "ok"
    },
    {
      "node_id": "merge",
      "state_before": {
        "additionalProp1": {},
        "chunks": [],
        "summaries": []
      },
      "state_after": {
        "additionalProp1": {},
        "chunks": [],
        "summaries": [],
        "merged_summary": ""
      },
      "status": "ok"
    },
    {
      "node_id": "refine",
      "state_before": {
        "additionalProp1": {},
        "chunks": [],
        "summaries": [],
        "merged_summary": ""
      },
      "state_after": {
        "additionalProp1": {},
        "chunks": [],
        "summaries": [],
        "merged_summary": "",
        "final_summary": "",
        "summary_length": 0,
        "keep_looping": "no"
      },
      "status": "ok"
    }
  ]
}
