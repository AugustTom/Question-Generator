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

##Stopword removal

In language such as english there is a lot of words that do not carry a meaning (such as the, a ...). Removing these words
from the text, allows the focus to be on the context words. There is two usual methods for this task - using pre-made
stopword set or creating your own. In this case, Spacy's pre-established one will be used.

## Stemming

Stemming is a process of removing inflected words to their base form. The idea is that removing end of the word allows
to compare words that have the same stem (like if you are looking for classess if also gives you results for class).

Example:
    Classes -> class
    Fishing -> fish

## Lemmatization
Similary to stemming but instead of cutting down word to a stem, if uses knowledge (such as WordNet) to change the word
to base. In this case, the words that have a different base (like better and good) still gets simplified to the same word.
Example:
    better -> good
    running -> run

## Normalization

Normalization is another popular practice. I focuses on transforming text into standard version. It is normally used
 when working with non-formal text such as social media posts. It changes the abbreviations such btw to by the way.
 It is an important practice, however, it will not be used as this project will focus on formal texts where abbreviations
 should be encountered.

 