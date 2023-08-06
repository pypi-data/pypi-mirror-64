# ud_spacy_model
spaCy model Based on UD representation.

We provide three models, based on the original en_core_web_sm/md/lg models (v2.2.5).
Actually, when we say based on, we mean, that we trained a different tagger and parser, but kept the NER component.
All three models could be found in PyPI under the names: en_ud_model_sm/md/lg

The data for training was merged from the following corpora:
	(a) UD_English-EWT-r1.4
	(b) penn treebank v2 (LDC95T7) that was converted to UD format:
			(i) standard split to train (02-21) dev (22) and test (23) (discarding 00/01/24)
			(ii) using CoreNLP v3.5.2 (https://nlp.stanford.edu/software/stanford-dependencies.shtml) to convert:
				java -cp "*" -mx1g edu.stanford.nlp.trees.ud.UniversalDependenciesConverter -treeFile train-tmp.mrg > train-penn.conllu
			(iii) Changed all -LCB- and -RCB- that appeared in the form and lemma columns to '{' and '}' respectily (as it is in the EWT corpus).

The training process was preformed as follow:
	using spaCy's CLI, 
	path_to_training_dir\> python -m spacy convert treebank/combined/combined_train.conllu combined_converted -n 10
	path_to_training_dir\> python -m spacy convert treebank/combined/combined_dev.conllu combined_converted -n 10
	path_to_training_dir\> mkdir models
	path_to_training_dir\> python -m spacy train en models combined_converted/combined_train.json combined_converted/combined_dev.json -b en_core_web_sm/md/lg -R -p tagger,parser

Model adjusments:
	After training we fixed the following meta.json fields: name, license, author, url, email, description, sources, version. 
	Since we have changed the name of the model in the meta.json, we also needed to fix the names of the "vectors_name" and "pretrained_vectors" to be en_ud_model_sm/md/lg under MODEL_PATH/ner/cfg , MODEL_PATH/tagger/cfg and MODEL_PATH/parser/cfg.
