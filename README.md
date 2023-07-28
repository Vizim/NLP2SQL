# NLP2SQL
This is a project I made as a proof of concept that proves that it's very much possible to use natural language processing AI to generate various SQL codes to test the quality of data in a large-scale database. This project was also done over the course of 2 months and is still in its very early stages...

# Example Outs

| Input Prompts:                                                                                                               	| Normalized Input                                                                                                             	| Output SQL Code:                                                                                                                                                                               	|
|------------------------------------------------------------------------------------------------------------------------------	|------------------------------------------------------------------------------------------------------------------------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| 1. Check if the date   is in the future:                                                                                     	| Check if the   date is in the future:                                                                                        	| SELECT   CASE          WHEN Birthday > CURRENT_DATE   THEN -10          ELSE 0      END as check_future FROM your_table;      ```                                                              	|
| 2. The birthday year should be within the   range of 1900 to 9999 to be stored in a SQL database.                            	| 2. The birthday year should be within the   range of 1900 to 9999 to be stored in a SQL database.                            	| SELECT   CASE WHEN birthday_year >= 1900 AND birthday_year <= 9999 THEN 0 ELSE 1   END AS year_check      FROM table_name;                                                                     	|
| 3. The birthday must not be a future date   to be stored in a SQL database.                                                  	| 3. The birthday must not be a future date   to be stored in a SQL database.                                                  	| SELECT   CASE WHEN birthday <= CURRENT_DATE THEN 0 ELSE 1 END AS   birthday_check      FROM table_name;                                                                                        	|
| 4. The birthday should not be an invalid   date, such as February 30th or April 31st, to be stored in a SQL database.        	| 4. The birthday should not be an invalid   date, such as February 30th or April 31st, to be stored in a SQL database.        	| SELECT   CASE WHEN ISDATE(birthday) = 1 THEN 0 ELSE 1 END AS date_check      FROM table_name;                                                                                                  	|
| 5. The birthday must be a valid date that   can be converted to a date data type in SQL to be stored in a SQL database.      	| 5. The birthday must be a valid date that   can be converted to a date data type in SQL to be stored in a SQL database.      	| SELECT   CASE WHEN TRY_CONVERT(date, birthday) IS NOT NULL THEN 0 ELSE 1 END AS   date_check      FROM table_name;                                                                             	|
| 6. The birthday must be a date that is   supported by the specific SQL database being used.                                  	| 6. The birthday must be a date that is   supported by the specific SQL database being used.                                  	| INSERT   INTO users(birthday) VALUES(946684800);                                                                                                                                               	|
| 7. The birthday should not be earlier   than the earliest possible date that can be stored in the SQL database being   used. 	| 7. The birthday should not be earlier   than the earliest possible date that can be stored in the SQL database being   used. 	| SELECT   CASE WHEN birthday >= '1900-01-01' THEN 0 ELSE 1 END AS   birthday_check      FROM table_name;                                                                                        	|
| 8. The birthday should not be later than   the latest possible date that can be stored in the SQL database being used.       	| 8. The birthday should not be later than   the latest possible date that can be stored in the SQL database being used.       	| SELECT   CASE WHEN birthday <= '9999-12-31' THEN 0 ELSE 1 END AS   birthday_check      FROM table_name;                                                                                        	|
| 9. The birthday must be a complete date   with a year, month, and day to be stored in a SQL database.                        	| 9. The birthday must be a complete date   with a year, month, and day to be stored in a SQL database.                        	| SELECT   CASE WHEN ISDATE(birthday) = 1 AND YEAR(birthday) IS NOT NULL AND   MONTH(birthday) IS NOT NULL AND DAY(birthday) IS NOT NULL THEN 0 ELSE 1 END   AS date_check      FROM table_name; 	|
| 10. The birthday should not be a date   with a time component to be stored as a date data type in a SQL database.            	| 10. The birthday should not be a date   with a time component to be stored as a date data type in a SQL database.            	| SELECT   CASE WHEN CAST(birthday AS TIME) = '00:00:00' THEN 0 ELSE 1 END AS   date_check      FROM table_name;                                                                                 	|
| 11. The birthday should not be a string   or text value to be stored as a date data type in a SQL database.                  	| 11. The birthday should not be a string   or text value to be stored as a date data type in a SQL database.                  	| SELECT   CASE WHEN TRY_CONVERT(date, birthday) IS NOT NULL THEN 0 ELSE 1 END AS   date_check      FROM table_name;                                                                             	|
## Training Data / Tools
 * Glove 6B (Stanford University)
 * W3 Schools SQL Tutorials
 * Google PaLM API
 * Google PaLM pre-trained
## Dependencies: 
* torch:
  - PyTorch is a Python package that provides two high-level features:
Tensor computation (like NumPy) with strong GPU acceleration.
Deep neural networks built on a tape-based autograd system.

* palm-rlhf-pytorch: 
  - Implementation of RLHF (Reinforcement Learning with Human Feedback) on top of the PaLM architecture. Basically ChatGPT but with PaLM

* transformers
  - Provides state-of-the-art general-purpose architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet, CTRL...) for Natural Language Understanding (NLU) and Natural Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between TensorFlow 2.0 and PyTorch.

* tokenizers
  - Tokenization is used in natural language processing to split paragraphs and sentences into smaller units that can be more easily assigned meaning. Tokinzers provides implementations of the most used tokens today.
  
* hidet
  - An open-source efficient deep learning framework/compiler, written in python.

* datasets
   - Online loaders for public data sets
   - Efficient data pre-processing essentially let us chunk the data if it is chunked in memory correctly it makes training faster and supports formats like CSV, JSON, text, png, jpeg, wav, mp3, parquet

* wandb
  - Allows you to store hyper-parameters while using them in your training run. Also allows you to visualize your hyper-parameters a lot better. 
* TensorFlow 2
  - This has so many features but typically tensorflow provides n-dimensional matrix manipulation and data flow graphs. 
* Numpy
  - Tensor computation and a lot of math/stat resources.
* Keras
  - Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow. It was developed with a focus on enabling fast experimentation. 

## How does this actually work:
1. The initial input data are written descriptions of what you want the test cases to do, for example, is the date field in the correct format?
2. This gets put into a "word embedding" or normalization layer to reduce the variance of the verbiage in the test case, this really only matters when you aren't generating the descriptions of the test cases and they aren't already written in standard format.
3. Take the output from this model and feed it into the Google PaLM API, and generate code based on each written description.
## Install:
First, install all of the above libraries.

```bash
git clone https://github.com/Viz/NLP2SQL
cd NLP2SQL/PaLM
pip3 -r requirements.txt
```

## Train: 
So we need to actually train the larger model on SQL code 

| Model Size | Num Tokens | Dim | Depth | Dim Head | Heads | Flash Attention | Learning Rate |
| -------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 150 M | 50304 | 768 | 12 | 128 | 8 | True | 6e-4 |
| 410 M | 50304 | 1024 | 24 | 128 | 8 | True | 3e-4 |
| 1 B | 50304 | 2048 | 16 | 128 | 8 | True | 3e-4 |
| 2.1 B | 50304 | 2560 | 24 | 128 | 8 | True | 1.8e-4 |




## Run:
```python
python3 inference.py "Your Test Prompt" --seq_len 1000 --temperature 0.5 --filter_thres 0.6 --model "palm_410m_8k_v0"
```


## Citations 

```bibtex
@inproceedings{Chowdhery2022PaLMSL,
    title   = {PaLM: Scaling Language Modeling with Pathways},
    author  = {Aakanksha Chowdhery and Sharan Narang and Jacob Devlin and Maarten Bosma and Gaurav Mishra and Adam Roberts and Paul Barham and Hyung Won Chung and Charles Sutton and Sebastian Gehrmann and Parker Schuh and Kensen Shi and Sasha Tsvyashchenko and Joshua Maynez and Abhishek Rao and Parker Barnes and Yi Tay and Noam M. Shazeer and Vinodkumar Prabhakaran and Emily Reif and Nan Du and Benton C. Hutchinson and Reiner Pope and James Bradbury and Jacob Austin and Michael Isard and Guy Gur-Ari and Pengcheng Yin and Toju Duke and Anselm Levskaya and Sanjay Ghemawat and Sunipa Dev and Henryk Michalewski and Xavier Garc{\'i}a and Vedant Misra and Kevin Robinson and Liam Fedus and Denny Zhou and Daphne Ippolito and David Luan and Hyeontaek Lim and Barret Zoph and Alexander Spiridonov and Ryan Sepassi and David Dohan and Shivani Agrawal and Mark Omernick and Andrew M. Dai and Thanumalayan Sankaranarayana Pillai and Marie Pellat and Aitor Lewkowycz and Erica Oliveira Moreira and Rewon Child and Oleksandr Polozov and Katherine Lee and Zongwei Zhou and Xuezhi Wang and Brennan Saeta and Mark Diaz and Orhan Firat and Michele Catasta and Jason Wei and Kathleen S. Meier-Hellstern and Douglas Eck and Jeff Dean and Slav Petrov and Noah Fiedel},
    year    = {2022}
}
```
```bibtex
@inproceedings{Sun2022ALT,
    title     = {A Length-Extrapolatable Transformer},
    author    = {Yutao Sun and Li Dong and Barun Patra and Shuming Ma and Shaohan Huang and Alon Benhaim and Vishrav Chaudhary and Xia Song and Furu Wei},
    year      = {2022}
}
```
```bibtex
@inproceedings{dao2022flashattention,
    title   = {Flash{A}ttention: Fast and Memory-Efficient Exact Attention with {IO}-Awareness},
    author  = {Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
    booktitle = {Advances in Neural Information Processing Systems},
    year    = {2022}
}
```
```bibtex
@misc{zhao2023pytorch,
    title={PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel}, 
    author={Yanli Zhao and Andrew Gu and Rohan Varma and Liang Luo and Chien-Chin Huang and Min Xu and Less Wright and Hamid Shojanazeri and Myle Ott and Sam Shleifer and Alban Desmaison and Can Balioglu and Bernard Nguyen and Geeta Chauhan and Yuchen Hao and Shen Li},
    year={2023},
}
```
```bibtex
@article{zhongSeq2SQL2017,
  author    = {Victor Zhong and
               Caiming Xiong and
               Richard Socher},
  title     = {Seq2SQL: Generating Structured Queries from Natural Language using
               Reinforcement Learning},
  journal   = {CoRR},
  volume    = {abs/1709.00103},
  year      = {2017}
}
```
