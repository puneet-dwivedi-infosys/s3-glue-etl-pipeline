# s3-glue-pipeline


S3 (File Uploaded)
   │
   └──> SQS Queue
         │
         └──> Lambda (Check status, config, run Glue)
                     │
                     └──> Glue Job (ETL)
                                │
         ┌──────────────────────┴──────────────────────┐
         v                                             v
   EventBridge (SUCCEEDED)                      EventBridge (FAILED)
         │                                             │
         v                                             v
  Lambda (Crawler + Athena)                   Lambda (Send Alert)