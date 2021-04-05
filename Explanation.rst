============
Explanation
============


.. contents:: Explanation table of contents
	:local:

NLP functions
-------------
The heart of the project are the words_in_set, matched_entries and best_match functions. They provide the natural language processing of the data, matching words and giving the match a score.

words_in_set
************
At the baseline, the words_in_set function takes a list_of_words and a sset. For each word, it checks if that word is in the set and, if succesfull, it raises the score by one and counts a match found.

Now the list_of_words could contain one or more descriptive words, wich appears in many set, even in ones that are uncorrelated. We can not discard them, but we have to take into account this phenomena.
Take for example ['abdominal', 'pain']: discarding the word 'pain' would result in a possible correlation with an ipotetical 'abdominal fat deposits' entry, wich would be wrong. At the same time, taking into account every possible 'pain' correlation could give birth to strange couples like 'abdominal pain'->'fingers pain', wich is also wrong.
For these reasons, when we have a list_of_words composed by two ore more words, every single word match is saved with a negative score. In this way we can preserve the matching score result (as absolute value) but we penalize it in further computations as, beeing negative, it's smaller then other scores.

We also have to address the word stemming: when 'stemmed', a word could be changed either losing a piece or beeing modified. In this way when checking inside the set with the 'in' statement, we will never find any corrispondence as the set's words are not stemmed.
Therefore we need to check for the stemmed word, not in the set, but in every word of the set, as the stemming process is built to preserve the root of the word and we aim to match that.

matched_entries
***************
We now step up a level, the matched_entries function manages the dict_of_sets taken in input, passing one set at a time to the words_in_set function.
When the words_in_set function returns a score, if it's not zero, wich means that at least one match has been found, the matched_entries function adds to the dictionary it's building, the name of the matched set, as the key, together with its score.

We have seen that single word matches are problematic, but what to do when the set we are looking at has only one word?
That's why we can enable checking for 'mono' word sets. In these cases, when there's a match the score will be negative. Checking for that and for the set to contain only one word, will let us set the score to an arbitrary '1', therefore recovering the match for further computations.

best_match
**********
Lastly, the best_match function checks all the matched_entries picking the best one(s).
Iterating over the obtained dictionary, the function initially saves the first positive non-zero score entry that it founds, then updates it whenever a higher score appears.
Allowing for multiple best matches, every time a score equal to the best one is found, the entry is appended to the best_list. The first best_entry found is appended last to dodge possible swapping mistakes.


Stargare uses NLP funcions
---------------------------
how it does that
why it does that

Stargate also uses databases!
-----------------------------
you see, here it uses SNAP
why it does it this way (loading data)
and why only "one way" (start to end links)

You said databases! wich ones?
------------------------------
database classes
why they are all different
why they are formatted the way they are

Some management functions
-------------------------
here

The main function
-----------------
end
