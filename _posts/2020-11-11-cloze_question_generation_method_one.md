---
title: Cloze questions: method One
tags:
- NLP
- cloze
desc: first try to generate cloze questions
layout: post
---

This is the first try to generate cloze questions.
<!-- more -->

## Method
This is a simple method of generating cloze questions 
(https://github.com/AugustTom/Question-Generator/blob/gh-pages/Code/main_based_keywords.ipynb). <br>
Step 1: Fetch text from Wikipedia 
 - To simplify this step TextFetcher (https://github.com/AugustTom/Question-Generator/blob/gh-pages/Code/text_fetcher.py)
  class was created. It returns Wikipedia article on a given topic. For testing 
 article about 'Oxygen' is used. 
Step 2: Get top keywords used in a text. 
 - To achieve this step TextRank (https://github.com/AugustTom/Question-Generator/blob/gh-pages/Code/text_rank.py) class was implemented. It uses an adapted version of Page Rank 
 (ref: http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf) algorithm to rank keywords and sentences. 
Step 3: Get top sentences in a text. 
 - The same TextRank algorithm was used to get the top sentences. 
Step 4: Iterating through the top sentences, top keywords are replaced by '____'. Original sentence, modified sentences,
 and the keyword are then added to ClozeQuestion class that stores the all of the information about the cloze question. 
Step 5: Print the questions. 
