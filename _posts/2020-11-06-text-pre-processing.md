---
title: Text Pre-processing
tags:
- NLP
- text
- pre-processing
desc: text pre-processing methodologies
layout: post
---

During this week, I dived into text pre-processing methodologies. Looking into how they can be applied to this project.
<!-- more -->

Text pre-processing is a vital step in any NLP application. As this project aims to transform unstructed data to
something computer can 'understand' (and then back into natural language), in this part I will look into different ways
of pre-processing natural language text and if can be applied to this project.

## Lowercasing

Lowercasing is one of the simplest approaches to pre-processing. It involves transforming all letters to lowercase.

For example:
    PLants -> plants
    COLORADO -> colorado
    Oxygen -> oxygen

In some cases lowercasing can not be applied. One of such examples is comparing different programming languages (Python
and Java), where lowercasing them both would make almost unidentifiable.

## Stemming

Stemming is a process of removing inflected words to their base form. The idea is that removing end of the word allows
to compare words that have the same stem (like if you are looking for classess if also gives you results for class).

Example:
    Classes -> class
    Fishing -> fish

## Lemmatization
Similary to stemming but instead of cutting down word to a stem, if uses knowledge (such as WordNet) to change the word
to base. In this case, the words that have a different base (like better and good) still gets simplified to the same word.


