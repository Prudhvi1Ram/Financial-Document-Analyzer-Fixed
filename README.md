
<h1>Bugs i found after extracting</h1>

   1) There was problem with dependencies all are clashing with crewai, so i had to modify others by changing versions of them and deleting which are not required.\n
   2) Next thing is the descriptions for the agents(They are so funny that i laughed for like 2-5 minutes just by reading them) yeah, keeping this aside the descriptions were bad, they were written in such a way     that model will be so overconfident while answering and tends to hallucinate so much, so i changed description for every agent
   3) Next in agents LLM class is not initialized so i imported crewai function and initialized LLM class, and i gave some parameters to the class including model,temparature,api key, max parameters to make it work
   4) There were some librarires that were not imported correctly, so changed them to make it work
   5) There was unnecessary async in main.py so removed it
   6) And when we were importing content from another files, there were some naming mistakes in file names
   7) i changed the parameters of agents in agents.py like increase the max iterations to 3 to make it think more and get best outcomes
   8) And in tools.py reading pdf some lines had unnecessary increased time complexity, so wrote some optimal lines there
   9) removed some tool validation errors
   10) Removed circuar import issues

<h1>Setup And Usage Instructions</h1>
  1) I have downloaded the project from document and extracted in my local computer
      
  2)I then created virtual environment and installed all the requirements
    
  3)and an .env file for my APi keys, and Mongo Db url(cloud)
    
  4)Finally run the server using unicorn


<h1>API Documentation</h1>
  Base Url:http://127.0.0.1:8000
  Swagger UI:http://127.0.0.1:8000/docs
  

 <h2> Work Flow: CREATE USER(/create-user) **->** UPLOAD PDF(\analyze) **->** GET JOB_ID **->** FETCH RESULT(/result/job_id)</h2>


  
                    
   _1)  Health Check_:
   
                  1) GET: {
                           "message": "Financial Document Analyzer API is running"
                           }
  _2) Create user (POST)_
  
                    1) POST/create_user:
                     2) Parameters:User_id,email
                     3) Output:
                     {
                    "message": "User created successfully",
                   "user_id": "f6a84225-2f0b-44cd-a47e-200d7dbd2ffc"
                     }

  _3) analyze(POST)_
  
            1)  Parameters: Userid,File,Query
             2) Output:
             {
                 "message": "Analysis completed",
                "job_id": "8f91b8e4-56f2-4c9e-b1ab-74b7cfc0a12e"
               }

  _4)  Get analysis Report(GET)_
  
                 1) Parameters:Job_id
                 2) Output:
                 {
                     "job_id": "8f91b8e4-56f2-4c9e-b1ab-74b7cfc0a12e",
                      "user_id": "f6a84225-2f0b-44cd-a47e-200d7dbd2ffc",
                        "file_name": "tesla_q2.pdf",
                         "query": "Analyze this financial document for investment insights",
                           "status": "completed",
                            "analysis": "Full AI-generated analysis text...",
                           "created_at": "2026-02-27T09:14:23",
                           "completed_at": "2026-02-27T09:14:40"
                         }

 **Bonus:**
   I have used MongoDB(Cloud Database) To store the user details






                  

  

  
