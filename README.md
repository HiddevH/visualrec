---
title: "Flask App for Facial Recognition"
output: html_document
---

## Connect to VM's 
Replace user@ with your google cloud account name. 
gcloud compute --project "feisty-beacon-215611" ssh --zone "europe-west4-a" "mauricerichard91@face-cog-2" -- -R 52698:localhost:52698
gcloud compute --project "feisty-beacon-215611" ssh --zone "europe-west2-c" "mauricerichard91@face-cog-gunicorn" -- -R 52698:localhost:52698

## To do list

* Allow someone to upload a picture and the go to the browse page to select the casts. The image preferably isn't stored but kept in memory. Need links on browse buttons to pictures.



#### Input

Name | Description
------------------ | -------------------------------------------------
test | test


## Acknowledgments


