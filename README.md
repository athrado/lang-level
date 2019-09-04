# Language Level Analysis and Classification for German

*lang-level* is a tool for identifying and analyzing linguistic constructions and characteristics that allow inference about the writer’s language skills. Experiments with a linear support vector classifier trained on these features demonstrate that this approach is fit for assigning language levels to unseen texts. This system clearly outperforms the baseline and reaches an accuracy of 89%. Feature agglomeration raises the performance to 96% accuracy. The features also proved suitable for author classification on literary works.

# ## Requirements

The system is implemented in Python 3.7 and tested under Ubuntu Linux, but it should work under other environments which have Python installed (no guarantee).

If you want to use the embedded parser functions, please install ParZu and CorZu.

- [ParZu](https://github.com/rsennrich/ParZu)
- [CorZu](https://github.com/dtuggener/CorZu)

Alternatively, you can use another dependency parser for German with CoNLL output format and enter its parsing output instead of raw text.  If you do not wish to incorporate CorZu, simply disable the entity features.



