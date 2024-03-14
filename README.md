# Eating Disorder Reddit Data (Pre and Post Covid Pandemic)

## Introduction
The dataset comprises Reddit data pertaining to eating disorders during the COVID-19 pandemic. We gathered information from three prominent subreddits focused on eating disorders, namely r/EatingDisorders, r/AnorexiaNervosa, and r/BingeEatingDisorder.

## Overview
We have collected the dataset for a 4 years long duration for each of the subreddit. The two years(1st March 2018 to 29th Feb 2020) dataset before the covid pandemic declaration is considered as pre-pandemic data and two years(1st March 2020 to 28th Feb 2022) dataset after the covid pandemic declaration as post-pandemic data. The folder Pre_Covid_Data and Post_Covid_Pandemic contain pre-pandemic and post-pandemic data respectively.

## Contents
- `Pre_Covid_Data`: Contains dataset of three subreddits of pre-pandemic.
- `Post_Covid_Data`:Contains dataset of three subreddits of post-pandemic.
- `README.md`: Description of the dataset.

## Format 
The data is provided in CSV format. Each subreddit data has been separated into submission and comment. Each row of submission file is a submission or post whereas each row of comment file is the comment of that submission. 

The submission file has the following fields:

- `id` : id is a unique id for each of the submission.
- `title` : title is the headline for each submission.
- `selftext` : selftext is the body text of the submission.
- `created_utc` : created_utc is the time when the submission is submitted to the reddit.
- `normal_time` : generated normal time from created_utc field.
- `url` : url for the submission.
- `comment_number` : number of comments of that submission.
- `author` : author of that submission.

For comment file, each file contains comment corresponds to the submission. We link the submission and comment with submission unique id. Each comment has 4 fields. These are:

- `id` : The first column is the submission unique id with which we link submission and comment.
  
After the first column, each four coulmns are the comment fields.

- `Column 2` : author id to see which author commenting to the submission.
- `Column 3` : comment text.
- `Column 4` : utc time. The time when the comment is submitted to the reddit.
- `Column 5` : normal time generated or converted from utc time.


## Usage
This dataset can be used to analyse the impact of covid pandemic on eating disorder community. These data also contain information about mental health. So, researchs are allowed to use and ispect the data contains and extract insightful information.

