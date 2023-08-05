# Pyterrier

## Terrier Python API

# Installation

pip install python-terrier

### Windows

### Linux

### Colab notebooks

# Indexing

### Indexing TREC formatted collections
```
index_path = "/home/alex/Documents/index"
path = "/home/alex/Downloads/books/doc-text.trec"
index_path = createTRECIndex(index_path, path)
```

### Indexing text files

### Indexing a pandas dataframe

Firstly, lets create an example dataframe

```
df = pd.DataFrame({'docno':  ['1', '2', '3'],
        'url': ['url1', 'url2', 'url3'],
         'text' : ['He ran out of money, so he had to stop playing',
          'The waves were crashing on the shore; it was a',
          'The body may perhaps compensates for the loss']
        })
```

Then there are a number of options to index that dataframe:
```
index = createDFIndex(index_path, df["text"])
index = createDFIndex(index_path, df["text"], df["docno"])
index = createDFIndex(index_path, df["text"], df["docno"], df["url"])
index = createDFIndex(index_path, df["text"], df)
index = createDFIndex(index_path, df["text"], docno=["1","2","3"])
meta_fields={"docno":["1","2","3"],"url":["url1", "url2", "url3"]}
index = createDFIndex(index_path, df["text"], **meta_fields)
```

# Retrieval

# Evaluation
